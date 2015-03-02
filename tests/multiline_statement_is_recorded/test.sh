#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 8 6 2 6 100.0 <<SCRIPT
#!/bin/bash

echo a statement \\
    that spans \\
    multiple lines \\
    but should be \\
    recorded \\
    correctly
SCRIPT
