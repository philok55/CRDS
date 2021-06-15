// REORDERINGS EXECUTED: 1

static long memory[MEM_SIZE];
static int NTRY;
static void cpu_scheduler()
{
    student_pcb *proc;
    proc = ready_proc;
    if (proc)
    {
        int largest = proc->mem_need;
        while ((proc = proc->next) != NULL)
        {
            if (proc->mem_need > largest)
            {
                queue_remove(&ready_proc, proc);
                queue_prepend(&ready_proc, proc);
                largest = proc->mem_need;
            }
        }
    }
}
static void give_memory()
{
    int index;
    student_pcb *proc;
    proc = new_proc;
    if (proc)
    {
        index = mem_get(proc->mem_need);
        if (index >= 0)
        {
            proc->mem_base = index;
            queue_remove(&new_proc, proc);
            queue_append(&ready_proc, proc);
        }
        else
        {
            for (int i = 0; i < NTRY; i++)
            {
                if ((proc = proc->next) == NULL)
                {
                    return;
                }
                index = mem_get(proc->mem_need);
                if (index >= 0)
                {
                    proc->mem_base = index;
                    queue_remove(&new_proc, proc);
                    queue_append(&ready_proc, proc);
                }
            }
        }
    }
}
static void reclaim_memory()
{
    student_pcb *proc;
    proc = defunct_proc;
    while (proc)
    {
        if (proc->userdata)
        {
            free(proc->userdata);
        }
        mem_free(proc->mem_base);
        proc->mem_base = -1;
        rm_process(&proc);
        proc = defunct_proc;
    }
}
static void my_finale() { mem_exit(); }
void schedule(event_type event)
{
    static int first = 1;
    if (first)
    {
        mem_init(memory);
        finale = my_finale;
        first = 0;
        NTRY = 5;
    }
    switch (event)
    {
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
