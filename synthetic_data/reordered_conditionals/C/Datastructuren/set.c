// REORDERINGS EXECUTED: 0

struct set { struct tree *tree; };
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
int set_insert(struct set *s, int num) { return tree_insert(s->tree, num); }
int set_find(struct set *s, int num) { return tree_find(s->tree, num); }
int set_remove(struct set *s, int num) { return tree_remove(s->tree, num); }
void set_cleanup(struct set *s)
{
    tree_cleanup(s->tree);
    free(s);
}
void set_print(struct set *s) { tree_print(s->tree); }
int set_verify(struct set *s) { return tree_check(s->tree); }
