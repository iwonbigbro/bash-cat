#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 16 3 13 3 100.0 <<SCRIPT
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
