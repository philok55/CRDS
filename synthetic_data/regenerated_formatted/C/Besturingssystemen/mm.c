struct header
{
    size_t size;
    bool is_free;
    struct header *next;
};
typedef struct header header_t;
struct mm_state
{
    header_t *first_el;
    size_t last_activated;
};
mm_state_t *mm_initialize(void)
{
    const struct ram_info *info = hw_raminfo();
    char *base = (char *)info->module_addrs[0];
    hw_activate(0, 0);
    mm_state_t *st = (mm_state_t *)base;
    st->last_activated = 0;
    st->first_el = (header_t *)((char *)st + sizeof(mm_state_t));
    st->first_el->is_free = true;
    st->first_el->size = (info->bank_size * info->nbanks_per_module) - sizeof(header_t) - sizeof(mm_state_t);
    st->first_el->next = NULL;
    return st;
}
void make_header(header_t *header, size_t nbytes)
{
    void *p = (void *)(header + 1);
    if (header->next != NULL)
    {
        header_t *temp = header->next;
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = temp;
    }
    else
    {
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = NULL;
    }
}
void *mm_alloc(mm_state_t *st, size_t nbytes)
{
    const struct ram_info *info = hw_raminfo();
    while (nbytes % sizeof(intmax_t) != 0)
    {
        nbytes++;
    }
    header_t *header = st->first_el;
    while (!header->is_free || header->size < (nbytes + sizeof(header_t)))
    {
        if ((header = header->next) == NULL)
            return 0;
    }
    for (size_t i = curr_bank + 1; i <= end_bank; i++)
    {
        if (i > st->last_activated)
        {
            hw_activate(0, i);
            st->last_activated = i;
        }
    }
    size_t curr_bank = ((char *)header - (char *)info->module_addrs[0] + sizeof(header_t)) / info->bank_size;
    size_t end_bank = ((char *)header - (char *)info->module_addrs[0] + nbytes + sizeof(header_t) * 2) / info->bank_size;
    if (info->nbanks_per_module <= end_bank)
    {
        return 0;
    }
    header->is_free = false;
    void *p = (void *)(header + 1);
    make_header(header, nbytes);
    header->size = (char *)header->next - (char *)p;
    return p;
}
void mm_free(mm_state_t *st, void *ptr)
{
    header_t *current = st->first_el;
    header_t *prev = NULL;
    while (current != (header_t *)ptr - 1)
    {
        prev = current;
        current = current->next;
    }
    if (current == NULL)
    {
        return;
    }
    if (!prev)
    {
        st->first_el = current->next;
    }
    current->is_free = true;
    if (current->next && current->next->is_free)
    {
        current->next = current->next->next;
    }
    if (prev && prev->is_free && current->next && current->next->is_free)
    {
        prev->next = current->next->next;
        prev->size += current->size + sizeof(header_t) * 2 + current->next->size;
    }
    else if(prev && prev->is_free)
    {
        prev->next = current->next;
        prev->size += current->size + sizeof(header_t);
    }
}
