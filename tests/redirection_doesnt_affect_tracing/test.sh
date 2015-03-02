#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

# With standard output and standard error redirected to /dev/null, we should
# still be able to intercept our trace output and produce the correct coverage
# statistics for the script.
bashcat_test 9 6 3 5 83.3 <<SCRIPT
exec 1>/dev/null 2>&1

false &&
true

true &&
true

true
SCRIPT
