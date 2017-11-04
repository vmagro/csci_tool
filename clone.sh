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
  if [[ -z "$unixname" ]];
  then
    echo "Must provide a student to clone"
    return 1
  fi

  base=/dev/shm
  path="$base/$unixname"
  # delete if it already exists
  rm -rf "$path"
  git clone --depth=1 $(git_url $unixname) "$path" > /dev/null 2>&1

  pushd $path > /dev/null
  git config user.name $author > /dev/null
  git config user.email $email > /dev/null
  popd > /dev/null

  echo $path
}

# only do something interesting if the script is actually being run
# this basically checks if the first argument (name of program) matches what
# bash says the source file name is
if [[ "$0" = "$BASH_SOURCE" ]];
then
  clone_student $1
fi
