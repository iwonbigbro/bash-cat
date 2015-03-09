#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# This script is preloaded by bash prior to execution of a script.  To spare
# having to instrument code, this code sets some bash internal parameters that
# make tracing statement and branch execution easier.
if [[ ! $BASHCAT_FD ]] ; then
    echo >&2 "${BASH_SOURCE##*/}: Missing BASHCAT_FD"
    exit 1
fi

bashcat_rcfile_sh=$(readlink -f "$BASH_SOURCE")
awkscr=${bashcat_rcfile_sh%/*}/readline.awk
awkcmd="$awkscr"' 2>/dev/null >>/dev/fd/'$BASHCAT_FD' -v p=X -v f="$BASH_SOURCE" -v l=$LINENO -v s="$BASH_COMMAND" "$BASH_SOURCE"'
#export PS4="+ \$($awkcmd)"

set -T
shopt -s extdebug

trap "${awkcmd//p=X/p=D}" DEBUG

unset BASH_ENV
