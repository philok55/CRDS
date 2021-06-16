// REORDERINGS EXECUTED: 0

structset { structtree *tree; };
structset *set_init(intturbo)
{
    structset *newSet = malloc(sizeof(structset));
    if (newSet == 0)
    {
        returnNULL;
    }
    newSet->tree = tree_init(turbo);
    returnnewSet;
}
intset_insert(structset *s, intnum) { returntree_insert(s->tree, num); }
intset_find(structset *s, intnum) { returntree_find(s->tree, num); }
intset_remove(structset *s, intnum) { returntree_remove(s->tree, num); }
voidset_cleanup(structset *s)
{
    tree_cleanup(s->tree);
    free(s);
}
voidset_print(structset *s) { tree_print(s->tree); }
intset_verify(structset *s) { returntree_check(s->tree); }
<EOF>