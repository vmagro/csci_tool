#!/bin/bash
set -e

source common.sh

source clone.sh


function run_for_student {
  unixname=$1
  run=${@:2}

  path="$(clone_student $unixname)"

  # set a variable to reference the assignments dir where the script is
  # this script must be run from within the assignments directory
  export ASSIGNMENTS_DIR="$(pwd)"
  # make sure we're in the student directory
  pushd $path > /dev/null
  # run whatever we were supposed to run
  result=$(eval "$ASSIGNMENTS_DIR/$run")
  # go back
  popd > /dev/null
  echo $result
}


# only do something interesting if the script is actually being run
# this basically checks if the first argument (name of program) matches what
# bash says the source file name is
if [[ "$0" = "$BASH_SOURCE" ]];
then
  run_for_student $1 ${@:2}
fi
