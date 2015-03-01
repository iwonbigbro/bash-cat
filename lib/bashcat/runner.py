#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, fcntl, select, bashcat.recorder


LIB_BASHCAT_DIR = os.path.abspath(os.path.dirname(__file__))
RCFILE = os.path.join(LIB_BASHCAT_DIR, 'rcfile.sh')


class RunnerException(Exception):
    pass


class Runner(object):
    def __init__(self, config):
        self._config = config
        self._exitcode = 1
        self._signum = 0
        self._script = config['script']
        self._script_args = config['script_args']

        if self._script is None:
            raise RunnerException("Missing 'script'")

        
    def monitor(self, r, pid):
        fr = os.fdopen(r)
        running = True
        recorder = bashcat.recorder.Recorder(self._config['data-dir'])

        # Keep trying to read while waiting for our process.
        while running:
            wpid, wstatus = os.waitpid(pid, os.WNOHANG)
            if wpid != 0:
                running = False

            # Wait for input...
            if not select.select([ r ], [], [], 0.1)[0]:
                continue

            # Use our exception handling sync interface to parse the input.
            try:
                for line in fr.readlines():
                    recorder.parse(line.rstrip('\n'))
            except IOError:
                pass

        self._exitcode = os.WEXITSTATUS(wstatus)
        self._signum = os.WTERMSIG(wstatus)


    def executor(self, w):
        os.environ['BASHCAT_FD'] = str(w)

        # Ensure our rcfile.sh file exists, or bash will ignore it and run the
        # target script without our hooks in place.
        if not os.path.exists(RCFILE):
            raise FileNotFoundError(RCFILE)

        # Form the command to be executed by bash along with our init file.
        cmd = [
            "/bin/bash",
                "--debugger",
                "--noprofile",
                "--init-file", RCFILE,
                "-i",
                self._script
        ] + self._script_args

        # Ensure our pipe doesn't get closed on exec.
        flags = fcntl.fcntl(w, fcntl.F_GETFD)
        flags &= ~fcntl.FD_CLOEXEC
        fcntl.fcntl(w, fcntl.F_SETFD, flags)

        # Flush the buffers.
        sys.stderr.flush()
        sys.stdout.flush()

        os.execv("/bin/bash", cmd)


    def run(self):
        r, w = os.pipe()
        pid = os.fork()

        if pid == 0:
            # Child
            os.close(r)
            self.executor(w)

        # Parent
        os.close(w)
        self.monitor(r, pid)


    @property
    def exitcode(self):
        return self._exitcode
