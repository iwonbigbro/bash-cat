#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# With standard output and standard error redirected to /dev/null, we should
# still be able to intercept our trace output and produce the correct coverage
# statistics for the script.
cat >script.sh <<SCRIPT
exec 1>/dev/null 2>&1

false &&
true

true &&
true

true
SCRIPT

bash-cat -d bash-cat.dat script.sh

# Verify the lines have been counted that we expect.
bash-cat -d bash-cat.dat --text report.txt

expected="Lines (9 [executable 6, unexecutable 3]), Covered (5), Coverage (83.3%)"
actual=$(grep '^Lines.*executable.*unexecutable.*Coverage' report.txt)

echo "e=[$expected]"
echo "a=[$actual]"

[[ "$actual" == "$expected" ]]
