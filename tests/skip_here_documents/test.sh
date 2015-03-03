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

bashcat_test 19 9 10 2 22.2 <<'SCRIPT'
line='[BUGFIX-A/12345] {A/F2_DB/1234} Blah'

[[ $line == \[BUGFIX-[A-C]/+([0-9])\]\ * ]] ||
[[ $line == \[DEVELOPMENT/+([0-9])\]\ * ]] ||
[[ $line == \[ENHANCEMENT/+([0-9])\]\ * ]] ||
[[ $line == \[OTHER/+([0-9])\]\ * ]] ||
[[ $line == \[USEREXIT/+([0-9])\]\ * ]] || {
      cat >&2 <<ERROR
Error: Invalid commit message, expecting category of:
    BUGFIX-[A-C]
    DEVELOPMENT
    ENHANCEMENT
    OTHER
    USEREXIT

Commit log message:
ERROR
    exit 0
}
SCRIPT
