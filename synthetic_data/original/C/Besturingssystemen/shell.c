/* Author:      Philo Decroos
 * UvA-Net-ID:  11752262
 * BSc Informatica
 *
 * shell.c:
 * This file contains functions that execute commands that have been given to
 * our shell. After the parsing of the input a pointer to a node_t type is
 * passed to the run_command function, and from there different functions will
 * be called depending on the type of the input.
 */


#include "arena.h"
#include "ast.h"
#include "front.h"
#include "shell.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

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

/*
 * The state of this struct determines the action taken when the <ctrl-C>
 * signals are given to the current process.
 */
struct sigaction sa;

/*
 * This function is used by the functions in arana.c to free the tree.
 */
void my_free_tree(void *pt) {
    free_tree((node_t *)pt);
}

/*
 * Here we change the signal handler to ignore SIGINT signals, because we
 * don't want the shell to exit on pressing ctrl-C.
 */
void initialize(void) {
    sa.sa_handler = SIG_IGN;
    if (sigaction(SIGINT, &sa, NULL) < 0) {
        perror("sigaction");
        _exit(-1);
    }
}

/*
 * This function is used to reset the handler of signals to default, which we
 * need after forking a child, because children inherit the settings of the
 * parent process.
 */
void reset_signals() {
    sa.sa_handler = SIG_DFL;
    if (sigaction(SIGINT, &sa, NULL) < 0) {
        perror("sigaction");
        _exit(-1);
    }
}

/*
 * For every command put into the shell this function is called. It creates
 * a memory arena from "arena.c" to handle the command, calles the run_type
 * function to determine the type of the command, and then pops the arena to
 * free the memory.
 */
void run_command(node_t *node) {
    arena_push();
    arena_register_mem(node, &my_free_tree);

    run_type(node);

    arena_pop();
}

/*
 * This function determines the type of the command and calls the corresponding
 * function to execute it.
 */
void run_type(node_t *node) {
    switch (node->type) {
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

/*
 * This function executes a simple command: exit and cd are executed with
 * builtin functions, for other commands we call the run_simple_command
 * function.
 */
void command(node_t *node) {
    char *program = node->command.program;
    char **argv = node->command.argv;

    if (strcmp(program, "exit") == 0) {
        _exit(atoi(argv[1]));
    } else if (strcmp(program, "cd") == 0) {
        if (chdir(argv[1]) < 0) {
            perror("cd");
        }
    } else {
        run_simple_command(node);
    }
}

/*
 * To run a simple command, we fork a childprocess, and execute the command in
 * it using the execvp system call.
 */
void run_simple_command(node_t *node) {
    char *program = node->command.program;
    char **argv = node->command.argv;
    pid_t pid;

    if ((pid = fork()) == -1) {
        perror("fork");
        _exit(-1);
    } else if (pid == 0) {
        reset_signals();
        if (execvp(program, argv) < 0) {
            perror("execvp error");
            _exit(-1);
        }
    } else {
        if (waitpid(pid, NULL, 0) < 0) {
            perror("error");
            _exit(-1);
        }
    }
    return;
}

/*
 * To run a sequence this function takes the first part and the second part of
 * a sequence, and puts both back into the run_type function.
 */
void run_sequence(node_t *node) {
    run_type(node->sequence.first);
    run_type(node->sequence.second);
    return;
}

/*
 * This function runs a pipe of two simple commands. We create a pipe, fork
 * a child for both commands, and connect stdin or stdout to the pipe. Then
 * we execute both commands, sending the output of the first command to the
 * input of the second.
 */
void run_pipe(node_t *node) {
    int fd[2];
    pid_t child1, child2;
    if (pipe(fd) < 0) {
        perror("pipe");
        _exit(-1);
    }
    if ((child1 = fork()) == -1) {
        perror("fork");
        _exit(-1);
    } else if (child1 == 0) {
        close(fd[0]);
        handle_pipe(fd, 1, 0, node);
        return;
    }
    close(fd[1]);
    if ((child2 = fork()) == -1) {
        perror("fork");
        _exit(-1);
    } else if (child2 == 0) {
        handle_pipe(fd, 0, 1, node);
        return;
    }
    waitpid(child1, NULL, 0);
    waitpid(child2, NULL, 0);
    close(fd[0]);
}

/*
 * This function is called in the children that are connected to a pipe. It
 * resets the signal handler so that the commands will not ignore signals,
 * connects stdin or stdout to the pipe and calls run_simple_no_fork to
 * execute the command.
 */
void handle_pipe(int *pipe, int fd, int index, node_t *node) {
    reset_signals();
    if (dup2(pipe[fd], fd) == -1) {
        perror("filedescriptor");
        _exit(-1);
    }
    run_simple_no_fork(node->pipe.parts[index]);
}

/*
 * This function runs a simple command without forking. It is used by the
 * run_pipe function to run a command in a process that has already been
 * forked from the shell.
 */
void run_simple_no_fork(node_t *node) {
    char *program = node->command.program;
    char **argv = node->command.argv;
    if (strcmp(program, "exit") == 0) {
        _exit(atoi(argv[1]));
    } else if (strcmp(program, "cd") == 0) {
        if (chdir(argv[1]) < 0) {
            perror("cd");
            _exit(-1);
        }
    } else {
        if (execvp(program, argv) < 0) {
            perror("execvp");
            _exit(-1);
        }
    }
}

/*
 * This function creates a subshell by forking and using the childprocess as
 * a new shell to run commands in.
 */
void run_subshell(node_t *node) {
    pid_t child;
    if ((child = fork()) == -1) {
        perror("fork");
    }
    if (child == 0) {
        run_type(node->subshell.child);
        _exit(0);
    } else {
        waitpid(child, NULL, 0);
    }
}
