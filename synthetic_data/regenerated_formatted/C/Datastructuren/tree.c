struct tree
{
    struct node *root;
    int turbo;
};
struct node
{
    int data;
    struct node *lhs;
    struct node *rhs;
};
typedef struct node node;
static int global_node_counter = 0;
static node *make_node(int data)
{
    node *newNode = malloc(sizeof(node));
    if (newNode == 0)
    {
        return NULL;
    }
    newNode->data = data;
    newNode->lhs = NULL;
    newNode->rhs = NULL;
    return newNode;
}
void swap(node *node1, node *node2)
{
    int temp = node1->data;
    node1->data = node2->data;
    node2->data = temp;
}
node *predecessor(node *node)
{
    node = node->lhs;
    while (node->rhs != 0)
    {
        node = node->rhs;
    }
    return node;
}
static int print_tree_dot_r(node *root, FILE *dotf)
{
    int left_id, right_id, my_id = global_node_counter++;
    if (root == NULL)
    {
        fprintf(dotf, "    %d [shape=point];\n", my_id);
        return my_id;
    }
    fprintf(dotf, "    %d [color=%s label=\"%d\"]\n", my_id, "black", root->data);
    left_id = print_tree_dot_r(root->lhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"l\"]\n", my_id, left_id);
    right_id = print_tree_dot_r(root->rhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"r\"]\n", my_id, right_id);
    return my_id;
}
void tree_dot(struct tree *tree, char *filename)
{
    node *root = tree->root;
    global_node_counter = 0;
    FILE *dotf = fopen(filename, "w");
    if (!dotf)
    {
        printf("error opening file: %s\n", filename);
        exit(1);
    }
    fprintf(dotf, "digraph {\n");
    if (root)
    {
        print_tree_dot_r(root, dotf);
    }
    fprintf(dotf, "}\n");
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
    newTree->turbo = turbo;
    return newTree;
}
int insert_node(node *root, node *newNode)
{
    if (newNode->data == root->data)
    {
        return 1;
    }
    if (newNode->data < root->data && root->lhs == 0)
    {
        root->lhs = newNode;
        return 0;
    }
    else if(root->rhs == 0 && newNode->data >= root->data)
    {
        root->rhs = newNode;
        return 0;
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
    node *newNode = make_node(data);
    if (newNode == NULL)
    {
        return -1;
    }
    if (tree->root == 0)
    {
        tree->root = newNode;
        return 0;
    }
    int output = insert_node(tree->root, newNode);
    if (output == 1)
    {
        free(newNode);
    }
    return output;
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
        return find_node(root->lhs, data);
    }
    else
    {
        return find_node(root->rhs, data);
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
        free(root->lhs);
        root->lhs = NULL;
        return 0;
    }
    else if(root->rhs != 0 && root->rhs->data == data && root->rhs->lhs == 0 && root->rhs->rhs == 0)
    {
        free(root->rhs);
        root->rhs = NULL;
        return 0;
    }
    else if(root->data == data && root->lhs != 0 && root->rhs != 0)
    {
        swap(root, predecessor(root));
        return remove_node(root, data);
    }
    else if(root->data == data && (root->lhs == 0 || root->rhs == 0))
    {
        if (root->lhs == 0)
        {
            swap(root, root->rhs);
            return remove_node(root, data);
        }
        else
        {
            swap(root, root->lhs);
            return remove_node(root, data);
        }
    }
    else
    {
        if (data < root->data)
            return remove_node(root->lhs, data);
        else return remove_node(root->rhs, data);
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
