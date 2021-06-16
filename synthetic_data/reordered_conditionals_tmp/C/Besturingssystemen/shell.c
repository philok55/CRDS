// REORDERINGS EXECUTED: 11

voidmake_header(header_t *header, size_tnbytes)
{
    void *p = (void *)(header + 1);
    if (header->next != NULL)
    {
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = NULL;
    }
    else
    {
        header_t *temp = header->next;
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = temp;
    }
}
structsigactionsa;
voidmy_free_tree(void *pt) { free_tree((node_t *)pt); }
voidinitialize(void)
{
    sa.sa_handler = SIG_IGN;
    if (sigaction(SIGINT, &sa, NULL) < 0)
    {
        perror("sigaction");
        _exit(-1);
    }
}
voidreset_signals()
{
    sa.sa_handler = SIG_DFL;
    if (sigaction(SIGINT, &sa, NULL) < 0)
    {
        perror("sigaction");
        _exit(-1);
    }
}
voidrun_command(node_t *node)
{
    arena_push();
    arena_register_mem(node, &my_free_tree);
    run_type(node);
    arena_pop();
}
voidrun_type(node_t *node)
{
    switch (node->type)
    {
    default:
        fprintf(stderr, "Error: unknown type");
    caseNODE_PIPE:
        run_pipe(node);
        break;
    caseNODE_COMMAND:
        command(node);
        break;
    caseNODE_SUBSHELL:
        run_subshell(node);
        break;
    caseNODE_SEQUENCE:
        run_sequence(node);
        break;
    }
}
voidcommand(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    if (strcmp(program, "exit") == 0)
        if (strcmp(program, "cd") == 0)
        {
            run_simple_command(node);
        }
        else
        {
            if (chdir(argv[1]) < 0)
            {
                perror("cd");
            }
        }
    else
    {
        _exit(atoi(argv[1]));
    }
}
voidrun_simple_command(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    pid_tpid;
    if ((pid = fork()) == -1)
        if (pid == 0)
        {
            if (waitpid(pid, NULL, 0) < 0)
            {
                perror("error");
                _exit(-1);
            }
        }
        else
        {
            reset_signals();
            if (execvp(program, argv) < 0)
            {
                perror("execvp error");
                _exit(-1);
            }
        }
    else
    {
        perror("fork");
        _exit(-1);
    }
    return;
}
voidrun_sequence(node_t *node)
{
    run_type(node->sequence.first);
    run_type(node->sequence.second);
    return;
}
voidrun_pipe(node_t *node)
{
    intfd[2];
    pid_tchild1, child2;
    if (pipe(fd) < 0)
    {
        perror("pipe");
        _exit(-1);
    }
    if ((child1 = fork()) == -1)
        if (child1 == 0)
        {
            close(fd[0]);
            handle_pipe(fd, 1, 0, node);
            return;
        }
        else
        {
            perror("fork");
            _exit(-1);
        }
    close(fd[1]);
    if ((child2 = fork()) == -1)
        if (child2 == 0)
        {
            handle_pipe(fd, 0, 1, node);
            return;
        }
        else
        {
            perror("fork");
            _exit(-1);
        }
    waitpid(child1, NULL, 0);
    waitpid(child2, NULL, 0);
    close(fd[0]);
}
voidhandle_pipe(int *pipe, intfd, intindex, node_t *node)
{
    reset_signals();
    if (dup2(pipe[fd], fd) == -1)
    {
        perror("filedescriptor");
        _exit(-1);
    }
    run_simple_no_fork(node->pipe.parts[index]);
}
voidrun_simple_no_fork(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    if (strcmp(program, "exit") == 0)
        if (strcmp(program, "cd") == 0)
        {
            if (execvp(program, argv) < 0)
            {
                perror("execvp");
                _exit(-1);
            }
        }
        else
        {
            if (chdir(argv[1]) < 0)
            {
                perror("cd");
                _exit(-1);
            }
        }
    else
    {
        _exit(atoi(argv[1]));
    }
}
voidrun_subshell(node_t *node)
{
    pid_tchild;
    if ((child = fork()) == -1)
    {
        perror("fork");
    }
    if (child == 0)
    {
        waitpid(child, NULL, 0);
    }
    else
    {
        run_type(node->subshell.child);
        _exit(0);
    }
}
<EOF>