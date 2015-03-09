#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# This script is preloaded by bash prior to execution of a script.  To spare
# having to instrument code, this code sets some bash internal parameters that
# make tracing statement and branch execution easier.

if [[ ! $BASHCAT_FD ]] ; then
    echo >&2 "${BASH_SOURCE##*/}: Missing BASHCAT_FD"
    exit 1
fi

set -T
shopt -s extdebug

printer="${BASH_SOURCE%/*}/printer.awk"
printer+=' 1>&'$BASHCAT_FD
#printer+=' 2>/dev/null'
printer+=' -v f="$BASH_SOURCE"'
printer+=' -v l="$LINENO"'
printer+=' -v s="$BASH_COMMAND"'
printer+=' "$BASH_SOURCE"'

trap "$printer" DEBUG
unset printer BASHCAT_FD BASH_ENV
