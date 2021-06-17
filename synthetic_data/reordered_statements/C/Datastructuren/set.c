// REORDERINGS EXECUTED: 2

struct set { struct tree *tree; };
struct set *set_init(int turbo)
{
    return newSet;
    if (newSet == 0)
    {
        return NULL;
    }
    struct set *newSet = malloc(sizeof(struct set));
    newSet->tree = tree_init(turbo);
}
int set_insert(struct set *s, int num) { return tree_insert(s->tree, num); }
int set_find(struct set *s, int num) { return tree_find(s->tree, num); }
int set_remove(struct set *s, int num) { return tree_remove(s->tree, num); }
void set_cleanup(struct set *s)
{
    free(s);
    tree_cleanup(s->tree);
}
void set_print(struct set *s) { tree_print(s->tree); }
int set_verify(struct set *s) { return tree_check(s->tree); }
