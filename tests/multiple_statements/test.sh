#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 8 3 5 3 100.0 <<SCRIPT
#!/bin/bash

echo "Single statement"

# A comment that should be ignored.
echo "Another statement"

: Bash null operation, which should be counted.
SCRIPT
