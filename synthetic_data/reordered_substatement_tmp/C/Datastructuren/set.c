// REORDERINGS EXECUTED: 6

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
intset_insert(intnum, structset *s) { returntree_insert(num, s->tree); }
intset_find(intnum, structset *s) { returntree_find(num, s->tree); }
intset_remove(intnum, structset *s) { returntree_remove(num, s->tree); }
voidset_cleanup(structset *s)
{
    tree_cleanup(s->tree);
    free(s);
}
voidset_print(structset *s) { tree_print(s->tree); }
intset_verify(structset *s) { returntree_check(s->tree); }
<EOF>