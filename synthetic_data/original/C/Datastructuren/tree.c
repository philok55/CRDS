/* Author: Philo Decroos
 * UvA-Net-ID: 11752262
 *
 * tree.c:
 * This program is the implementation of a binary search tree. It sorts its
 * input by making every left child smaller than its parents, and every right
 * child greater than its parent. We have functions to insert or delete nodes
 * from the tree, find a node, and print the tree. Most functions have helper
 * functions to be able to traverse the tree recursively.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "tree.h"

/* This is the structure we use for the tree: it has a root and a
 * "turbo" option that will be set if we want the tree to balance itself.
 */
struct tree {
    struct node* root;
    int turbo;
};

/* This struct is a node in the tree. */
struct node {
    int data;
    struct node* lhs;
    struct node* rhs;
};

typedef struct node node;

/* Unique id's for numbering nodes in dot format. */
static int global_node_counter = 0;

/* This is a helper function: it allocates a new tree node and initialises
 * it with the given parameters. It returns a pointer to the new node or
 * NULL on failure.
 */
static node* make_node(int data) {
    node* newNode = malloc(sizeof (node));

    if (newNode == 0) {
        return NULL;
    }

    newNode->data = data;
    newNode->lhs = NULL;
    newNode->rhs = NULL;

    return newNode;
}

/* This function is used to swap two nodes in a tree. */
void swap(node* node1, node* node2) {
    int temp = node1->data;
    node1->data = node2->data;
    node2->data = temp;
}

/* This function finds the predecessor of a node in the tree. */
node* predecessor(node* node) {
    node = node->lhs;

    while (node->rhs != 0) {
        node = node->rhs;
    }

    return node;
}

/* This function prints the code that will be put in the .dot-file, which will
 * then be used to create a pdf that displays the tree.
 */
static int print_tree_dot_r(node* root, FILE* dotf) {
    int left_id, right_id, my_id = global_node_counter++;

    if (root == NULL) {
        fprintf(dotf, "    %d [shape=point];\n", my_id);
        return my_id;
    }

    fprintf(dotf, "    %d [color=%s label=\"%d\"]\n",
            my_id, "black", root->data);

    left_id = print_tree_dot_r(root->lhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"l\"]\n", my_id, left_id);

    right_id = print_tree_dot_r(root->rhs, dotf);
    fprintf(dotf, "    %d -> %d [label=\"r\"]\n", my_id, right_id);

    return my_id;
}

/* This function creates a .dot-file and then calls the print_tree_dot_r
 * function to display a tree in pdf format.
 */
void tree_dot(struct tree* tree, char* filename) {
    node* root = tree->root;
    global_node_counter = 0;
    FILE* dotf = fopen(filename, "w");
    if (!dotf) {
        printf("error opening file: %s\n", filename);
        exit(1);
    }

    fprintf(dotf, "digraph {\n");
    if (root) {
        print_tree_dot_r(root, dotf);
    }

    fprintf(dotf, "}\n");
}

/* If the turbo option is set, this function can check if the tree is
 * balanced.
 */
int tree_check(struct tree* tree) {
    if (!tree->turbo) {
        return 0;
    }

    return 0;
}

/* This function initialises a tree by allocating memory for it, and sets
 * the variables of the tree struct to default.
 */
struct tree* tree_init(int turbo) {
    struct tree* newTree = malloc(sizeof (struct tree));

    if (newTree == 0) {
        return NULL;
    }

    newTree->root = NULL;
    newTree->turbo = turbo;
    return newTree;
}

/* This function is used to recursively traverse the tree and insert the given
 * node in the correct place.
 */
int insert_node(node* root, node* newNode) {
    if (newNode->data == root->data) {
        return 1;
    }

    if (newNode->data < root->data && root->lhs == 0) {
        root->lhs = newNode;
        return 0;
    }

    else if (root->rhs == 0 && newNode->data >= root->data) {
        root->rhs = newNode;
        return 0;
    }

    if (newNode->data < root->data) {
        return insert_node(root->lhs, newNode);
    }

    else if (newNode->data > root->data){
        return insert_node(root->rhs, newNode);
    }

    return -1;
}

/* This function makes the new node that needs to be inserted and then calls
 * the insert_node function to insert this node into the tree.
 */
int tree_insert(struct tree* tree, int data) {
    node* newNode = make_node(data);

    if (newNode == NULL) {
        return -1;
    }

    if (tree->root == 0) {
        tree->root = newNode;
        return 0;
    }

    int output = insert_node(tree->root, newNode);

    if (output == 1) {
        free(newNode);
    }

    return output;
}

/* This function is used to recursively traverse the tree to find a node.
 * If it is found, it returns 1, and 0 otherwise.
 */
int find_node(node* root, int data) {
    if (root == 0) {
        return 0;
    }

    if (root->data == data) {
        return 1;
    }

    if (data < root->data) {
        return find_node(root->lhs, data);
    }

    else {
        return find_node(root->rhs, data);
    }
}

/* This function calls the recursive find_node function and returns its return
 * value.
 */
int tree_find(struct tree* tree, int data) {
    if (tree->root == 0) {
        return 0;
    }

    return find_node(tree->root, data);
}

/* This function is used to recursively traverse the tree and remove the given
 * node from the tree. If it is not in there, it will return 1, and 0 if it
 * is succesfully removed.
 */
int remove_node(node* root, int data) {
    if (root == 0)
        return 1;

    if (root->lhs != 0 && root->lhs->data == data
                       && root->lhs->lhs == 0
                       && root->lhs->rhs == 0) {
        free(root->lhs);
        root->lhs = NULL;
        return 0;
    }

    else if (root->rhs != 0 && root->rhs->data == data
                            && root->rhs->lhs == 0
                            && root->rhs->rhs == 0) {
        free(root->rhs);
        root->rhs = NULL;
        return 0;
    }

    /* If the node that needs removal has two children, we need to swap it
     * with its predecessor and then remove it.
     */
    else if (root->data == data && root->lhs != 0 && root->rhs != 0) {
        swap(root, predecessor(root));
        return remove_node(root, data);
    }

    /* If the node that needs removal has 1 child, we need to swap it with its
     * child and then remove it.
     */
    else if (root->data == data && (root->lhs == 0 || root->rhs == 0)) {
        if (root->lhs == 0) {
            swap(root, root->rhs);
            return remove_node(root, data);
        }

        else {
            swap(root, root->lhs);
            return remove_node(root, data);
        }
    }

    else {
        if (data < root->data)
            return remove_node(root->lhs, data);

        else
            return remove_node(root->rhs, data);
    }
}

/* The remove function calls the recursive removal function and returns its
 * return value.
 */
int tree_remove(struct tree *tree, int data) {
    if (tree->root == 0) {
        return 1;
    }

    return remove_node(tree->root, data);
}

/* This function takes care of the in-order traversal of the tree to print
 * the entire tree in order.
 */
void print_nodes(node* root) {
    if (root->lhs != 0) {
        print_nodes(root->lhs);
    }

    printf("%d\n", root->data);

    if (root->rhs != 0) {
        print_nodes(root->rhs);
    }
}

/* This funtion calls the print_nodes function to print the tree. */
void tree_print(struct tree *tree) {
    if (tree->root != 0) {
        print_nodes(tree->root);
    }
}

/* This funtion traverses the tree and frees every node. */
void free_nodes(node* root) {
    if (root->lhs != 0) {
        free_nodes(root->lhs);
    }

    if (root->rhs != 0) {
        free_nodes(root->rhs);
    }

    free(root);
}

/* This function calls the free_nodes function to free all the nodes in the
 * tree, and then frees the tree itself.
 */
void tree_cleanup(struct tree *tree) {
    if (tree->root != 0) {
        free_nodes(tree->root);
    }

    free(tree);
}
