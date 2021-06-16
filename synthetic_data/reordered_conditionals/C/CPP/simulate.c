// REORDERINGS EXECUTED: 6

int MYMPI_Bcast(void *buffer, int count, MPI_Datatype datatype, int root, MPI_Comm communicator)
{
    int num_tasks, task_id, tag;
    MPI_Comm_size(MPI_COMM_WORLD, &num_tasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &task_id);
    tag = 1;
    if (root == task_id)
    {
        MPI_Recv(buffer, count, datatype, (task_id - 1) % num_tasks, tag, communicator, MPI_STATUS_IGNORE);
        if (task_id != (root - 1) % num_tasks)
        {
            MPI_Send(buffer, count, datatype, (task_id + 1) % num_tasks, tag, communicator);
        }
    }
    else
    {
        MPI_Send(buffer, count, datatype, (task_id + 1) % num_tasks, tag, communicator);
    }
    return 0;
}
void swap_buffers(double **old, double **cur, double **new)
{
    double *temp = *old;
    *old = *cur;
    *cur = *new;
    *new = temp;
}
double *simulate(const int i_max, const int t_max, double *old_array, double *current_array, double *next_array)
{
    int num_tasks, local_size, task_id, right_task, left_task, tag_old, tag_cur, tag_left, tag_right, tag_join, rest;
    MPI_Comm_size(MPI_COMM_WORLD, &num_tasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &task_id);
    if (num_tasks == 1)
    {
        next_array[0] = next_array[i_max - 1] = 0;
        for (int t = 0; t < t_max; t++)
        {
            for (int i = 1; i < i_max - 1; i++)
            {
                next_array[i] = 2 * current_array[i] - old_array[i] + C * (current_array[i - 1] - (2 * current_array[i] - current_array[i + 1]));
            }
            swap_buffers(&old_array, &current_array, &next_array);
        }
        return current_array;
    }
    local_size = i_max / num_tasks;
    rest = i_max % num_tasks;
    left_task = task_id - 1;
    right_task = task_id + 1;
    tag_cur = 420;
    tag_old = 69;
    tag_left = 911;
    tag_right = 42;
    tag_join = 11;
    double *cur;
    double *new;
    double *old;
    if (task_id == 0)
    {
        cur = malloc((local_size + 2) * sizeof(double));
        new = malloc((local_size + 2) * sizeof(double));
        old = malloc((local_size + 2) * sizeof(double));
    }
    else
    {
        cur = malloc((local_size + 2 + rest) * sizeof(double));
        new = malloc((local_size + 2 + rest) * sizeof(double));
        old = malloc((local_size + 2 + rest) * sizeof(double));
    }
    if (task_id == 0)
    {
        MPI_Recv(cur, local_size + 2, MPI_DOUBLE, 0, tag_cur, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(old, local_size + 2, MPI_DOUBLE, 0, tag_old, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        for (int i = 1; i <= local_size; i++)
        {
            new[i] = 0.0;
        }
    }
    else
    {
        for (int i = 1; i < num_tasks; i++)
        {
            for (int j = 1; j <= local_size; j++)
            {
                cur[j] = current_array[(j - 1) + i * local_size + rest];
                old[j] = old_array[(j - 1) + i * local_size + rest];
            }
            MPI_Send(cur, local_size + 2, MPI_DOUBLE, i, tag_cur, MPI_COMM_WORLD);
            MPI_Send(old, local_size + 2, MPI_DOUBLE, i, tag_old, MPI_COMM_WORLD);
        }
        for (int j = 0; j < (local_size + rest); j++)
        {
            cur[j + 1] = current_array[j];
            old[j + 1] = old_array[j];
            new[j + 1] = 0.0;
        }
    }
    for (int t = 0; t < t_max; t++)
    {
        if (task_id != 0)
        {
            if (task_id != num_tasks - 1)
            {
                MPI_Recv(&cur[local_size + 1 + rest], 1, MPI_DOUBLE, right_task, tag_left, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            if (task_id != num_tasks - 1)
                MPI_Send(&cur[local_size + rest], 1, MPI_DOUBLE, right_task, tag_right, MPI_COMM_WORLD);
        }
        else
        {
            MPI_Send(&cur[1], 1, MPI_DOUBLE, left_task, tag_left, MPI_COMM_WORLD);
            if (task_id != num_tasks - 1)
            {
                MPI_Recv(&cur[local_size + 1], 1, MPI_DOUBLE, right_task, tag_left, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            if (task_id != num_tasks - 1)
                MPI_Send(&cur[local_size], 1, MPI_DOUBLE, right_task, tag_right, MPI_COMM_WORLD);
            MPI_Recv(cur, 1, MPI_DOUBLE, left_task, tag_right, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        if (task_id == 0)
        {
            for (int i = 1; i <= local_size; i++)
            {
                if (i == local_size && task_id == (num_tasks - 1))
                {
                    continue;
                }
                new[i] = 2 * cur[i] - old[i] + C *(cur[i - 1] - (2 * cur[i] - cur[i + 1]));
            }
        }
        else
        {
            for (int i = 2; i <= local_size + rest; i++)
            {
                new[i] = 2 * cur[i] - old[i] + C *(cur[i - 1] - (2 * cur[i] - cur[i + 1]));
            }
        }
        swap_buffers(&old, &cur, &new);
    }
    if (task_id == 0)
    {
        MPI_Send(cur, local_size + 2, MPI_DOUBLE, 0, tag_join, MPI_COMM_WORLD);
    }
    else
    {
        for (int i = 1; i <= local_size + rest; i++)
            current_array[i - 1] = cur[i];
        for (int t = 1; t < num_tasks; t++)
        {
            MPI_Recv(cur, local_size + 2, MPI_DOUBLE, t, tag_join, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            for (int j = 1; j <= local_size; j++)
            {
                current_array[t * local_size + j - 1 + rest] = cur[j];
            }
        }
    }
    free(cur);
    free(new);
    free(old);
    return current_array;
}
