# Bachelor Thesis of Philo Decroos

This project is the implementation used for my Bachelor Thesis at the University of Amsterdam.

This is a code plagiarism tool using Abstract Syntax Trees.

Currently, comparison is only between 2 files.

Python and C are supported, but other languages are easy to add using ANTLR.

## Setup

Uses python 3.6.

1. Create virtual environment:

    ```bash

    python3 -m venv venv
    . venv/bin/activate
    pip install pip-tools
    pip-sync
    ```

2. Restart venv:

    ```bash

    . venv/bin/activate
    pip-sync
    ```

## Add new packages/dependencies to venv

1. Add package name to requirements.in

2. run:

    ```bash

    pip-compile
    pip-sync
    ```

## Run plagiarism checker

1. run:

    ```bash

    python ./main.py path/to/source/file path/to/target/file
    ```
