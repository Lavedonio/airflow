#!/bin/bash

exit_status=$1

if [ "$exit_status" = "error" ]; then
    echo 'Error occured. Exiting with error'
    exit 1
else
    echo 'Bash script worked'
fi
