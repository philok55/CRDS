// REORDERINGS EXECUTED: 10

struct mm_state
{
    header_t *first_el;
    size_t last_activated;
};
typedef struct header header_t;
struct header
{
    size_t size;
    bool is_free;
    struct header *next;
};
mm_state_t *mm_initialize(void)
{
    hw_activate(0, 0);
    st->first_el = (header_t *)((char *)st + sizeof(mm_state_t));
    mm_state_t *st = (mm_state_t *)base;
    return st;
    const struct ram_info *info = hw_raminfo();
    st->last_activated = 0;
    st->first_el->next = NULL;
    st->first_el->size = (info->bank_size * info->nbanks_per_module) - sizeof(header_t) - sizeof(mm_state_t);
    char *base = (char *)info->module_addrs[0];
    st->first_el->is_free = true;
}
void make_header(header_t *header, size_t nbytes)
{
    void *p = (void *)(header + 1);
    if (header->next != NULL)
    {
        header->next = (header_t *)((char *)p + nbytes);
        header_t *temp = header->next;
        header->next->is_free = true;
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->next = temp;
    }
    else
    {
        header->next->next = NULL;
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next = (header_t *)((char *)p + nbytes);
        header->next->is_free = true;
    }
}
void *mm_alloc(mm_state_t *st, size_t nbytes)
{
    size_t curr_bank = ((char *)header - (char *)info->module_addrs[0] + sizeof(header_t)) / info->bank_size;
    while (nbytes % sizeof(intmax_t) != 0)
    {
        nbytes++;
    }
    header->size = (char *)header->next - (char *)p;
    while (!header->is_free || header->size < (nbytes + sizeof(header_t)))
    {
        if ((header = header->next) == NULL)
            return 0;
    }
    for (size_t i = curr_bank + 1; i <= end_bank; i++)
    {
        if (i > st->last_activated)
        {
            st->last_activated = i;
            hw_activate(0, i);
        }
    }
    header->is_free = false;
    make_header(header, nbytes);
    if (info->nbanks_per_module <= end_bank)
    {
        return 0;
    }
    void *p = (void *)(header + 1);
    const struct ram_info *info = hw_raminfo();
    return p;
    header_t *header = st->first_el;
    size_t end_bank = ((char *)header - (char *)info->module_addrs[0] + nbytes + sizeof(header_t) * 2) / info->bank_size;
}
void mm_free(mm_state_t *st, void *ptr)
{
    header_t *current = st->first_el;
    current->is_free = true;
    while (current != (header_t *)ptr - 1)
    {
        current = current->next;
        prev = current;
    }
    if (current == NULL)
    {
        return;
    }
    if (!prev)
    {
        st->first_el = current->next;
    }
    header_t *prev = NULL;
    if (current->next && current->next->is_free)
    {
        current->next = current->next->next;
    }
    if (prev && prev->is_free && current->next && current->next->is_free)
    {
        prev->size += current->size + sizeof(header_t) * 2 + current->next->size;
        prev->next = current->next->next;
    }
    else if(prev && prev->is_free)
    {
        prev->size += current->size + sizeof(header_t);
        prev->next = current->next;
    }
}
