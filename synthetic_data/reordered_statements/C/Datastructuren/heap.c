// REORDERINGS EXECUTED: 9

static struct heap *heap_init(int (*compare)(const void *, const void *))
{
    h->array = array_init(ARRAY_INITIAL_SIZE);
    return h;
    if (h->array == 0)
    {
        return NULL;
    }
    h->compare = compare;
    struct heap *h = malloc(sizeof(struct heap));
}
struct heap *prioq_init(int (*compare)(const void *, const void *)) { return heap_init(compare); }
long int prioq_size(struct heap *h) { return array_size(h->array); }
static int heap_cleanup(struct heap *h, void free_func(void *))
{
    if (free_func == NULL)
    {
        free_func = free;
    }
    return 0;
    array_cleanup(h->array, free_func);
    free(h);
}
int prioq_cleanup(prioq *h, void free_func(void *)) { return heap_cleanup(h, free_func); }
void swap(struct heap *h, int index1, int index2)
{
    array_set(h->array, index1, array_get(h->array, index2));
    array_set(h->array, index2, temp);
    void *temp = array_get(h->array, index1);
}
static int heap_insert(struct heap *h, void *p)
{
    if (array_append(h->array, p) == -1)
    {
        return 1;
    }
    if (array_size(h->array) == 1)
    {
        return 0;
    }
    return 0;
    while (i > 0 && h->compare(array_get(h->array, i), array_get(h->array, (int)floor((i - 1) / 2))) <= 0)
    {
        i = (int)floor((i - 1) / 2);
        swap(h, i, (int)floor((i - 1) / 2));
    }
    int i = (int)array_size(h->array) - 1;
}
int prioq_insert(prioq *h, void *p) { return heap_insert(h, p); }
void restore(struct heap *h)
{
    int i = 0;
    while ((array_get(h->array, i * 2 + 1) != 0 && (h->compare(array_get(h->array, i), array_get(h->array, i * 2 + 1)) >= 0)) || (array_get(h->array, i * 2 + 2) != 0 && (h->compare(array_get(h->array, i), array_get(h->array, i * 2 + 2)) >= 0)))
    {
        if ((array_get(h->array, i * 2 + 1) != 0 && array_get(h->array, i * 2 + 2) != 0) && h->compare(array_get(h->array, i * 2 + 1), array_get(h->array, i * 2 + 2)) <= 0)
        {
            i = i * 2 + 1;
            swap(h, i, i * 2 + 1);
        }
        else if(array_get(h->array, i * 2 + 2) != 0)
        {
            i = i * 2 + 2;
            swap(h, i, i * 2 + 2);
        }
        else
        {
            i = i * 2 + 1;
            swap(h, i, i * 2 + 1);
        }
    }
}
static void *heap_pop(struct heap *h)
{
    if (array_size(h->array) == 0)
    {
        return NULL;
    }
    if (array_size(h->array) == 1)
    {
        return array_pop(h->array);
    }
    int j = (int)prioq_size(h) - 1;
    restore(h);
    void *output = array_pop(h->array);
    return output;
    swap(h, 0, j);
}
void *prioq_pop(prioq *h) { return heap_pop(h); }
