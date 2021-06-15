/* Author: Philo Decroos
 * UvA-Net-ID: 11752262
 *
 * list.c:
 * This program is the implementation of the doubly linked list datastructure.
 * This list will be used for the insertion sort. We have different functions
 * to execute different operations on the list.
 */

#include <stdio.h>
#include <stdlib.h>

#include "list.h"

/* The node structure is a node in the list, and has a value, a pointer to
 * the next node and a pointer to the previous node.
 */
struct node {
    int value;
    struct node* next;
    struct node* prev;
};

/* This structure is the actual list, that has a pointer to the first node
 * of the list and a variable that holds the length of the list.
 */
struct list {
    struct node* firstNode;
    int length;
};

/* This function allocates memory for the list and sets the pointer and
 * length value. It returns NULL if the allocation fails.
 */
struct list* list_init() {
    struct list* l = malloc(sizeof(struct list));

    if (l == 0) {
        return NULL;
    }

    l->firstNode = NULL;
    l->length = 0;

    return l;
}

/* This function cleans the list by first freeing every node and then
 * freeing the list structure.
 */
int list_cleanup(struct list* l) {
    struct node* current = l->firstNode;

    if (l->length != 0 && l->length != 1) {
        while (current->next != NULL) {
            current = current->next;
            list_free_node(current->prev);
        }

        list_free_node(current);
    }

    else if (l->length == 1) {
        list_free_node(l->firstNode);
    }

    free(l);

    return 0;
}

/* This function creates a new node to put in the list. */
struct node* list_new_node(int num) {
    struct node* newNode = malloc(sizeof(struct node));

    if (newNode == 0) {
        return NULL;
    }

    newNode->value = num;
    newNode->next = NULL;
    newNode->prev = NULL;

    return newNode;
}

/* This function creates a new node with value num, and adds it
 * to the front of the list.
 */
int list_add(struct list* l, int num) {
    struct node* newNode = list_new_node(num);

    if (l->length != 0) {
        l->firstNode->prev = newNode;
        newNode->next = l->firstNode;
        l->firstNode = newNode;

        if (l->firstNode->next == 0) {
            return 1;
        }
    }

    else {
        l->firstNode = newNode;

        if (l->firstNode == 0) {
            return 1;
        }
    }

    l->length++;

    return 0;
}

/* This function creates a new node for the list and adds it to
 * the back.
 */
int list_add_back(struct list* l, int num) {
    struct node* newNode = list_new_node(num);
    struct node* current = l->firstNode;

    if (l->length != 0) {
        while (current->next != 0) {
            current = current->next;
        }

        current->next = newNode;
        newNode->prev = current;

        if (current->next == 0) {
            return 1;
        }
    }

    else {
        l->firstNode = newNode;

        if (l->firstNode == 0) {
            return 1;
        }
    }

    l->length++;

    return 0;
}

/* This function returns a pointer to the first element of
 * the list.
 */
struct node* list_head(struct list* l) {
    if (l->firstNode == 0) {
        return NULL;
    }

    return l->firstNode;
}

/* This function returns the length of the list. */
int list_length(struct list* l) {
    return l->length;
}

/* This function returns the value of a given node. */
int list_node_data(struct node* n) {
    return n->value;
}

/* This function returns the next-pointer of a given node. */
struct node* list_next(struct node* n) {
    if (n->next != NULL) {
        return n->next;
    }

    return NULL;
}
 /* This function returns the pointer to the previous node. */
struct node* list_prev(struct list* l, struct node* n) {
    if (n != l->firstNode) {
        return n->prev;
    }

    return NULL;
}

/* This function unlinks a node from the list and returns it. */
int list_unlink_node(struct list* l, struct node* n) {
    struct node* current = l->firstNode;

    if (l->firstNode == n && l->firstNode->next == 0) {
        current->prev = NULL;
        l->firstNode = NULL;
    }

    else if (l->firstNode == n) {
        l->firstNode = l->firstNode->next;
        n->prev = NULL;
        n->next = NULL;
        l->firstNode->prev = NULL;
    }

    else {
        while (current->next != n) {
            if (current->next == 0) {
                return 1;
            }

            current = current->next;
        }

        if (n->next != NULL) {
            n->next->prev = current;
            current->next = n->next;
            n->prev = NULL;
            n->next = NULL;
        }

        else {
            current->next->prev = NULL;
            current->next = NULL;
        }
    }

    l->length--;

    return 0;
}

/* This function frees the memory that was allocated for a node. */
void list_free_node(struct node* n) {
    free(n);
}

/* This function inserts a node after another given node. */
int list_insert_after(struct list* l, struct node* n, struct node* m) {
    struct node* current = l->firstNode;

    while (current->next != 0) {
        if (current->next == n) {
            return 1;
        }

        current = current->next;
    }

    current = l->firstNode;

    while (current != m) {
        if (current->next == 0) {
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

/* This function inserts a node before another given node. */
int list_insert_before(struct list* l, struct node* n, struct node* m) {
    struct node* current = l->firstNode;

    while (current->next != 0) {
        if (current->next == n) {
            return 1;
        }

        current = current->next;
    }

    current = l->firstNode;

    if (l->firstNode != m) {
        while (current->next != m) {
            if (current->next == 0) {
                return 1;
            }

            current = current->next;
        }

        current->next = n;
        n->next = m;
        n->prev = current;
        m->prev = n;
    }

    else {
        n->next = l->firstNode;
        l->firstNode->prev = n;
        l->firstNode = n;
    }

    l->length++;

    return 0;
}
