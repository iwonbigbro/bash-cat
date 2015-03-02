#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# Test that both logical lines are executed when the logical branch
# mandates that they be executed.
bashcat_test 3 3 0 3 100.0 <<SCRIPT
true &&
true
true
SCRIPT

# Test that only one logical line is executed when the logical branch
# prohibits further execution.
bashcat_test 3 3 0 2 66.7 <<SCRIPT
false &&
true
true
SCRIPT

# Test that the first logical test is executed and prohobits the next, but
# allows the next.
bashcat_test 4 4 0 3 75.0 <<SCRIPT
false &&
true ||
true
true
SCRIPT

# Test that the first logical test is executed and subsequent tests are ignored.
bashcat_test 4 4 0 2 50.0 <<SCRIPT
true ||
true ||
true
true
SCRIPT

# Sinle line logical branch test - at some point, we should fix this.  Logically
# it is the same as the preceding test, but coverage is higher because only line
# based coverage is considered.  When implemented through the masking layer,
# the result should match the preceding test when run in branch mode.
bashcat_test 2 2 0 2 100.0 <<SCRIPT
true || true || true
true
SCRIPT
