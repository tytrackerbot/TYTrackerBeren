#!/bin/bash
SCRIPT_DIR="$( dirname "${BASH_SOURCE[0]}" )";
GIT_PATH="${SCRIPT_DIR}/../";
cd "${GIT_PATH}";
git config user.name "tybot";
git config user.email "tytrackerbot@gmail.com";