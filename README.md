# CRDS: Code Reordering Detection System

This project is a Proof-of-Concept implementation used for my Bachelor Thesis at the University of Amsterdam.

CRDS (Code Reordering Detection System) is a source-code plagiarism detection tool based on Abstract Syntax Trees.

It is able to show similar code between submissions, and detect and show code reordering within similar blocks.

Python and C are currently supported, but other languages are easy to add using ANTLR.

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

## Usage

1. To check two files against each other, run:

    ```bash

    python ./main.py path/to/source/file path/to/target/file
    ```
    
2. To cross-compare all submissions in a single folder, run:

    ```bash

    python ./main.py path/to/source/foder/
    ```

## Add new packages/dependencies to venv

1. Add package name to requirements.in

2. run:

    ```bash

    pip-compile
    pip-sync
    ```
