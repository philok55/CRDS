/* Author: Philo Decroos
 * UvA-Net-ID: 11752262
 *
 * heap.c:
 * This program is a min-heap data structure, that we will use as a priority
 * queue. The heap consists of a dynamic array, sorted by a generic compare
 * function. It inserts and removes following the algorithms for a min-heap.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "array.h"
#include "prioq.h"

#define ARRAY_INITIAL_SIZE 10

/* The heap_init function initiates a heap, checks the malloc and passes
 * the compare function to the heap struct.
 */
static
struct heap* heap_init(int (*compare)(const void*, const void*)) {
    struct heap* h = malloc(sizeof(struct heap));
    h->array = array_init(ARRAY_INITIAL_SIZE);

    if (h->array == 0) {
        return NULL;
    }

    h->compare = compare;

    return h;
}

/* This function does the same as the heap_init function. */
struct heap* prioq_init(int (*compare)(const void*, const void*)) {
    return heap_init(compare);
}

/* This function returns the amount of elements in the heap. */
long int prioq_size(struct heap* h) {
    return array_size(h->array);
}

/* This function frees the memory that was allocated, by using a generic
 * freeing function. If this function is not specified it just frees the heap.
 */
static
int heap_cleanup(struct heap* h, void free_func(void*)) {
    if (free_func == NULL) {
        free_func = free;
    }

    array_cleanup(h->array, free_func);
    free(h);

    return 0;
}

/* This function redirects to heap_cleanup. */
int prioq_cleanup(prioq* h, void free_func(void*)) {
    return heap_cleanup(h, free_func);
}

/* This function is used whenever we want to swap two elements in the heap. */
void swap(struct heap* h, int index1, int index2) {
    void* temp = array_get(h->array, index1);
    array_set(h->array, index1, array_get(h->array, index2));
    array_set(h->array, index2, temp);
}

/* This function inserts an element into the heap, and makes sure
 * the heap properties are contained by swapping the inserted element
 * with its parent if it is smaller.
 */
static
int heap_insert(struct heap* h, void* p) {
    if (array_append(h->array, p) == -1) {
        return 1;
    }

    if (array_size(h->array) == 1) {
        return 0;
    }

    int i = (int)array_size(h->array) - 1;

    while (i > 0 && h->compare(array_get(h->array, i), array_get(h->array,
           (int)floor((i - 1) / 2))) <= 0) {

        swap(h, i, (int)floor((i - 1) / 2));
        i = (int)floor((i - 1) / 2);
    }

    return 0;
}

/* This function redirects to heap_insert. */
int prioq_insert(prioq* h, void* p) {
    return heap_insert(h, p);
}

/* This function is used to restore the heap properties after we have removed
 * the smallest element. To do this we have to keep comparing the top element
 * to both its children and swap it with its smallest child if it is smaller.
 */
void restore(struct heap* h) {
    int i = 0;

    while ((array_get(h->array, i * 2 + 1) != 0 &&
            (h->compare(array_get(h->array, i),
                        array_get(h->array, i * 2 +1)) >= 0))
           ||
           (array_get(h->array, i * 2 + 2) != 0 &&
           (h->compare(array_get(h->array, i),
                       array_get(h->array, i * 2 + 2)) >= 0))) {

        if ((array_get(h->array, i * 2 + 1) != 0 &&
            array_get(h->array, i * 2 + 2) != 0) &&
            h->compare(array_get(h->array, i * 2 + 1),
            array_get(h->array, i * 2 + 2)) <= 0) {

            swap(h, i, i * 2 + 1);
            i = i * 2 + 1;
        }

        else if (array_get(h->array, i * 2 + 2) != 0) {
            swap(h, i, i * 2 + 2);
            i = i * 2 + 2;
        }

        else {
            swap(h, i, i * 2 + 1);
            i = i * 2 + 1;
        }
    }
}

/* This function removes and returns the smallest (top) element of the heap by
 * swapping it with the last element of the array, removing it and restoring
 * the heap by calling the restore function.
 */
static
void* heap_pop(struct heap* h) {
    if (array_size(h->array) == 0) {
        return NULL;
    }

    if (array_size(h->array) == 1) {
        return array_pop(h->array);
    }

    int j = (int)prioq_size(h) - 1;
    swap(h, 0, j);

    void* output = array_pop(h->array);

    restore(h);
    return output;
}

/* This function redirects to the heap_pop function. */
void* prioq_pop(prioq* h) {
    return heap_pop(h);
}
