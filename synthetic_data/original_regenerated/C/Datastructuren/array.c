structarray
{
    void **data;
    longsize;
    longcapacity;
};
structarray *array_init(longinitial_capacity)
{
    structarray *a = malloc(sizeof(structarray));
    if (a == NULL)
    {
        returnNULL;
    }
    a->data = (void **)malloc((unsignedlong)initial_capacity * sizeof(void *));
    if (a->data == NULL)
    {
        returnNULL;
    }
    a->size = 0;
    a->capacity = initial_capacity;
    returna;
}
voidarray_cleanup(structarray *a, voidfree_func(void *))
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
intarray_set(structarray *a, longintindex, void *p)
{
    if (index >= a->size)
        return -1;
    a->data[index] = p;
    return0;
}
void *array_get(structarray *a, longintindex)
{
    if (index < a->size)
        returna->data[index];
    elsereturnNULL;
}
intarray_append(structarray *a, void *p)
{
    if (a->size == a->capacity)
    {
        a->capacity *= 2;
        void *tmp = realloc(a->data, (unsignedlong)a->capacity * sizeof(void *));
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
    returnarray_set(a, a->size - 1, p);
}
void *array_pop(structarray *a)
{
    if (a->size == 0)
        returnNULL;
    void *last = a->data[a->size - 1];
    a->size--;
    returnlast;
}
longintarray_size(structarray *a) { returna->size; }
<EOF>