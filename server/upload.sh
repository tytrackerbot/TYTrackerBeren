#!/bin/bash  
SCRIPT_DIR="$( dirname "${BASH_SOURCE[0]}" )"
ADD_FILE_PATH="${SCRIPT_DIR}/../data/tracked_items.json"
git add "${ADD_FILE_PATH}" 
git commit -m "User Item Update"
git push origin master --force