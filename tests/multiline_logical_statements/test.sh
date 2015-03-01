#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

function check_branch() {
    cat >script.sh

    bash-cat -d bash-cat.dat script.sh

    # Verify the lines have been counted that we expect.
    bash-cat -d bash-cat.dat --text report.txt

    expected="Lines ($1 [executable $2, unexecutable $3]), Covered ($4), Coverage (${5}%)"
    actual=$(grep '^Lines.*executable.*unexecutable.*Coverage' report.txt)

    echo "e=[$expected]"
    echo "a=[$actual]"

    [[ "$actual" == "$expected" ]]
}

# Test that both logical lines are executed when the logical branch
# mandates that they be executed.
check_branch 3 3 0 3 100.0 <<SCRIPT
true &&
true
true
SCRIPT

# Test that only one logical line is executed when the logical branch
# prohibits further execution.
check_branch 3 3 0 2 66.7 <<SCRIPT
false &&
true
true
SCRIPT

# Test that the first logical test is executed and prohobits the next, but
# allows the next.
check_branch 4 4 0 3 75.0 <<SCRIPT
false &&
true ||
true
true
SCRIPT

# Test that the first logical test is executed and subsequent tests are ignored.
check_branch 4 4 0 2 50.0 <<SCRIPT
true ||
true ||
true
true
SCRIPT

# Sinle line logical branch test - at some point, we should fix this.  Logically
# it is the same as the preceding test, but coverage is higher because only line
# based coverage is considered.  When implemented through the masking layer,
# the result should match the preceding test when run in branch mode.
check_branch 2 2 0 2 100.0 <<SCRIPT
true || true || true
true
SCRIPT
