#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

echo a statement \\
    that spans \\
    multiple lines \\
    but should be \\
    recorded \\
    correctly
SCRIPT

bash-cat -d bash-cat.dat script.sh

# Verify the lines have been counted that we expect.
bash-cat -d bash-cat.dat --text report.txt

expected='Lines (8 [executable 1, non-executable 7]), Covered (1), Coverage (100.0%)'
actual=$(grep '^Lines.*executable.*non-executable.*Coverage' report.txt)

echo "e=[$expected]"
echo "a=[$actual]"

[[ "$actual" == "$expected" ]]

