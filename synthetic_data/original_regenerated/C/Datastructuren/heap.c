staticstructheap *heap_init(int (*compare)(constvoid *, constvoid *))
{
    structheap *h = malloc(sizeof(structheap));
    h->array = array_init(ARRAY_INITIAL_SIZE);
    if (h->array == 0)
    {
        returnNULL;
    }
    h->compare = compare;
    returnh;
}
structheap *prioq_init(int (*compare)(constvoid *, constvoid *)) { returnheap_init(compare); }
longintprioq_size(structheap *h) { returnarray_size(h->array); }
staticintheap_cleanup(structheap *h, voidfree_func(void *))
{
    if (free_func == NULL)
    {
        free_func = free;
    }
    array_cleanup(h->array, free_func);
    free(h);
    return0;
}
intprioq_cleanup(prioq *h, voidfree_func(void *)) { returnheap_cleanup(h, free_func); }
voidswap(structheap *h, intindex1, intindex2)
{
    void *temp = array_get(h->array, index1);
    array_set(h->array, index1, array_get(h->array, index2));
    array_set(h->array, index2, temp);
}
staticintheap_insert(structheap *h, void *p)
{
    if (array_append(h->array, p) == -1)
    {
        return1;
    }
    if (array_size(h->array) == 1)
    {
        return0;
    }
    inti = (int)array_size(h->array) - 1;
    while (i > 0 && h->compare(array_get(h->array, i), array_get(h->array, (int)floor((i - 1) / 2))) <= 0)
    {
        swap(h, i, (int)floor((i - 1) / 2));
        i = (int)floor((i - 1) / 2);
    }
    return0;
}
intprioq_insert(prioq *h, void *p) { returnheap_insert(h, p); }
voidrestore(structheap *h)
{
    inti = 0;
    while ((array_get(h->array, i * 2 + 1) != 0 && (h->compare(array_get(h->array, i), array_get(h->array, i * 2 + 1)) >= 0)) || (array_get(h->array, i * 2 + 2) != 0 && (h->compare(array_get(h->array, i), array_get(h->array, i * 2 + 2)) >= 0)))
    {
        if ((array_get(h->array, i * 2 + 1) != 0 && array_get(h->array, i * 2 + 2) != 0) && h->compare(array_get(h->array, i * 2 + 1), array_get(h->array, i * 2 + 2)) <= 0)
        {
            swap(h, i, i * 2 + 1);
            i = i * 2 + 1;
        }
        elseif(array_get(h->array, i * 2 + 2) != 0)
        {
            swap(h, i, i * 2 + 2);
            i = i * 2 + 2;
        }
        else
        {
            swap(h, i, i * 2 + 1);
            i = i * 2 + 1;
        }
    }
}
staticvoid *heap_pop(structheap *h)
{
    if (array_size(h->array) == 0)
    {
        returnNULL;
    }
    if (array_size(h->array) == 1)
    {
        returnarray_pop(h->array);
    }
    intj = (int)prioq_size(h) - 1;
    swap(h, 0, j);
    void *output = array_pop(h->array);
    restore(h);
    returnoutput;
}
void *prioq_pop(prioq *h) { returnheap_pop(h); }
<EOF>