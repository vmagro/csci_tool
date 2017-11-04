#!/bin/bash
set -e

source common.sh

source clone.sh


function run_for_student {
  unixname=$1
  studentid=$2
  run=${@:3}

  path="$(clone_student $unixname)"

  # set a variable to reference the assignments dir where the script is
  # this script must be run from within the assignments directory
  export ASSIGNMENTS_DIR="$(pwd)"
  # export some data about the student that the subprocess can use
  export STUDENT=$unixname
  export STUDENT_ID=$studentid
  # make sure we're in the student directory
  pushd $path > /dev/null
  # run whatever we were supposed to run
  result=$(eval "$ASSIGNMENTS_DIR/$run")
  # go back
  popd > /dev/null
  echo $result

  rm -rf $path
}


# only do something interesting if the script is actually being run
# this basically checks if the first argument (name of program) matches what
# bash says the source file name is
if [[ "$0" = "$BASH_SOURCE" ]];
then
  students=$(load_students "$1")
  while read -r student; do
    # we can abuse string "expansion" to pass $student as multiple variables to
    # the run_for_student function
    echo "Running on $student"
    run_for_student $student ${@:2}
  done <<< "$students"
fi
