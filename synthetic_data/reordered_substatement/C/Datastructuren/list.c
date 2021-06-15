// REORDERINGS EXECUTED: 6

struct node
{
    int value;
    struct node *next;
    struct node *prev;
};
struct list
{
    struct node *firstNode;
    int length;
};
struct list *list_init()
{
    struct list *l = malloc(sizeof(struct list));
    if (l == 0)
    {
        return NULL;
    }
    l->firstNode = NULL;
    l->length = 0;
    return l;
}
int list_cleanup(struct list *l)
{
    struct node *current = l->firstNode;
    if (l->length != 0 && l->length != 1)
    {
        while (current->next != NULL)
        {
            current = current->next;
            list_free_node(current->prev);
        }
        list_free_node(current);
    }
    else if(l->length == 1) { list_free_node(l->firstNode); }
    free(l);
    return 0;
}
struct node *list_new_node(int num)
{
    struct node *newNode = malloc(sizeof(struct node));
    if (newNode == 0)
    {
        return NULL;
    }
    newNode->value = num;
    newNode->next = NULL;
    newNode->prev = NULL;
    return newNode;
}
int list_add(int num, struct list *l)
{
    struct node *newNode = list_new_node(num);
    if (l->length != 0)
    {
        l->firstNode->prev = newNode;
        newNode->next = l->firstNode;
        l->firstNode = newNode;
        if (l->firstNode->next == 0)
        {
            return 1;
        }
    }
    else
    {
        l->firstNode = newNode;
        if (l->firstNode == 0)
        {
            return 1;
        }
    }
    l->length++;
    return 0;
}
int list_add_back(int num, struct list *l)
{
    struct node *newNode = list_new_node(num);
    struct node *current = l->firstNode;
    if (l->length != 0)
    {
        while (current->next != 0)
        {
            current = current->next;
        }
        current->next = newNode;
        newNode->prev = current;
        if (current->next == 0)
        {
            return 1;
        }
    }
    else
    {
        l->firstNode = newNode;
        if (l->firstNode == 0)
        {
            return 1;
        }
    }
    l->length++;
    return 0;
}
struct node *list_head(struct list *l)
{
    if (l->firstNode == 0)
    {
        return NULL;
    }
    return l->firstNode;
}
int list_length(struct list *l) { return l->length; }
int list_node_data(struct node *n) { return n->value; }
struct node *list_next(struct node *n)
{
    if (n->next != NULL)
    {
        return n->next;
    }
    return NULL;
}
struct node *list_prev(struct node *n, struct list *l)
{
    if (n != l->firstNode)
    {
        return n->prev;
    }
    return NULL;
}
intlist_unlink_node(struct node *n, struct list *l)
{
    struct node *current = l->firstNode;
    if (l->firstNode == n && l->firstNode->next == 0)
    {
        current->prev = NULL;
        l->firstNode = NULL;
    }
    else if(l->firstNode == n)
    {
        l->firstNode = l->firstNode->next;
        n->prev = NULL;
        n->next = NULL;
        l->firstNode->prev = NULL;
    }
    else
    {
        while (current->next != n)
        {
            if (current->next == 0)
            {
                return 1;
            }
            current = current->next;
        }
        if (n->next != NULL)
        {
            n->next->prev = current;
            current->next = n->next;
            n->prev = NULL;
            n->next = NULL;
        }
        else
        {
            current->next->prev = NULL;
            current->next = NULL;
        }
    }
    l->length--;
    return 0;
}
void list_free_node(struct node *n) { free(n); }
int list_insert_after(struct node *n, struct node *m, struct list *l)
{
    struct node *current = l->firstNode;
    while (current->next != 0)
    {
        if (current->next == n)
        {
            return 1;
        }
        current = current->next;
    }
    current = l->firstNode;
    while (current != m)
    {
        if (current->next == 0)
        {
            return 1;
        }
        current = current->next;
    }
    n->next = m->next;
    n->prev = m;
    m->next = n;
    n->next->prev = n;
    l->length++;
    return 0;
}
int list_insert_before(struct node *m, struct list *l, struct node *n)
{
    struct node *current = l->firstNode;
    while (current->next != 0)
    {
        if (current->next == n)
        {
            return 1;
        }
        current = current->next;
    }
    current = l->firstNode;
    if (l->firstNode != m)
    {
        while (current->next != m)
        {
            if (current->next == 0)
            {
                return 1;
            }
            current = current->next;
        }
        current->next = n;
        n->next = m;
        n->prev = current;
        m->prev = n;
    }
    else
    {
        n->next = l->firstNode;
        l->firstNode->prev = n;
        l->firstNode = n;
    }
    l->length++;
    return 0;
}
