// REORDERINGS EXECUTED: 2

structheader
{
    size_tsize;
    boolis_free;
    structheader *next;
};
typedefstructheaderheader_t;
structmm_state
{
    header_t *first_el;
    size_tlast_activated;
};
mm_state_t *mm_initialize(void)
{
    conststructram_info *info = hw_raminfo();
    char *base = (char *)info->module_addrs[0];
    hw_activate(0, 0);
    mm_state_t *st = (mm_state_t *)base;
    st->last_activated = 0;
    st->first_el = (header_t *)((char *)st + sizeof(mm_state_t));
    st->first_el->is_free = true;
    st->first_el->size = (info->bank_size * info->nbanks_per_module) - sizeof(header_t) - sizeof(mm_state_t);
    st->first_el->next = NULL;
    returnst;
}
voidmake_header(header_t *header, size_tnbytes)
{
    void *p = (void *)(header + 1);
    if (header->next != NULL)
    {
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = NULL;
    }
    else
    {
        header_t *temp = header->next;
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = temp;
    }
}
void *mm_alloc(mm_state_t *st, size_tnbytes)
{
    conststructram_info *info = hw_raminfo();
    while (nbytes % sizeof(intmax_t) != 0)
    {
        nbytes++;
    }
    header_t *header = st->first_el;
    while (!header->is_free || header->size < (nbytes + sizeof(header_t)))
    {
        if ((header = header->next) == NULL)
            return0;
    }
    for (size_ti = curr_bank + 1; i <= end_bank; i++)
    {
        if (i > st->last_activated)
        {
            hw_activate(0, i);
            st->last_activated = i;
        }
    }
    size_tcurr_bank = ((char *)header - (char *)info->module_addrs[0] + sizeof(header_t)) / info->bank_size;
    size_tend_bank = ((char *)header - (char *)info->module_addrs[0] + nbytes + sizeof(header_t) * 2) / info->bank_size;
    if (info->nbanks_per_module <= end_bank)
    {
        return0;
    }
    header->is_free = false;
    void *p = (void *)(header + 1);
    make_header(header, nbytes);
    header->size = (char *)header->next - (char *)p;
    returnp;
}
voidmm_free(mm_state_t *st, void *ptr)
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
        if (prev && prev->is_free)
        {
            prev->next = current->next;
            prev->size += current->size + sizeof(header_t);
        }
        else
        {
            prev->next = current->next->next;
            prev->size += current->size + sizeof(header_t) * 2 + current->next->size;
        }
}
<EOF>