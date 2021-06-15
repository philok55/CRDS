/* Author: Philo Decroos
 * UvA-Net-ID: 11752262
 *
 * set.c:
 * This is the implementation of the abstract set datastructure. The functions
 * of this datastructure are used to control a binary search tree, and are
 * mostly calls to the funtions of the tree datastructure.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "set.h"
#include "tree.h"

/* The set structure contains a binary search tree. */
struct set {
    struct tree* tree;
};

/* This function initialises a set, by allocating memory for it and calling
 * the tree_init function to initialise the tree.
 */
struct set *set_init(int turbo) {
    struct set* newSet = malloc(sizeof (struct set));

    if (newSet == 0) {
        return NULL;
    }

    newSet->tree = tree_init(turbo);
    return newSet;
}

/* This function calls the tree_insert function to insert something in the
 * set.
 */
int set_insert(struct set *s, int num) {
    return tree_insert(s->tree, num);
}

/* This function calls the tree_find function to find a node in the set. */
int set_find(struct set *s, int num) {
    return tree_find(s->tree, num);
}

/* This function calls the tree_remove function to remove a node from the set.
 */
int set_remove(struct set *s, int num) {
    return tree_remove(s->tree, num);
}

/* This function calls the tree_cleanup function to clean up the sets tree,
 * and then frees the set itself.
 */
void set_cleanup(struct set *s) {
    tree_cleanup(s->tree);
    free(s);
}

/* This function calls the tree_print function to print the set in order. */
void set_print(struct set *s) {
    tree_print(s->tree);
}

/* This function calls the tree_check function to check the tree for balance.
 */
int set_verify(struct set *s) {
    return tree_check(s->tree);
}
