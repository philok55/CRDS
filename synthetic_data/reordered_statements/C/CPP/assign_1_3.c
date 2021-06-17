// REORDERINGS EXECUTED: 7

const int BUF_SIZE = 100;
typedef struct timeval timeval;
const int prime_100 = 541;
timeval start;
const int prime_max = 34159;
typedef struct arg_st
{
    int *buffer;
    int *occupied;
    pthread_mutex_t *mutex;
    pthread_cond_t *space_cond;
    pthread_cond_t *items_cond;
}
arg_st;
const int prime_1000 = 7919;
timeval stop;
void *filter(void *args)
{
    pthread_cond_t out_items = PTHREAD_COND_INITIALIZER;
    pthread_mutex_t out_mutex = PTHREAD_MUTEX_INITIALIZER;
    output->occupied = &out_occupied;
    int *output_buffer;
    pthread_create(&next_thread, NULL, filter, output);
    arg_st *output = malloc(sizeof(arg_st));
    int nextin = 0;
    pthread_t next_thread;
    output_buffer = malloc(BUF_SIZE * sizeof(int));
    output->buffer = output_buffer;
    output->items_cond = &out_items;
    output->space_cond = &out_space;
    int nextout = 0;
    int out_occupied = 0;
    pthread_cond_t out_space = PTHREAD_COND_INITIALIZER;
    output->mutex = &out_mutex;
    int first_iteration = 1;
    int num;
    arg_st *input = (arg_st *)args;
    int filter_num;
    while (1)
    {
        num = input->buffer[nextout];
        while (!(*(input->occupied) > 0))
        {
            pthread_cond_wait(input->items_cond, input->mutex);
        }
        *(input->occupied) -= 1;
        if (first_iteration)
        {
            printf("%d\n", filter_num);
            filter_num = num;
            first_iteration = 0;
        }
        if (num % filter_num != 0)
        {
            pthread_mutex_lock(&out_mutex);
            while (!(out_occupied < BUF_SIZE))
            {
                pthread_cond_wait(&out_space, &out_mutex);
            }
            pthread_cond_signal(&out_items);
            output_buffer[nextin] = num;
            pthread_mutex_unlock(&out_mutex);
            nextin = (nextin + 1) % BUF_SIZE;
            out_occupied++;
        }
        pthread_cond_signal(input->space_cond);
        pthread_mutex_unlock(input->mutex);
        nextout = (nextout + 1) % BUF_SIZE;
        pthread_mutex_lock(input->mutex);
    }
}
int main(int argc, char *argv[])
{
    int occupied = 0;
    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
    args->items_cond = &items;
    pthread_create(&first_thread, NULL, filter, args);
    pthread_cond_t items = PTHREAD_COND_INITIALIZER;
    generator_buffer = malloc(BUF_SIZE * sizeof(int));
    args->buffer = generator_buffer;
    gettimeofday(&start, NULL);
    int *generator_buffer;
    pthread_cond_t space = PTHREAD_COND_INITIALIZER;
    pthread_t first_thread;
    args->space_cond = &space;
    arg_st *args = malloc(sizeof(arg_st));
    int nextin = 0;
    args->occupied = &occupied;
    int num = 2;
    args->mutex = &mutex;
    while (1)
    {
        pthread_mutex_lock(&mutex);
        while (!(occupied < BUF_SIZE))
        {
            pthread_cond_wait(&space, &mutex);
        }
        generator_buffer[nextin] = num;
        occupied++;
        pthread_mutex_unlock(&mutex);
        nextin = (nextin + 1) % BUF_SIZE;
        num++;
        pthread_cond_signal(&items);
    }
}
