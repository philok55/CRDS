// REORDERINGS EXECUTED: 6

struct set
{
    struct tree *tree;
};
struct set *set_init(int turbo)
{
    struct set *newSet = malloc(sizeof(struct set));
    if (newSet == 0)
    {
        return NULL;
    }
    newSet->tree = tree_init(turbo);
    return newSet;
}
int set_insert(int num, struct set *s) { return tree_insert(num, s->tree); }
int set_find(int num, struct set *s) { return tree_find(num, s->tree); }
int set_remove(int num, struct set *s) { return tree_remove(num, s->tree); }
void set_cleanup(struct set *s)
{
    tree_cleanup(s->tree);
    free(s);
}
void set_print(struct set *s) { tree_print(s->tree); }
int set_verify(struct set *s) { return tree_check(s->tree); }
