#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

cat >script.sh <<SCRIPT
#!/bin/bash

echo "Single statement"
SCRIPT

bash-cat -d bash-cat.dat script.sh

[[ $(bash-cat -d bash-cat.dat --total -) == "(100.00%) covered" ]]
