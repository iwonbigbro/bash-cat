#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, bashcat.datafile


class RecorderException(Exception):
    pass


class Recorder(object):
    def __init__(self, datadir):
        self._datadir = datadir
        self._datafiles = {}

    
    def parse(self, bashcat_line):
        if not bashcat_line.startswith("BASHCAT:::"):
            raise RecorderException("invalid line '{0}'".format(bashcat_line))

        info = bashcat_line.split(":::")
        srcfile = os.path.abspath(info[1])
        info[1] = srcfile

        try:
            self._datafiles[srcfile].update(*info[1:])

        except KeyError:
            self._datafiles[srcfile] = \
                bashcat.datafile.DataFile(*info[1:], datadir=self._datadir)


    def __del__(self):
        for df in self._datafiles.itervalues():
            df.sync()
