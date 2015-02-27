#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

class Runner(object):
    def __init__(self, config):
        self._config = config
        self._exitcode = 255

    def run(self):
        pass

    @property
    def exitcode(self):
        return self._exitcode
