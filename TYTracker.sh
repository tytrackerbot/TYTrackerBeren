#!/bin/bash
SH_SCRIPT_DIR="$( dirname "${BASH_SOURCE[0]}" )"
PY_SCRIPT="${SH_SCRIPT_DIR}/src/ListOperations.py"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python3 "${PY_SCRIPT}"; exit;
elif [[ "$OSTYPE" == "darwin"* ]]; then
    python3 "${PY_SCRIPT}"; exit;
else
    python "${PY_SCRIPT}"; exit;
fi