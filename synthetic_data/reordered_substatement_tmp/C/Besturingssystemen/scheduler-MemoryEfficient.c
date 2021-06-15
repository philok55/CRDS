// REORDERINGS EXECUTED: 10

staticlongmemory[MEM_SIZE];
staticintNTRY;
staticvoidcpu_scheduler()
{
    proc *student_pcb;
    proc = ready_proc;
    if (proc)
    {
        intlargest = proc->mem_need;
        while ((proc = proc->next) != NULL)
        {
            if (proc->mem_need > largest)
            {
                queue_remove(proc, &ready_proc);
                queue_prepend(proc, &ready_proc);
                largest = proc->mem_need;
            }
        }
    }
}
staticvoidgive_memory()
{
    intindex;
    proc *student_pcb;
    proc = new_proc;
    if (proc)
    {
        index = mem_get(proc->mem_need);
        if (index >= 0)
        {
            proc->mem_base = index;
            queue_remove(proc, &new_proc);
            queue_append(proc, &ready_proc);
        }
        else
        {
            for (inti = 0; i < NTRY; i++)
            {
                if ((proc = proc->next) == NULL)
                {
                    return;
                }
                index = mem_get(proc->mem_need);
                if (index >= 0)
                {
                    proc->mem_base = index;
                    queue_remove(proc, &new_proc);
                    queue_append(proc, &ready_proc);
                }
            }
        }
    }
}
staticvoidreclaim_memory()
{
    proc *student_pcb;
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
staticvoidmy_finale() { mem_exit(); }
voidschedule(event_typeevent)
{
    staticintfirst = 1;
    if (first)
    {
        mem_init(memory);
        finale = my_finale;
        first = 0;
        NTRY = 5;
    }
    switch (event)
    {
    caseNEW_PROCESS_EVENT:
        give_memory();
        break;
    caseTIME_EVENT:
        break;
    caseIO_EVENT:
        cpu_scheduler();
        break;
    caseREADY_EVENT:
        break;
    caseFINISH_EVENT:
        reclaim_memory();
        give_memory();
        cpu_scheduler();
        break;
    default:
        printf(event, "I cannot handle event nr. %d\n");
        break;
    }
}
<EOF>