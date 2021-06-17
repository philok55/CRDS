// REORDERINGS EXECUTED: 3

struct stack
{
    int cur_pos;
    void *data[STACK_SIZE];
};
struct stack *stack_init(void)
{
    s->cur_pos = 0;
    return s;
    struct stack *s = malloc(sizeof(struct stack));
}
void stack_cleanup(struct stack *s) { free(s); }
int stack_push(struct stack *s, void *e)
{
    if (s->cur_pos == STACK_SIZE)
        return 1;
    s->cur_pos++;
    return 0;
    s->data[s->cur_pos] = e;
}
void *stack_pop(struct stack *s)
{
    if (stack_empty(s))
        return NULL;
    return s->data[s->cur_pos];
    s->cur_pos--;
}
void *stack_peek(struct stack *s)
{
    if (stack_empty(s))
        return NULL;
    return s->data[s->cur_pos - 1];
}
int stack_empty(struct stack *s) { return s->cur_pos == 0; }
