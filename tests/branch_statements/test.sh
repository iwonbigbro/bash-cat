#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 3 2 1 2 100.0 <<SCRIPT
if true ; then
    echo
fi
SCRIPT

bashcat_test 4 2 2 2 100.0 <<SCRIPT
if true
then
    echo
fi
SCRIPT

bashcat_test 6 3 3 2 66.7 <<SCRIPT
if true
then
    echo # Covered
else
    echo # Not covered
fi
SCRIPT

bashcat_test 6 3 3 2 66.7 <<SCRIPT
if false
then
    echo # Not covered
else
    echo # Covered
fi
SCRIPT

bashcat_test 7 4 3 2 50.0 <<SCRIPT
if true
then
    echo # Covered
elif true
then
    echo # Not covered
fi
SCRIPT

bashcat_test 7 4 3 3 75.0 <<SCRIPT
if false
then
    echo # Not covered
elif true
then
    echo # Covered
fi
SCRIPT

