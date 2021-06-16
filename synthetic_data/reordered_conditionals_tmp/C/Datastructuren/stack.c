// REORDERINGS EXECUTED: 0

structstack
{
    intcur_pos;
    void *data[STACK_SIZE];
};
structstack *stack_init(void)
{
    structstack *s = malloc(sizeof(structstack));
    s->cur_pos = 0;
    returns;
}
voidstack_cleanup(structstack *s) { free(s); }
intstack_push(structstack *s, void *e)
{
    if (s->cur_pos == STACK_SIZE)
        return1;
    s->data[s->cur_pos] = e;
    s->cur_pos++;
    return0;
}
void *stack_pop(structstack *s)
{
    if (stack_empty(s))
        returnNULL;
    s->cur_pos--;
    returns->data[s->cur_pos];
}
void *stack_peek(structstack *s)
{
    if (stack_empty(s))
        returnNULL;
    returns->data[s->cur_pos - 1];
}
intstack_empty(structstack *s) { returns->cur_pos == 0; }
<EOF>