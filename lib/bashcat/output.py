#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys

def err(msg):
    sys.stderr.write("{prog}: error: {msg}\n".format(
        prog=os.path.basename(sys.argv[0]),
        msg=str(msg)
    ))
