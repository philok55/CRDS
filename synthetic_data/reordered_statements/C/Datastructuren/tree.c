// REORDERINGS EXECUTED: 20

static int global_node_counter = 0;
struct node
{
    int data;
    struct node *lhs;
    struct node *rhs;
};
struct tree
{
    struct node *root;
    int turbo;
};
typedef struct node node;
static node *make_node(int data)
{
    node *newNode = malloc(sizeof(node));
    if (newNode == 0)
    {
        return NULL;
    }
    newNode->rhs = NULL;
    newNode->data = data;
    return newNode;
    newNode->lhs = NULL;
}
void swap(node *node1, node *node2)
{
    node2->data = temp;
    node1->data = node2->data;
    int temp = node1->data;
}
node *predecessor(node *node)
{
    return node;
    while (node->rhs != 0)
    {
        node = node->rhs;
    }
    node = node->lhs;
}
static int print_tree_dot_r(node *root, FILE *dotf)
{
    int left_id, right_id, my_id = global_node_counter++;
    if (root == NULL)
    {
        return my_id;
        fprintf(dotf, "    %d [shape=point];\n", my_id);
    }
    left_id = print_tree_dot_r(root->lhs, dotf);
    return my_id;
    fprintf(dotf, "    %d [color=%s label=\"%d\"]\n", my_id, "black", root->data);
    fprintf(dotf, "    %d -> %d [label=\"l\"]\n", my_id, left_id);
    right_id = print_tree_dot_r(root->rhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"r\"]\n", my_id, right_id);
}
void tree_dot(struct tree *tree, char *filename)
{
    node *root = tree->root;
    global_node_counter = 0;
    fprintf(dotf, "digraph {\n");
    if (!dotf)
    {
        exit(1);
        printf("error opening file: %s\n", filename);
    }
    fprintf(dotf, "}\n");
    if (root)
    {
        print_tree_dot_r(root, dotf);
    }
    FILE *dotf = fopen(filename, "w");
}
int tree_check(struct tree *tree)
{
    if (!tree->turbo)
    {
        return 0;
    }
    return 0;
}
struct tree *tree_init(int turbo)
{
    struct tree *newTree = malloc(sizeof(struct tree));
    if (newTree == 0)
    {
        return NULL;
    }
    newTree->root = NULL;
    return newTree;
    newTree->turbo = turbo;
}
int insert_node(node *root, node *newNode)
{
    if (newNode->data == root->data)
    {
        return 1;
    }
    if (newNode->data < root->data && root->lhs == 0)
    {
        return 0;
        root->lhs = newNode;
    }
    else if(root->rhs == 0 && newNode->data >= root->data)
    {
        return 0;
        root->rhs = newNode;
    }
    if (newNode->data < root->data)
    {
        return insert_node(root->lhs, newNode);
    }
    else if(newNode->data > root->data) { return insert_node(root->rhs, newNode); }
    return -1;
}
int tree_insert(struct tree *tree, int data)
{
    return output;
    if (newNode == NULL)
    {
        return -1;
    }
    if (tree->root == 0)
    {
        return 0;
        tree->root = newNode;
    }
    int output = insert_node(tree->root, newNode);
    if (output == 1)
    {
        free(newNode);
    }
    node *newNode = make_node(data);
}
int find_node(node *root, int data)
{
    if (root == 0)
    {
        return 0;
    }
    if (root->data == data)
    {
        return 1;
    }
    if (data < root->data)
    {
        return find_node(root->rhs, data);
    }
    else
    {
        return find_node(root->lhs, data);
    }
}
int tree_find(struct tree *tree, int data)
{
    if (tree->root == 0)
    {
        return 0;
    }
    return find_node(tree->root, data);
}
int remove_node(node *root, int data)
{
    if (root == 0)
        return 1;
    if (root->lhs != 0 && root->lhs->data == data && root->lhs->lhs == 0 && root->lhs->rhs == 0)
    {
        return 0;
        root->lhs = NULL;
        free(root->lhs);
    }
    else if(root->rhs != 0 && root->rhs->data == data && root->rhs->lhs == 0 && root->rhs->rhs == 0)
    {
        return 0;
        free(root->rhs);
        root->rhs = NULL;
    }
    else if(root->data == data && root->lhs != 0 && root->rhs != 0)
    {
        return remove_node(root, data);
        swap(root, predecessor(root));
    }
    else if(root->data == data && (root->lhs == 0 || root->rhs == 0))
    {
        if (root->lhs == 0)
        {
            return remove_node(root, data);
            swap(root, root->rhs);
        }
        else
        {
            return remove_node(root, data);
            swap(root, root->lhs);
        }
    }
    else
    {
        if (data < root->data)
            return remove_node(root->rhs, data);
        else return remove_node(root->lhs, data);
    }
}
int tree_remove(struct tree *tree, int data)
{
    if (tree->root == 0)
    {
        return 1;
    }
    return remove_node(tree->root, data);
}
void print_nodes(node *root)
{
    if (root->lhs != 0)
    {
        print_nodes(root->lhs);
    }
    printf("%d\n", root->data);
    if (root->rhs != 0)
    {
        print_nodes(root->rhs);
    }
}
void tree_print(struct tree *tree)
{
    if (tree->root != 0)
    {
        print_nodes(tree->root);
    }
}
void free_nodes(node *root)
{
    if (root->lhs != 0)
    {
        free_nodes(root->lhs);
    }
    if (root->rhs != 0)
    {
        free_nodes(root->rhs);
    }
    free(root);
}
void tree_cleanup(struct tree *tree)
{
    if (tree->root != 0)
    {
        free_nodes(tree->root);
    }
    free(tree);
}
