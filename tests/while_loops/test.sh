#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 4 3 1 3 100.0 <<SCRIPT
while true ; do
    : a simple loop
    break
done
SCRIPT

bashcat_test 5 3 2 3 100.0 <<SCRIPT
while true
do
    : a simple loop
    break
done
SCRIPT

bashcat_test 1 1 0 1 100.0 <<SCRIPT
while true ; do : a simple loop ; break ; done
SCRIPT
