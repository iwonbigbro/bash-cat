#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

function bashcat_test() {
    cat >script.sh

    bash-cat -d bash-cat.dat script.sh

    # Verify the lines have been counted that we expect.
    bash-cat -d bash-cat.dat --text report.txt

    if [[ ${1:-x}${2:-x}${3:-x}${4:-x} == +([0-9]) ]] ; then
        expected="Lines ($1 [executable $2, unexecutable $3]), Covered ($4), Coverage (${5}%)"
        actual=$(grep '^Lines.*executable.*unexecutable.*Coverage' report.txt)
    elif [[ ${1:-} == "expected="* ]] ; then
        eval "$1"
        actual=$(grep -F "$expected" report.txt)
    else
        err "bashcat_test(): Invalid parameters: $*"
    fi

    echo "expected=[$expected]"
    echo "  actual=[$actual]"
    echo "  report=["
    cat report.txt
    echo "]"

    [[ "$actual" == "$expected" ]]
}

