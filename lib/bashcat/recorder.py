#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, bashcat.datafile, bashcat.output


class RecorderException(Exception):
    pass


class Recorder(object):
    def __init__(self, datadir):
        self._datadir = datadir
        self._datafiles = {}

    
    def parse(self, bashcat_line):
        if not bashcat_line.startswith("BASHCAT:::") \
        and bashcat_line.endswith(":::BASHCAT"):
            raise RecorderException("invalid line '{0}'".format(bashcat_line))

        info = bashcat_line.split(":::")
        srcfile = os.path.abspath(info[1])
        info[1] = srcfile

        try:
            self._datafiles[srcfile].update(*info[1:])
            return

        except KeyError:
            pass

        try:
            self._datafiles[srcfile] = \
                bashcat.datafile.DataFile(*info[1:], datadir=self._datadir)
            return

        except TypeError as e:
            bashcat.output.err(e)
            bashcat.output.err("  line: '{0}'".format(bashcat_line))
            raise


    def __del__(self):
        for df in self._datafiles.itervalues():
            df.sync()
