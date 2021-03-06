typedefstructarg_st
{
    int *buffer;
    int *occupied;
    pthread_mutex_t *mutex;
    pthread_cond_t *space_cond;
    pthread_cond_t *items_cond;
}
arg_st;
constintBUF_SIZE = 100;
constintprime_100 = 541;
constintprime_1000 = 7919;
constintprime_max = 34159;
typedefstructtimevaltimeval;
timevalstart;
timevalstop;
void *filter(void *args)
{
    arg_st *input = (arg_st *)args;
    intfirst_iteration = 1;
    intnextout = 0;
    intnextin = 0;
    intnum;
    intfilter_num;
    int *output_buffer;
    output_buffer = malloc(BUF_SIZE * sizeof(int));
    pthread_mutex_tout_mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_tout_space = PTHREAD_COND_INITIALIZER;
    pthread_cond_tout_items = PTHREAD_COND_INITIALIZER;
    pthread_tnext_thread;
    intout_occupied = 0;
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
intmain(intargc, char *argv[])
{
    gettimeofday(&start, NULL);
    intnextin = 0;
    intnum = 2;
    int *generator_buffer;
    generator_buffer = malloc(BUF_SIZE * sizeof(int));
    pthread_tfirst_thread;
    pthread_mutex_tmutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_tspace = PTHREAD_COND_INITIALIZER;
    pthread_cond_titems = PTHREAD_COND_INITIALIZER;
    intoccupied = 0;
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
<EOF>