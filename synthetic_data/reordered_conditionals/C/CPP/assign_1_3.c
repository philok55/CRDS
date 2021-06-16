// REORDERINGS EXECUTED: 0

typedef struct arg_st
{
    int *buffer;
    int *occupied;
    pthread_mutex_t *mutex;
    pthread_cond_t *space_cond;
    pthread_cond_t *items_cond;
}
arg_st;
const int BUF_SIZE = 100;
const int prime_100 = 541;
const int prime_1000 = 7919;
const int prime_max = 34159;
typedef struct timeval timeval;
timeval start;
timeval stop;
void *filter(void *args)
{
    arg_st *input = (arg_st *)args;
    int first_iteration = 1;
    int nextout = 0;
    int nextin = 0;
    int num;
    int filter_num;
    int *output_buffer;
    output_buffer = malloc(BUF_SIZE * sizeof(int));
    pthread_mutex_t out_mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t out_space = PTHREAD_COND_INITIALIZER;
    pthread_cond_t out_items = PTHREAD_COND_INITIALIZER;
    pthread_t next_thread;
    int out_occupied = 0;
    arg_st *output = malloc(sizeof(arg_st));
    output->buffer = output_buffer;
    output->mutex = &out_mutex;
    output->occupied = &out_occupied;
    output->space_cond = &out_space;
    output->items_cond = &out_items;
    pthread_create(&next_thread, NULL, filter, output);
    while (1)
    {
        pthread_mutex_lock(input->mutex);
        while (!(*(input->occupied) > 0))
        {
            pthread_cond_wait(input->items_cond, input->mutex);
        }
        num = input->buffer[nextout];
        if (first_iteration)
        {
            filter_num = num;
            printf("%d\n", filter_num);
            first_iteration = 0;
        }
        if (num % filter_num != 0)
        {
            pthread_mutex_lock(&out_mutex);
            while (!(out_occupied < BUF_SIZE))
            {
                pthread_cond_wait(&out_space, &out_mutex);
            }
            output_buffer[nextin] = num;
            nextin = (nextin + 1) % BUF_SIZE;
            out_occupied++;
            pthread_cond_signal(&out_items);
            pthread_mutex_unlock(&out_mutex);
        }
        nextout = (nextout + 1) % BUF_SIZE;
        *(input->occupied) -= 1;
        pthread_cond_signal(input->space_cond);
        pthread_mutex_unlock(input->mutex);
    }
}
int main(int argc, char *argv[])
{
    gettimeofday(&start, NULL);
    int nextin = 0;
    int num = 2;
    int *generator_buffer;
    generator_buffer = malloc(BUF_SIZE * sizeof(int));
    pthread_t first_thread;
    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t space = PTHREAD_COND_INITIALIZER;
    pthread_cond_t items = PTHREAD_COND_INITIALIZER;
    int occupied = 0;
    arg_st *args = malloc(sizeof(arg_st));
    args->buffer = generator_buffer;
    args->mutex = &mutex;
    args->occupied = &occupied;
    args->space_cond = &space;
    args->items_cond = &items;
    pthread_create(&first_thread, NULL, filter, args);
    while (1)
    {
        pthread_mutex_lock(&mutex);
        while (!(occupied < BUF_SIZE))
        {
            pthread_cond_wait(&space, &mutex);
        }
        generator_buffer[nextin] = num;
        nextin = (nextin + 1) % BUF_SIZE;
        occupied++;
        num++;
        pthread_cond_signal(&items);
        pthread_mutex_unlock(&mutex);
    }
}
