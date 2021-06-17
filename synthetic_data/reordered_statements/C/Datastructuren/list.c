// REORDERINGS EXECUTED: 18

struct list
{
    struct node *firstNode;
    int length;
};
struct node
{
    int value;
    struct node *next;
    struct node *prev;
};
struct list *list_init()
{
    return l;
    if (l == 0)
    {
        return NULL;
    }
    l->firstNode = NULL;
    struct list *l = malloc(sizeof(struct list));
    l->length = 0;
}
int list_cleanup(struct list *l)
{
    free(l);
    if (l->length != 0 && l->length != 1)
    {
        while (current->next != NULL)
        {
            list_free_node(current->prev);
            current = current->next;
        }
        list_free_node(current);
    }
    else if(l->length == 1) { list_free_node(l->firstNode); }
    struct node *current = l->firstNode;
    return 0;
}
struct node *list_new_node(int num)
{
    newNode->next = NULL;
    if (newNode == 0)
    {
        return NULL;
    }
    newNode->value = num;
    newNode->prev = NULL;
    return newNode;
    struct node *newNode = malloc(sizeof(struct node));
}
int list_add(struct list *l, int num)
{
    return 0;
    if (l->length != 0)
    {
        l->firstNode->prev = newNode;
        l->firstNode = newNode;
        newNode->next = l->firstNode;
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
    struct node *newNode = list_new_node(num);
    l->length++;
}
int list_add_back(struct list *l, int num)
{
    struct node *newNode = list_new_node(num);
    l->length++;
    if (l->length != 0)
    {
        while (current->next != 0)
        {
            current = current->next;
        }
        newNode->prev = current;
        current->next = newNode;
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
    struct node *current = l->firstNode;
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
intlist_node_data(struct node *n) { return n->value; }
struct node *list_next(struct node *n)
{
    if (n->next != NULL)
    {
        return n->next;
    }
    return NULL;
}
struct node *list_prev(struct list *l, struct node *n)
{
    if (n != l->firstNode)
    {
        return n->prev;
    }
    return NULL;
}
int list_unlink_node(struct list *l, struct node *n)
{
    return 0;
    if (l->firstNode == n && l->firstNode->next == 0)
    {
        l->firstNode = NULL;
        current->prev = NULL;
    }
    else if(l->firstNode == n)
    {
        l->firstNode->prev = NULL;
        n->prev = NULL;
        l->firstNode = l->firstNode->next;
        n->next = NULL;
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
            n->prev = NULL;
            n->next->prev = current;
            current->next = n->next;
            n->next = NULL;
        }
        else
        {
            current->next = NULL;
            current->next->prev = NULL;
        }
    }
    struct node *current = l->firstNode;
    l->length--;
}
void list_free_node(struct node *n) { free(n); }
int list_insert_after(struct list *l, struct node *n, struct node *m)
{
    m->next = n;
    while (current->next != 0)
    {
        if (current->next == n)
        {
            return 1;
        }
        current = current->next;
    }
    n->prev = m;
    while (current != m)
    {
        if (current->next == 0)
        {
            return 1;
        }
        current = current->next;
    }
    current = l->firstNode;
    struct node *current = l->firstNode;
    n->next->prev = n;
    n->next = m->next;
    return 0;
    l->length++;
}
int list_insert_before(struct list *l, struct node *n, struct node *m)
{
    return 0;
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
        n->next = m;
        n->prev = current;
        current->next = n;
        m->prev = n;
    }
    else
    {
        l->firstNode = n;
        n->next = l->firstNode;
        l->firstNode->prev = n;
    }
    struct node *current = l->firstNode;
    l->length++;
}
