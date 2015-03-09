#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys

def err(msg):
    if not str(msg):
        msg = repr(msg)

    if int(os.environ.get('DEBUG', 0)):
        (exc_type, exc_val, exc_tb) = sys.exc_info()
        import traceback
        traceback.print_tb(exc_tb)

    sys.stderr.write("{prog}: error: {msg}\n".format(
        prog=os.path.basename(sys.argv[0]),
        msg=str(msg)
    ))
