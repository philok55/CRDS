/*
 * simulate.c
 *
 * Names: Thijn Albers, Philo Decroos
 * Student ID's: 11874295, 11752262
 *
 * This file simulates the calculation of a wave using the MPI programming
 * model, making parallelism with distributed memory possible. It also contains
 * a function that implements an MPI Broadcast message.
 */

#include <stdio.h>
#include <stdlib.h>
#include "simulate.h"
#include "mpi.h"

#define C 0.15


/* MYMPI_Bcast implements a broadcast message within an MPI communicator.
 * Root is the initiator, and sens its content of buffer to all other processes
 * in the same communicator. They will receive this message and put the content
 * in their buffer. In this case we assume a circular network topology, which
 * means the messages will hop through the network via other processes to be
 * distributed to all of them.
 */
int MYMPI_Bcast (void* buffer, int count, MPI_Datatype datatype, int root, MPI_Comm communicator) {
    int num_tasks, task_id, tag;
    MPI_Comm_size(MPI_COMM_WORLD, &num_tasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &task_id);
    tag = 1;

    if (root == task_id) {  // initiate the broadcast
        MPI_Send(buffer, count, datatype, (task_id + 1) % num_tasks, tag, communicator);
    } else {  // receive from neighbor and send further through network
        MPI_Recv(buffer, count, datatype, (task_id - 1) % num_tasks, tag, communicator, MPI_STATUS_IGNORE);
        if (task_id != (root - 1) % num_tasks) {
            MPI_Send(buffer, count, datatype, (task_id + 1) % num_tasks, tag, communicator);
        }
    }
    return 0;
}


/* This function swaps the three buffers after every time step. */
void swap_buffers(double **old, double **cur, double **new)
{
    double *temp = *old;
    *old = *cur;
    *cur = *new;
    *new = temp;
}

/*
 * Executes the entire simulation.
 *
 * Simulate is executed by every process spawned by MPI. Process with taskID
 * 0 is the master process: it distributes the data over the rest of the threads
 * and rejoins everything at the end to return it. This function takes care
 * of all computation and synchronization.
 *
 * i_max: how many data points are on a single wave
 * t_max: how many iterations the simulation should run
 * old_array: array of size i_max filled with data for t-1
 * current_array: array of size i_max filled with data for t
 * next_array: array of size i_max. You should fill this with t+1
 */
double *simulate(const int i_max, const int t_max, double *old_array,
        double *current_array, double *next_array)
{
    int num_tasks, local_size, task_id, right_task, left_task, tag_old, tag_cur, tag_left, tag_right, tag_join, rest;

    MPI_Comm_size(MPI_COMM_WORLD, &num_tasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &task_id);

    /* If the amount of tasks is 1 we don't need to do any synchronization:
     * we only have a master process that executes the sequential code and
     * returns the result.
     */
    if (num_tasks == 1) {
        next_array[0] = next_array[i_max - 1] = 0;
        for (int t = 0; t < t_max; t++)
        {
            for (int i = 1; i < i_max - 1; i++)
            {
                next_array[i] = 2 * current_array[i] - old_array[i] + C *
                                (current_array[i - 1] - (2 * current_array[i] -
                                current_array[i + 1]));
            }
            swap_buffers(&old_array, &current_array, &next_array);
        }
        return current_array;
    }

    // the size of the part of the arrays every task gets
    local_size = i_max / num_tasks;

    // if i_max % num_tasks is not 0 we need to give a rest to one of the processes
    rest = i_max % num_tasks;
    left_task = task_id - 1;
    right_task = task_id + 1;

    // tags for the messages
    tag_cur = 420;
    tag_old = 69;
    tag_left = 911;
    tag_right = 42;
    tag_join = 11;

    // local parts of the arrays
    double *cur;
    double *new;
    double *old;

    if (task_id == 0) {
        cur = malloc((local_size + 2 + rest) * sizeof(double));
        new = malloc((local_size + 2 + rest) * sizeof(double));
        old = malloc((local_size + 2 + rest) * sizeof(double));
    } else {
        cur = malloc((local_size + 2) * sizeof(double));
        new = malloc((local_size + 2) * sizeof(double));
        old = malloc((local_size + 2) * sizeof(double));
    }

    // setting up the threads
    if (task_id == 0) {  // master thread
        for (int i = 1; i < num_tasks; i++) {
            for (int j = 1; j <= local_size; j++) {
                cur[j] = current_array[(j-1) + i*local_size + rest];
                old[j] = old_array[(j-1) + i*local_size + rest];
            }
            MPI_Send(cur, local_size + 2, MPI_DOUBLE, i, tag_cur, MPI_COMM_WORLD);
            MPI_Send(old, local_size + 2, MPI_DOUBLE, i, tag_old, MPI_COMM_WORLD);
        }
        for (int j = 0; j < (local_size + rest); j++) {
            // Initialise own arrays, the master takes care of the rest i-values
            cur[j+1] = current_array[j];
            old[j+1] = old_array[j];
            new[j+1] = 0.0;
        }
    } else {  // worker thread
        MPI_Recv(cur, local_size + 2, MPI_DOUBLE, 0, tag_cur, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(old, local_size + 2, MPI_DOUBLE, 0, tag_old, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        for (int i = 1; i <= local_size; i++) {
            new[i] = 0.0;
        }
    }

    // The calculation
    for (int t = 0; t < t_max; t++) {
        if (task_id != 0) {
            // send to left halo
            MPI_Send(&cur[1], 1, MPI_DOUBLE, left_task, tag_left, MPI_COMM_WORLD);

            // receive from right halo
            if (task_id != num_tasks - 1) {
                MPI_Recv(&cur[local_size + 1], 1, MPI_DOUBLE, right_task, tag_left, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            // send to right halo
            if (task_id != num_tasks - 1)
                MPI_Send(&cur[local_size], 1, MPI_DOUBLE, right_task, tag_right, MPI_COMM_WORLD);

            // receive from right halo
            MPI_Recv(cur, 1, MPI_DOUBLE, left_task, tag_right, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        } else {  // master thread
            // receive from right halo
            if (task_id != num_tasks - 1) {
                MPI_Recv(&cur[local_size + 1 + rest], 1, MPI_DOUBLE, right_task, tag_left, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
            // send to right halo
            if (task_id != num_tasks - 1)
                MPI_Send(&cur[local_size + rest], 1, MPI_DOUBLE, right_task, tag_right, MPI_COMM_WORLD);
        }

        // Different computation loop for master because its arrays are longer
        if (task_id == 0) {
            for (int i = 2; i <= local_size + rest; i++) {
                new[i] = 2 * cur[i] - old[i] + C *
                            (cur[i - 1] -
                            (2 * cur[i] -
                            cur[i + 1]));
            }
        } else {
            for (int i = 1; i <= local_size; i++) {
                if (i == local_size && task_id == (num_tasks - 1)) {
                    continue;  // Rightmost task has no right halo
                }
                new[i] = 2 * cur[i] - old[i] + C *
                            (cur[i - 1] -
                            (2 * cur[i] -
                            cur[i + 1]));
            }
        }

        swap_buffers(&old, &cur, &new);
    }

    // receive all chunks of the array and join them
    if (task_id == 0) {
        for (int i = 1; i <= local_size + rest; i++)
            current_array[i-1] = cur[i];
        for (int t = 1; t < num_tasks; t++) {
            MPI_Recv(cur, local_size + 2, MPI_DOUBLE, t, tag_join, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            for (int j = 1; j <= local_size; j++) {
                current_array[t*local_size + j - 1 + rest] = cur[j];
            }
        }
    } else {
        MPI_Send(cur, local_size + 2, MPI_DOUBLE, 0, tag_join, MPI_COMM_WORLD);
    }

    free(cur);
    free(new);
    free(old);

    /* Returns a pointer to the array with the final results. */
    return current_array;
}
