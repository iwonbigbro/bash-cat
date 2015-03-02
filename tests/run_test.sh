#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# A simple test runner implementation.

set +x
set -Eeu

run_test_sh=$(readlink -f "$BASH_SOURCE")

export TEST_NAME=$1
export TEST_DATE=$(date -u "+%Y%m%dT%H%M%S")
export TEST_SCRIPT=$(readlink -f "${run_test_sh%/*}/$1/test.sh")
export TEST_SETUP=$(readlink -f "${run_test_sh%/*}/$1/setup.sh")
export TEST_TEARDOWN=$(readlink -f "${run_test_sh%/*}/$1/teardown.sh")
export TEST_ROOT=$BUILDROOT/tests/$1

rm -rf $TEST_ROOT
mkdir -p $TEST_ROOT

export PS4='+ $(date +%M:%S.%N):${BASH_SOURCE##*/}:$LINENO:${FUNCNAME:-main}()::: '

function bail() {
    set +xeu
    local e=$1 ; shift
    local p="${FUNCNAME[1]^^} - $TEST_NAME${1:+ [$*]}"
    local debug_line=$(tail -9 $TEST_ROOT/debug | head -1 | sed 's?^+.*()::: ??')

    {

    if [[ $e == 0 ]] ; then
        echo "$p"
        exit $e
    fi

    if [[ ${TEST_DEBUG:-} ]] ; then
        echo "$p: DEBUG_BEG:"
        cat $TEST_ROOT/debug
        echo "$p: DEBUG_END:"
    fi

    if [[ -s $TEST_ROOT/output ]] ; then
        echo "$p: OUTPUT_BEG:"
        cat $TEST_ROOT/output
        echo "$p: OUTPUT_END:"
    elif [[ ! ${TEST_DEBUG:-} ]] ; then
        echo "$p"
    fi

    echo

    if [[ $TEST_STATEMENT != $debug_line ]] ; then
        echo "    >>>   ${TEST_STATEMENT:-Unknown error}   <<<"
    fi

    echo "    >>>   $debug_line   <<<"
    echo
    echo "$p"

    } >&5

    exit $e
}

function err() { bail 1 "$@" ; }
function fail() { bail 1 "$@" ; }
function skip() { bail 0 "$@" ; }
function pass() { bail 0 "$@" ; }

function setup() {
    if [[ -f $TEST_SETUP ]] ; then
        TEST_SETUP_RUN=1

        . $TEST_SETUP
    fi
}

function end_test() {
    if [[ $TEST_RESULT == 0 ]] ; then
        touch $TEST_ROOT/pass

        ( pass ) || true
    else
        ( fail "$TEST_SECTION failure" ) || true
    fi

    if [[ -f $TEST_TEARDOWN ]] ; then
        ( . $TEST_TEARDOWN ) || fail "Teardown failure"
    fi

    exit $TEST_RESULT
}

function section() {
    TEST_SECTION=$1

    :>$TEST_ROOT/debug
}

if [[ -f ${run_test_sh%/*}/run_test_functions.sh ]] ; then
    . ${run_test_sh%/*}/run_test_functions.sh
fi

exec 5>&1 1>$TEST_ROOT/output 2>&1 3>$TEST_ROOT/debug

BASH_XTRACEFD=3
set -x

section "Initlisation"

TEST_RESULT=1
TEST_SETUP_RUN=

trap 'e=$? ; TEST_STATEMENT=$BASH_COMMAND ; exit $e' ERR
trap 'end_test $?' EXIT

cd $TEST_ROOT

section "Setup"
setup

section "Test"
. $TEST_SCRIPT

TEST_RESULT=0
