#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# This script is preloaded by bash prior to execution of a script.  To spare
# having to instrument code, this code sets some bash internal parameters that
# make tracing statement and branch execution easier.

if [[ ! $BASHCAT_FD ]] ; then
    echo >&2 "${BASH_SOURCE##*/}: Missing BASHCAT_FD"
    exit 1
fi

if [[ ${BASHCAT_DEBUG:-} == 1 ]] ; then
    set -x
fi

function bashcat_intercept() {
    local ret=$? \
          file=$1 \
          lineno=$2 \
          statement=$3

    awk \
        -v f="$file" \
        -v l=$lineno \
        -v s="$statement" \
        -v fd=$BASHCAT_FD \
        '
            NR == l {
                printf "BASHCAT:::%s:::%s:::%s:::%s:::BASHCAT\n", f, l, s, $0 >>"/dev/fd/"fd;
                exit;
            }
        ' "$file" || true

    return $ret
}

set -T

trap 'bashcat_intercept "$BASH_SOURCE" $LINENO "$BASH_COMMAND"' DEBUG
