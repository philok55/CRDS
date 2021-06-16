// REORDERINGS EXECUTED: 9

structtree
{
    structnode *root;
    intturbo;
};
structnode
{
    intdata;
    structnode *lhs;
    structnode *rhs;
};
typedefstructnodenode;
staticintglobal_node_counter = 0;
staticnode *make_node(intdata)
{
    node *newNode = malloc(sizeof(node));
    if (newNode == 0)
    {
        returnNULL;
    }
    newNode->data = data;
    newNode->lhs = NULL;
    newNode->rhs = NULL;
    returnnewNode;
}
voidswap(node *node1, node *node2)
{
    inttemp = node1->data;
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
    returnnode;
}
staticintprint_tree_dot_r(node *root, FILE *dotf)
{
    intleft_id, right_id, my_id = global_node_counter++;
    if (root == NULL)
    {
        fprintf(dotf, "    %d [shape=point];\n", my_id);
        returnmy_id;
    }
    fprintf(dotf, "    %d [color=%s label=\"%d\"]\n", my_id, "black", root->data);
    left_id = print_tree_dot_r(root->lhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"l\"]\n", my_id, left_id);
    right_id = print_tree_dot_r(root->rhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"r\"]\n", my_id, right_id);
    returnmy_id;
}
voidtree_dot(structtree *tree, char *filename)
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
inttree_check(structtree *tree)
{
    if (!tree->turbo)
    {
        return0;
    }
    return0;
}
structtree *tree_init(intturbo)
{
    structtree *newTree = malloc(sizeof(structtree));
    if (newTree == 0)
    {
        returnNULL;
    }
    newTree->root = NULL;
    newTree->turbo = turbo;
    returnnewTree;
}
intinsert_node(node *root, node *newNode)
{
    if (newNode->data == root->data)
    {
        return1;
    }
    if (newNode->data < root->data && root->lhs == 0)
        if (root->rhs == 0 && newNode->data >= root->data)
        {
            root->rhs = newNode;
            return0;
        }
        else
        {
            root->lhs = newNode;
            return0;
        }
    if (newNode->data < root->data)
        if (newNode->data > root->data)
        {
            returninsert_node(root->rhs, newNode);
        }
        else
        {
            returninsert_node(root->lhs, newNode);
        }
    return -1;
}
inttree_insert(structtree *tree, intdata)
{
    node *newNode = make_node(data);
    if (newNode == NULL)
    {
        return -1;
    }
    if (tree->root == 0)
    {
        tree->root = newNode;
        return0;
    }
    intoutput = insert_node(tree->root, newNode);
    if (output == 1)
    {
        free(newNode);
    }
    returnoutput;
}
intfind_node(node *root, intdata)
{
    if (root == 0)
    {
        return0;
    }
    if (root->data == data)
    {
        return1;
    }
    if (data < root->data)
    {
        returnfind_node(root->rhs, data);
    }
    else
    {
        returnfind_node(root->lhs, data);
    }
}
inttree_find(structtree *tree, intdata)
{
    if (tree->root == 0)
    {
        return0;
    }
    returnfind_node(tree->root, data);
}
intremove_node(node *root, intdata)
{
    if (root == 0)
        return1;
    if (root->lhs != 0 && root->lhs->data == data && root->lhs->lhs == 0 && root->lhs->rhs == 0)
        if (root->rhs != 0 && root->rhs->data == data && root->rhs->lhs == 0 && root->rhs->rhs == 0)
            if (root->data == data && root->lhs != 0 && root->rhs != 0)
                if (root->data == data && (root->lhs == 0 || root->rhs == 0))
                {
                    if (data < root->data)
                        returnremove_node(root->rhs, data);
                    elsereturnremove_node(root->lhs, data);
                }
                else
                {
                    if (root->lhs == 0)
                    {
                        swap(root, root->lhs);
                        returnremove_node(root, data);
                    }
                    else
                    {
                        swap(root, root->rhs);
                        returnremove_node(root, data);
                    }
                }
            else
            {
                swap(root, predecessor(root));
                returnremove_node(root, data);
            }
        else
        {
            free(root->rhs);
            root->rhs = NULL;
            return0;
        }
    else
    {
        free(root->lhs);
        root->lhs = NULL;
        return0;
    }
}
inttree_remove(structtree *tree, intdata)
{
    if (tree->root == 0)
    {
        return1;
    }
    returnremove_node(tree->root, data);
}
voidprint_nodes(node *root)
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
voidtree_print(structtree *tree)
{
    if (tree->root != 0)
    {
        print_nodes(tree->root);
    }
}
voidfree_nodes(node *root)
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
voidtree_cleanup(structtree *tree)
{
    if (tree->root != 0)
    {
        free_nodes(tree->root);
    }
    free(tree);
}
<EOF>