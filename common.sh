set -e

source config.sh

function load_students {
  path=$1
  # unix name and usc id are the first two columns separated by a comma
  awk -F',' '{print $1 " " $2}' "$path"
}
