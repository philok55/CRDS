// REORDERINGS EXECUTED: 36

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
void swap(node *node2, node *node1)
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
static int print_tree_dot_r(FILE *dotf, node *root)
{
    int left_id, right_id, my_id = global_node_counter++;
    if (root == NULL)
    {
        fprintf("    %d [shape=point];\n", my_id, dotf);
        return my_id;
    }
    fprintf(dotf, my_id, root->data, "black", "    %d [color=%s label=\"%d\"]\n");
    left_id = print_tree_dot_r(dotf, root->lhs);
    fprintf(my_id, dotf, left_id, "    %d -> %d [label=\"l\"]\n");
    right_id = print_tree_dot_r(dotf, root->rhs);
    fprintf(right_id, my_id, dotf, "    %d -> %d [label=\"r\"]\n");
    return my_id;
}
void tree_dot(char *filename, struct tree *tree)
{
    node *root = tree->root;
    global_node_counter = 0;
    FILE *dotf = fopen("w", filename);
    if (!dotf)
    {
        printf(filename, "error opening file: %s\n");
        exit(1);
    }
    fprintf("digraph {\n", dotf);
    if (root)
    {
        print_tree_dot_r(dotf, root);
    }
    fprintf("}\n", dotf);
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
int insert_node(node *newNode, node *root)
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
        return insert_node(newNode, root->lhs);
    }
    else if(newNode->data > root->data) { return insert_node(newNode, root->rhs); }
    return -1;
}
int tree_insert(int data, struct tree *tree)
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
    int output = insert_node(newNode, tree->root);
    if (output == 1)
    {
        free(newNode);
    }
    return output;
}
int find_node(int data, node *root)
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
        return find_node(data, root->lhs);
    }
    else
    {
        return find_node(data, root->rhs);
    }
}
int tree_find(int data, struct tree *tree)
{
    if (tree->root == 0)
    {
        return 0;
    }
    return find_node(data, tree->root);
}
int remove_node(int data, node *root)
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
        swap(predecessor(root), root);
        return remove_node(data, root);
    }
    else if(root->data == data && (root->lhs == 0 || root->rhs == 0))
    {
        if (root->lhs == 0)
        {
            swap(root->rhs, root);
            return remove_node(data, root);
        }
        else
        {
            swap(root->lhs, root);
            return remove_node(data, root);
        }
    }
    else
    {
        if (data < root->data)
            return remove_node(data, root->lhs);
        else return remove_node(data, root->rhs);
    }
}
int tree_remove(int data, struct tree *tree)
{
    if (tree->root == 0)
    {
        return 1;
    }
    return remove_node(data, tree->root);
}
void print_nodes(node *root)
{
    if (root->lhs != 0)
    {
        print_nodes(root->lhs);
    }
    printf(root->data, "%d\n");
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
