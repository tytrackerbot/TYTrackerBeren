#!/bin/bash
SCRIPT_DIR="$( dirname "${BASH_SOURCE[0]}" )"
REQS_FILE_PATH="${SCRIPT_DIR}/../requirements.txt"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python3 -m pip install --upgrade pip --user;
    if [ -f "${REQS_FILE_PATH}" ]; then 
        python3 -m pip install -r requirements.txt --user; 
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m pip install --upgrade pip --user;
    if [ -f "${REQS_FILE_PATH}" ]; then 
        python3 -m pip install -r requirements.txt --user; 
    fi
else
    python -m pip install --upgrade pip --user;
    if [ -f "${REQS_FILE_PATH}" ]; then 
        python -m pip install -r requirements.txt --user; 
    fi
fi