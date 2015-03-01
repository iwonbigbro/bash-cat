#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

echo "Single statement"

# A comment that should be ignored.
echo "Another statement"

: Bash null operation, which should be counted.
SCRIPT

bash-cat -d bash-cat.dat script.sh

[[ $(bash-cat -d bash-cat.dat --total -) == "(100.00%) covered" ]]

# Verify the lines have been counted that we expect.
bash-cat -d bash-cat.dat --text report.txt

grep -F 'Lines (8 [executable 3, non-executable 5]), Covered (3), Coverage (100.0%)' report.txt

