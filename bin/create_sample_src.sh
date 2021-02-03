#!/bin/bash


# quick way to make sample src files for an Achievement
# usage: create_sample_src.sh achievement_name
# it'll create the files under valid and invalid subdirs
# using the achievement_name


VALID_PATH="./tests/samples/valid/$1.py"
INVALID_PATH="./tests/samples/invalid/$1.py"

touch $VALID_PATH
touch $INVALID_PATH

printf "# cases where $1 should unlock\n\n# >> CASE\n" > $VALID_PATH
printf "# cases where $1 should not unlock\n\n# >> CASE\n" > $INVALID_PATH
