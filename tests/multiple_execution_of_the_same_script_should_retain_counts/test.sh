#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

echo when a script is executed multiple times, it should \\
    retain previous invocation counts and the coverage stats \\
    should be shown in the report.
SCRIPT

bash-cat -d bash-cat.dat script.sh
bash-cat -d bash-cat.dat script.sh
bash-cat -d bash-cat.dat script.sh
bash-cat -d bash-cat.dat script.sh
bash-cat -d bash-cat.dat script.sh

# Verify the lines have been counted that we expect.
bash-cat -d bash-cat.dat --text report.txt

expected='[+5  ] echo when a script is executed multiple times, it should \'
actual=$(grep 'echo when a script is executed multiple times, it should' report.txt)

echo "e=[$expected]"
echo "a=[$actual]"

[[ "$actual" == "$expected" ]]

