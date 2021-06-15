/* Student Name: Philo Decroos
 * Student ID  : 11752262
 * BSc Informatica
 *
 * scheduler-MemoryEfficient.c:
 * This file contains a scheduler that uses a memory efficient algorithm. To
 * make this the skeleton file made by G.D. van Albada is used.
 */

#include <stdio.h>
#include <stdlib.h>

#include "schedule.h"
#include "mem_alloc.h"

/* This variable will simulate the allocatable memory */

static long memory[MEM_SIZE];

static int NTRY;

/* Here we implement a memory efficient CPU scheduler. We make it memory
 * efficient by giving processes with a large memory need high preference,
 * which means they will be executed first so that as much memory as possible
 * will be made available as soon as possible.
 */
static void cpu_scheduler() {
    student_pcb *proc;
    proc = ready_proc;

    if (proc) {
        int largest = proc->mem_need;
        while((proc = proc->next) != NULL) {
            if (proc->mem_need > largest) {
                queue_remove(&ready_proc, proc);
                queue_prepend(&ready_proc, proc);
                largest = proc->mem_need;
            }
        }
    }
}

/* Here we create a memory allocation scheduler. We take a process from the
 * new_proc queue, and try to allocate the amount of memory it needs. If it
 * succeeds, we set the memory base and put the process in the ready_proc
 * queue. If it does not succeed, we try other proccesses the amount of times
 * stated in the NTRY constant.
 */
static void give_memory() {
    int index;
    student_pcb *proc;
    proc = new_proc;

    if (proc) {
        index = mem_get(proc->mem_need);
        if (index >= 0) {
            proc->mem_base = index;
            queue_remove(&new_proc, proc);
            queue_append(&ready_proc, proc);
        } else {
            for (int i = 0; i < NTRY; i++) {
                if ((proc = proc->next) == NULL) {
                    return;
                }
                index = mem_get(proc->mem_need);
                if (index >= 0) {
                    proc->mem_base = index;
                    queue_remove(&new_proc, proc);
                    queue_append(&ready_proc, proc);
                }
            }
        }
    }
}

/* Here we reclaim the memory of a process after it
  has finished */
static void reclaim_memory() {
    student_pcb *proc;

    proc = defunct_proc;
    while (proc) {
        /* Free your own administrative structure if it exists
         */
        if (proc->userdata) {
            free(proc->userdata);
        }
        /* Free the simulated allocated memory
         */
        mem_free(proc->mem_base);
        proc->mem_base = -1;

        /* Call the function that cleans up the simulated process
         */
        rm_process(&proc);

        /* See if there are more processes to be removed
         */
        proc = defunct_proc;
    }
}

/* Here we end the use of the memory manager. */
static void my_finale() {
    mem_exit();
}

/* The main scheduling routine */
void schedule(event_type event) {
    static int first = 1;

    if (first) {
        mem_init(memory);
        finale = my_finale;
        first = 0;
        NTRY = 5;
    }

    switch (event) {
    case NEW_PROCESS_EVENT:
        give_memory();
        break;
    case TIME_EVENT:
        break;
    case IO_EVENT:
        cpu_scheduler();
        break;
    case READY_EVENT:
        break;
    case FINISH_EVENT:
        reclaim_memory();
        give_memory();
        cpu_scheduler();
        break;
    default:
        printf("I cannot handle event nr. %d\n", event);
        break;
    }
}
