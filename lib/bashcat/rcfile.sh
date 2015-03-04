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
          bash_lineno=$3 \
          statement=$4

    # Re-assert after new function declarations.
    set -T

    if (( lineno < 1 && bash_lineno > 0 )) ; then
        lineno=$bash_lineno
    fi

    # Cache the file in a global array.
    local var="bashcat_mapfile_${file//[^A-Za-z0-9]/_}"
    eval "local lines=( \"\${$var[@]}\" )"

    if (( ${#lines[@]} == 0 )) ; then
        mapfile -O 1 $var < $file &&
        eval "local lines=( \"\${$var[@]}\" )"
    fi

    printf >/dev/fd/$BASHCAT_FD \
        "BASHCAT:::%s:::%s:::%s:::%s:::BASHCAT\n" \
        "$file" "$lineno" "$statement" "${lines[$lineno]}" \
    || true
}

set -T
shopt -s extdebug

trap 'bashcat_intercept "$BASH_SOURCE" "$LINENO" "$BASH_LINENO" "$BASH_COMMAND"' DEBUG
