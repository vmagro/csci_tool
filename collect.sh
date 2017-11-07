#!/bin/bash
set -e

source common.sh

source run.sh

# only do something interesting if the script is actually being run
# this basically checks if the first argument (name of program) matches what
# bash says the source file name is
if [[ "$0" = "$BASH_SOURCE" ]];
then
  students=$(load_students "$1")
  project="$2"
  dest="$3"
  deadline="$4"
  while read -r student; do
    # we can abuse string "expansion" to pass $student as multiple variables to
    # the run_for_student function
    echo "Running on $student"
    run_for_student $student collect $project $dest $deadline
  done <<< "$students"
fi
