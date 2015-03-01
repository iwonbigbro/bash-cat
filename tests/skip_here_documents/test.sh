#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

cat <<EXPANSION_CAPABLE_HERE_DOCUMENT
These lines within this here document
will be excluded from the coverage results.
EXPANSION_CAPABLE_HERE_DOCUMENT

cat <<-UNINDENT_CAPABLE_HERE_DOCUMENT
    These lines within this here document
    will be excluded from the coverage results.
UNINDENT_CAPABLE_HERE_DOCUMENT

cat <<'QUOTED_HERE_DOCUMENT'
These lines within this here document
will be excluded from the coverage results.
QUOTED_HERE_DOCUMENT
SCRIPT

bash-cat -d bash-cat.dat script.sh

# Verify the lines have been counted that we expect.
bash-cat -d bash-cat.dat --text report.txt

expected='Lines (16 [executable 3, unexecutable 13]), Covered (3), Coverage (100.0%)'
actual=$(grep '^Lines.*executable.*unexecutable.*Coverage' report.txt)

echo "e=[$expected]"
echo "a=[$actual]"

[[ "$actual" == "$expected" ]]

