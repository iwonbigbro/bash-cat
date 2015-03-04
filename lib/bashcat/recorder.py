#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, bashcat.datafile, bashcat.output


class RecorderException(Exception):
    pass


class Recorder(object):
    def __init__(self, datadir):
        self._datadir = datadir
        self._datafiles = {}
        self._errors = {}

    
    def parse(self, bashcat_line):
        if not bashcat_line.startswith("BASHCAT:::") \
        and bashcat_line.endswith(":::BASHCAT"):
            bashcat.output.err('Invalid line: ' + bashcat_line)
            return

        info = bashcat_line.split(":::")
        info[1] = srcfile = os.path.abspath(info[1])

        try:
            self._datafiles[srcfile].update(*info[1:])
            return

        except KeyError:
            pass

        try:
            self._datafiles[srcfile] = \
                bashcat.datafile.DataFile(*info[1:], datadir=self._datadir)
            return

        except IOError as e:
            if not self._errors.get(srcfile):
                self._errors[srcfile] = True
                bashcat.output.err(e)
            pass

        except Exception as e:
            bashcat.output.err(e)
            pass


    def __del__(self):
        for df in self._datafiles.itervalues():
            df.sync()
