#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

command='echo Test invocation count'

bashcat_test "expected='[+1  ] $command'" <<<"$command"
