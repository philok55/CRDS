// REORDERINGS EXECUTED: 1

struct array
{
    void **data;
    long size;
    long capacity;
};
int array_append(struct array *a, void *p)
{
    if (a->size == a->capacity)
    {
        a->capacity *= 2;
        void *tmp = realloc(a->data, (unsigned long)a->capacity * sizeof(void *));
        if (tmp)
        {
            a->data = tmp;
        }
        else
        {
            return -1;
        }
    }
    a->size++;
    return array_set(a, a->size - 1, p);
}
int array_set(struct array *a, long int index, void *p)
{
    if (index >= a->size)
        return -1;
    a->data[index] = p;
    return 0;
}
void *array_get(struct array *a, long int index)
{
    if (index < a->size)
        return a->data[index];
    else return NULL;
}
void *array_pop(struct array *a)
{
    if (a->size == 0)
        return NULL;
    void *last = a->data[a->size - 1];
    a->size--;
    return last;
}
void array_cleanup(struct array *a, void free_func(void *))
{
    void *e;
    if (free_func == NULL)
    {
        free_func = free;
    }
    while ((e = array_pop(a)))
    {
        free_func(e);
    }
    free(a->data);
    free(a);
}
long int array_size(struct array *a) { return a->size; }
struct array *array_init(long initial_capacity)
{
    struct array *a = malloc(sizeof(struct array));
    if (a == NULL)
    {
        return NULL;
    }
    a->data = (void **)malloc((unsigned long)initial_capacity * sizeof(void *));
    if (a->data == NULL)
    {
        return NULL;
    }
    a->size = 0;
    a->capacity = initial_capacity;
    return a;
}
