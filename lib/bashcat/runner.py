#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, fcntl, select, bashcat.recorder


LIB_BASHCAT_DIR = os.path.abspath(os.path.dirname(__file__))
HELPER = os.path.join(LIB_BASHCAT_DIR, 'helper.sh')


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
        frp = select.poll()
        frp.register(fr, select.POLLIN)

        running = True
        recorder = bashcat.recorder.Recorder(self._config['data-dir'])

        # Keep trying to read while waiting for our process.
        while running:
            wpid, wstatus = os.waitpid(pid, os.WNOHANG)
            if wpid != 0:
                running = False

            # Wait for input...
            ready = frp.poll(0.2)
            for fd, evt in ready:
                if not fd or fd != fr.fileno():
                    continue

                # Use our exception handling sync interface to parse the input.
                try:
                    bashcat_line = ""
                    for line in fr.readlines():
                        bashcat_line += line.rstrip('\n').replace('\n', ' ')

                        if bashcat_line.endswith(":::BASHCAT"):
                            recorder.parse(bashcat_line)
                            bashcat_line = ""

                    if bashcat_line:
                        raise Exception("Fragment found with no terminator: '{0}'".format(bashcat_line))

                except IOError:
                    pass

        self._exitcode = os.WEXITSTATUS(wstatus)
        self._signum = os.WTERMSIG(wstatus)


    def executor(self, w):
        os.environ['BASHCAT_FD'] = str(w)
        os.environ['BASH_ENV'] = HELPER

        # Ensure our helper.sh file exists, or bash will ignore it and run the
        # target script without our hooks in place.
        if not os.path.exists(HELPER):
            raise FileNotFoundError(HELPER)

        # Form the command to be executed by bash along with our init file.
        cmd = [ "/bin/bash", self._script ] + self._script_args

        # Ensure our pipe doesn't get closed on exec.
        flags = fcntl.fcntl(w, fcntl.F_GETFD)
        flags &= ~fcntl.FD_CLOEXEC
        fcntl.fcntl(w, fcntl.F_SETFD, flags)

        # Flush the buffers.
        sys.stderr.flush()
        sys.stdout.flush()

        os.execve("/bin/bash", cmd, os.environ)


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
