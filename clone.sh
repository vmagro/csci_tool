#!/bin/bash
set -e

source common.sh

# get a preauthenticated url to use for git clones
function git_url {
  unixname=$1
  echo "https://$username:$token@github.com/$org/hw_$unixname.git"
}

# clone a student repo into temporary directory and return its path
function clone_student {
  unixname=$1
  base=/dev/shm
  path="$base/$unixname"
  echo "Cloning repo for $unixname to $path"
  # delete if it already exists
  rm -rf "$path"
  git clone --depth=1 $(git_url $unixname) "$path" > /dev/null 2>&1

  git config user.name $author > /dev/null
  git config user.email $email > /dev/null

  echo $path
}

# only do something interesting if the script is actually being run
# this basically checks if the first argument (name of program) matches what
# bash says the source file name is
if [[ "$0" = "$BASH_SOURCE" ]];
then
  if [[ -n "$1" ]];
  then
    clone_student $1
  else
    echo "Must provide a student to clone"
    exit 1
  fi
fi
