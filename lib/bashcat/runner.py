#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os


class Runner(object):
    def __init__(self, config):
        self._pid = os.getpid()
        self._config = config
        self._exitcode = 255

        
    def monitor(self, r):
        fr = os.fdopen(r)
        os.waitpid(pid, 0)


    def executor(self, w):
        os.environ['BASHCAT_FD'] = w
        os.execv("/bin/bash", [ self._config['script'] ] + self._config['script_args'])


    def run(self):
        r, w = os.pipe()
        pid = os.fork()

        if pid == 0:
            # Child
            os.close(r)
            self.executor(w)

        # Parent
        os.close(w)
        self.monitor(r)


    @property
    def exitcode(self):
        return self._exitcode
