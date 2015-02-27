#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# A simple test runner implementation.

set -Eeu

run_test_sh=$(readlink -f "$BASH_SOURCE")

export TEST_NAME=$1
export TEST_DATE=$(date -u "+%Y%m%dT%H%M%S")
export TEST_SCRIPT=$(readlink -f "${run_test_sh%/*}/$1/test.sh")
export TEST_SETUP=$(readlink -f "${run_test_sh%/*}/$1/setup.sh")
export TEST_TEARDOWN=$(readlink -f "${run_test_sh%/*}/$1/teardown.sh")
export TEST_ROOT=$BUILDROOT/$1

mkdir -p $TEST_ROOT

function bail() {
    set +eu
    local e=$1 ; shift
    if [[ $e != 0 ]] ; then
        echo >&5 "${FUNCNAME[1]^^} - $TEST_NAME${1:+ [$*]}"
        if [[ ${TEST_DEBUG:-} ]] ; then
            cat >&5 $TEST_ROOT/debug
        fi
        cat >&5 $TEST_ROOT/stdout $TEST_ROOT/stderr
    elif [[ ${TEST_DEBUG:-} ]] ; then
        echo >&5 "${FUNCNAME[1]^^} - $TEST_NAME${1:+ [$*]}"
        cat >&5 $TEST_ROOT/debug $TEST_ROOT/stdout $TEST_ROOT/stderr
    fi
    echo >&5 "${FUNCNAME[1]^^} - $TEST_NAME${1:+ [$*]}"
    exit $e
}

function err() { bail 1 "$@" ; }
function fail() { bail 1 "$@" ; }
function skip() { bail 0 "$@" ; }
function pass() { bail 0 "$@" ; }

function setup() {
    trap "err 'Setup error'" ERR
    if [[ -f $TEST_SETUP ]] ; then
        . $TEST_SETUP
    fi
}

function teardown() {
    if [[ $TEST_RESULT == 0 ]] ; then
        ( pass ) || true
    else
        ( fail "Test failure" ) || true
    fi

    section "Teardown"
    if [[ -f $TEST_TEARDOWN ]] ; then
        . $TEST_TEARDOWN
    fi

    exit $TEST_RESULT
}

function section() {
    set +x
    exec 1>&- 2>&- 3>&-
    trap "err '$1 error'" ERR
    exec 1>$TEST_ROOT/stdout 2>$TEST_ROOT/stderr 3>$TEST_ROOT/debug
    set -x
}

exec 5>&1
BASH_XTRACEFD=3
set -x

section "Initlisation"

cd $TEST_ROOT

# The path to the local CVS repository should have been set.
[[ -d $CVSROOT ]]

TEST_RESULT=1

trap "teardown" EXIT

section "Setup"
setup

section "Test"
. $TEST_SCRIPT

TEST_RESULT=0
