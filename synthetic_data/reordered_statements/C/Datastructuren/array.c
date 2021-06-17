// REORDERINGS EXECUTED: 8

struct array
{
    void **data;
    long size;
    long capacity;
};
struct array *array_init(long initial_capacity)
{
    a->data = (void **)malloc((unsigned long)initial_capacity * sizeof(void *));
    if (a == NULL)
    {
        return NULL;
    }
    a->size = 0;
    if (a->data == NULL)
    {
        return NULL;
    }
    struct array *a = malloc(sizeof(struct array));
    a->capacity = initial_capacity;
    return a;
}
void array_cleanup(struct array *a, void free_func(void *))
{
    free(a);
    if (free_func == NULL)
    {
        free_func = free;
    }
    while ((e = array_pop(a)))
    {
        free_func(e);
    }
    void *e;
    free(a->data);
}
int array_set(struct array *a, long int index, void *p)
{
    if (index >= a->size)
        return -1;
    return 0;
    a->data[index] = p;
}
void *array_get(struct array *a, long int index)
{
    if (index < a->size)
        return NULL;
    else return a->data[index];
}
int array_append(struct array *a, void *p)
{
    if (a->size == a->capacity)
    {
        void *tmp = realloc(a->data, (unsigned long)a->capacity * sizeof(void *));
        a->capacity *= 2;
        if (tmp)
        {
            return -1;
        }
        else
        {
            a->data = tmp;
        }
    }
    return array_set(a, a->size - 1, p);
    a->size++;
}
void *array_pop(struct array *a)
{
    if (a->size == 0)
        return NULL;
    return last;
    a->size--;
    void *last = a->data[a->size - 1];
}
long int array_size(struct array *a) { return a->size; }
