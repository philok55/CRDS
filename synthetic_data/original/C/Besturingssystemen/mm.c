/* Author:      Philo Decroos
 * UvA-Net-ID:  11752262
 * BSc Informatica
 *
 * mm.c:
 * This file contains functions to allocate and free memory in a RAM
 * simulation. We get a certain amount of memory modules devided in banks from
 * the simulation. We have to keep metadata (a linked list) where we can keep
 * information about which parts of the memory are free. Then we have functions
 * to allocate memory of a given amount of bytes, and to free the memory
 * associated with a given pointer.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "myalloc.h"

/* The header struct is used to keep metadata
 * about every part of the memory.
 */
struct header {
    size_t size;
    bool is_free;
    struct header* next;
};

typedef struct header header_t;

struct mm_state {
    header_t* first_el;
    size_t last_activated;
};

/* Here we initialize the memory by activating the first bank and storing a
 * pointer there to the first header. We initialize the data in this header.
 */
mm_state_t* mm_initialize(void) {
    const struct ram_info *info = hw_raminfo();

    char *base = (char*)info->module_addrs[0];
    hw_activate(0, 0);

    mm_state_t* st = (mm_state_t*)base;
    st->last_activated = 0;
    st->first_el = (header_t*)((char*)st + sizeof(mm_state_t));
    st->first_el->is_free = true;
    st->first_el->size = (info->bank_size*info->nbanks_per_module)-sizeof(header_t)-sizeof(mm_state_t);
    st->first_el->next = NULL;

    return st;
}

/* This function is used to create a new header after allocating bytes in our
 * memory. It takes the header of the memory part that the bytes were allocated
 * in, and the amount of bytes that were allocated.
 */
void make_header(header_t* header, size_t nbytes) {
    void* p = (void*)(header + 1);
    if (header->next != NULL) {
        header_t* temp = header->next;
        header->next = (header_t*)((char*)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = temp;
    } else {
        header->next = (header_t*)((char*)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = NULL;
    }
}

/* This function is called to allocate memory for a given amount of bytes. We
 * try to fit in in memory by going through the linked list of headers and
 * finding a gap that is suited to store this amount of bytes. If needed we
 * activate extra banks and make a new header for the free block that remains.
 * Then we return a pointer to the start of the allocated memory.
 */
void *mm_alloc(mm_state_t* st, size_t nbytes) {
    const struct ram_info* info = hw_raminfo();
    while (nbytes % sizeof(intmax_t) != 0) {
        nbytes++;
    }

    header_t* header = st->first_el;
    while (!header->is_free || header->size < (nbytes + sizeof(header_t))) {
        if ((header = header->next) == NULL)
            return 0;
    }

    for (size_t i = curr_bank + 1; i <= end_bank; i++) {
        if (i > st->last_activated) {
            hw_activate(0, i);
            st->last_activated = i;
        }
    }

    size_t curr_bank = ((char*)header - (char*)info->module_addrs[0] + sizeof(header_t)) / info->bank_size;
    size_t end_bank = ((char*)header - (char*)info->module_addrs[0] + nbytes + sizeof(header_t)*2) / info->bank_size;
    if (info->nbanks_per_module <= end_bank) {
        return 0;
    }

    header->is_free = false;
    void* p = (void*)(header + 1);
    make_header(header, nbytes);
    header->size = (char*)header->next - (char*)p;
    return p;
}

/* This function is used to free the memory pointed to by the given pointer.
 * If the surrounding memory is also free, we have to merge headers in order
 * to prevent the header from filling up the memory.
 */
void mm_free(mm_state_t* st, void* ptr) {
    header_t* current = st->first_el;
    header_t* prev = NULL;

    while (current != (header_t*)ptr - 1) {
        prev = current;
        current = current->next;
    }

    if (current == NULL) {
        return;
    }

    if (!prev) {
        st->first_el = current->next;
    }

    current->is_free = true;
    if (current->next && current->next->is_free) {
        current->next = current->next->next;
    }

    if (prev && prev->is_free && current->next && current->next->is_free) {
        prev->next = current->next->next;
        prev->size += current->size + sizeof(header_t)*2 + current->next->size;
    } else if (prev && prev->is_free) {
        prev->next = current->next;
        prev->size += current->size + sizeof(header_t);
    }
}
