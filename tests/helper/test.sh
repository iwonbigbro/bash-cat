#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

function run_helper() {
    BASH_ENV=$SRC_LIBDIR/helper.sh /bin/bash -x "$@"
}

function validate_helper() {
    local nlines=0

    while read line ; do
        (( ++nlines ))

        parts=()
        while [[ $line == *":::"* ]] ; do
            parts+=( "${line%%:::*}" )
            line=${line#*:::}
        done
        parts+=( "$line" )
        nparts=${#parts[@]}

        if [[ $nparts != 6 ]] ; then
            echo "expected 6 elements"
            echo "got $nparts elements"
            echo "parts=("
            printf "    %s\n" "${parts[@]}"
            echo ")"
            return 1
        fi
    done

    (( nlines > 0 ))
}

export BASHCAT_FD=200

shopt -s nullglob

for f in ${BASH_SOURCE%/*}/scripts/*.sh ; do
    run_helper $f 200>helper.out
    cat helper.out
    validate_helper $f <helper.out
done
