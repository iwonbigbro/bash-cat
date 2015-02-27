#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

echo "Single statement"
SCRIPT

bash-cat -o bash-cat.dat script.sh

[[ $(bash-cat -o bash-cat.dat --total) == "(100.00%) covered" ]]
