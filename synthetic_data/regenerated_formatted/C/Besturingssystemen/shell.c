void make_header(header_t *header, size_t nbytes)
{
    void *p = (void *)(header + 1);
    if (header->next != NULL)
    {
        header_t *temp = header->next;
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = temp;
    }
    else
    {
        header->next = (header_t *)((char *)p + nbytes);
        header->next->size = header->size - sizeof(header_t) - nbytes;
        header->next->is_free = true;
        header->next->next = NULL;
    }
}
struct sigaction sa;
void my_free_tree(void *pt) { free_tree((node_t *)pt); }
void initialize(void)
{
    sa.sa_handler = SIG_IGN;
    if (sigaction(SIGINT, &sa, NULL) < 0)
    {
        perror("sigaction");
        _exit(-1);
    }
}
void reset_signals()
{
    sa.sa_handler = SIG_DFL;
    if (sigaction(SIGINT, &sa, NULL) < 0)
    {
        perror("sigaction");
        _exit(-1);
    }
}
void run_command(node_t *node)
{
    arena_push();
    arena_register_mem(node, &my_free_tree);
    run_type(node);
    arena_pop();
}
void run_type(node_t *node)
{
    switch (node->type)
    {
    case NODE_COMMAND:
        command(node);
        break;
    case NODE_SEQUENCE:
        run_sequence(node);
        break;
    case NODE_PIPE:
        run_pipe(node);
        break;
    case NODE_SUBSHELL:
        run_subshell(node);
        break;
    default:
        fprintf(stderr, "Error: unknown type");
    }
}
void command(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    if (strcmp(program, "exit") == 0)
    {
        _exit(atoi(argv[1]));
    }
    else if(strcmp(program, "cd") == 0)
    {
        if (chdir(argv[1]) < 0)
        {
            perror("cd");
        }
    }
    else { run_simple_command(node); }
}
void run_simple_command(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    pid_t pid;
    if ((pid = fork()) == -1)
    {
        perror("fork");
        _exit(-1);
    }
    else if(pid == 0)
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
        if (waitpid(pid, NULL, 0) < 0)
        {
            perror("error");
            _exit(-1);
        }
    }
    return;
}
void run_sequence(node_t *node)
{
    run_type(node->sequence.first);
    run_type(node->sequence.second);
    return;
}
void run_pipe(node_t *node)
{
    int fd[2];
    pid_t child1, child2;
    if (pipe(fd) < 0)
    {
        perror("pipe");
        _exit(-1);
    }
    if ((child1 = fork()) == -1)
    {
        perror("fork");
        _exit(-1);
    }
    else if(child1 == 0)
    {
        close(fd[0]);
        handle_pipe(fd, 1, 0, node);
        return;
    }
    close(fd[1]);
    if ((child2 = fork()) == -1)
    {
        perror("fork");
        _exit(-1);
    }
    else if(child2 == 0)
    {
        handle_pipe(fd, 0, 1, node);
        return;
    }
    waitpid(child1, NULL, 0);
    waitpid(child2, NULL, 0);
    close(fd[0]);
}
void handle_pipe(int *pipe, int fd, int index, node_t *node)
{
    reset_signals();
    if (dup2(pipe[fd], fd) == -1)
    {
        perror("filedescriptor");
        _exit(-1);
    }
    run_simple_no_fork(node->pipe.parts[index]);
}
void run_simple_no_fork(node_t *node)
{
    char *program = node->command.program;
    char **argv = node->command.argv;
    if (strcmp(program, "exit") == 0)
    {
        _exit(atoi(argv[1]));
    }
    else if(strcmp(program, "cd") == 0)
    {
        if (chdir(argv[1]) < 0)
        {
            perror("cd");
            _exit(-1);
        }
    }
    else
    {
        if (execvp(program, argv) < 0)
        {
            perror("execvp");
            _exit(-1);
        }
    }
}
void run_subshell(node_t *node)
{
    pid_t child;
    if ((child = fork()) == -1)
    {
        perror("fork");
    }
    if (child == 0)
    {
        run_type(node->subshell.child);
        _exit(0);
    }
    else
    {
        waitpid(child, NULL, 0);
    }
}
