// REORDERINGS EXECUTED: 7

structnode
{
    intvalue;
    structnode *next;
    structnode *prev;
};
structlist
{
    structnode *firstNode;
    intlength;
};
structlist *list_init()
{
    structlist *l = malloc(sizeof(structlist));
    if (l == 0)
    {
        returnNULL;
    }
    l->firstNode = NULL;
    l->length = 0;
    returnl;
}
intlist_cleanup(structlist *l)
{
    structnode *current = l->firstNode;
    if (l->length != 0 && l->length != 1)
        if (l->length == 1)
        {
            list_free_node(l->firstNode);
        }
        else
        {
            while (current->next != NULL)
            {
                current = current->next;
                list_free_node(current->prev);
            }
            list_free_node(current);
        }
    free(l);
    return0;
}
structnode *list_new_node(intnum)
{
    structnode *newNode = malloc(sizeof(structnode));
    if (newNode == 0)
    {
        returnNULL;
    }
    newNode->value = num;
    newNode->next = NULL;
    newNode->prev = NULL;
    returnnewNode;
}
intlist_add(structlist *l, intnum)
{
    structnode *newNode = list_new_node(num);
    if (l->length != 0)
    {
        l->firstNode = newNode;
        if (l->firstNode == 0)
        {
            return1;
        }
    }
    else
    {
        l->firstNode->prev = newNode;
        newNode->next = l->firstNode;
        l->firstNode = newNode;
        if (l->firstNode->next == 0)
        {
            return1;
        }
    }
    l->length++;
    return0;
}
intlist_add_back(structlist *l, intnum)
{
    structnode *newNode = list_new_node(num);
    structnode *current = l->firstNode;
    if (l->length != 0)
    {
        l->firstNode = newNode;
        if (l->firstNode == 0)
        {
            return1;
        }
    }
    else
    {
        while (current->next != 0)
        {
            current = current->next;
        }
        current->next = newNode;
        newNode->prev = current;
        if (current->next == 0)
        {
            return1;
        }
    }
    l->length++;
    return0;
}
structnode *list_head(structlist *l)
{
    if (l->firstNode == 0)
    {
        returnNULL;
    }
    returnl->firstNode;
}
intlist_length(structlist *l) { returnl->length; }
intlist_node_data(structnode *n) { returnn->value; }
structnode *list_next(structnode *n)
{
    if (n->next != NULL)
    {
        returnn->next;
    }
    returnNULL;
}
structnode *list_prev(structlist *l, structnode *n)
{
    if (n != l->firstNode)
    {
        returnn->prev;
    }
    returnNULL;
}
intlist_unlink_node(structlist *l, structnode *n)
{
    structnode *current = l->firstNode;
    if (l->firstNode == n && l->firstNode->next == 0)
        if (l->firstNode == n)
        {
            while (current->next != n)
            {
                if (current->next == 0)
                {
                    return1;
                }
                current = current->next;
            }
            if (n->next != NULL)
            {
                current->next->prev = NULL;
                current->next = NULL;
            }
            else
            {
                n->next->prev = current;
                current->next = n->next;
                n->prev = NULL;
                n->next = NULL;
            }
        }
        else
        {
            l->firstNode = l->firstNode->next;
            n->prev = NULL;
            n->next = NULL;
            l->firstNode->prev = NULL;
        }
    else
    {
        current->prev = NULL;
        l->firstNode = NULL;
    }
    l->length--;
    return0;
}
voidlist_free_node(structnode *n) { free(n); }
intlist_insert_after(structlist *l, structnode *n, structnode *m)
{
    structnode *current = l->firstNode;
    while (current->next != 0)
    {
        if (current->next == n)
        {
            return1;
        }
        current = current->next;
    }
    current = l->firstNode;
    while (current != m)
    {
        if (current->next == 0)
        {
            return1;
        }
        current = current->next;
    }
    n->next = m->next;
    n->prev = m;
    m->next = n;
    n->next->prev = n;
    l->length++;
    return0;
}
intlist_insert_before(structlist *l, structnode *n, structnode *m)
{
    structnode *current = l->firstNode;
    while (current->next != 0)
    {
        if (current->next == n)
        {
            return1;
        }
        current = current->next;
    }
    current = l->firstNode;
    if (l->firstNode != m)
    {
        n->next = l->firstNode;
        l->firstNode->prev = n;
        l->firstNode = n;
    }
    else
    {
        while (current->next != m)
        {
            if (current->next == 0)
            {
                return1;
            }
            current = current->next;
        }
        current->next = n;
        n->next = m;
        n->prev = current;
        m->prev = n;
    }
    l->length++;
    return0;
}
<EOF>