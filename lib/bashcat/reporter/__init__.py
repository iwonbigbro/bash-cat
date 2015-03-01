#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import sys, importlib, bashcat.datafile


report_types = {}

class Factory(object):
    @staticmethod
    def create(report_type, *args, **kwargs):
        return (report_types[report_type])(*args, **kwargs)

    @staticmethod
    def register(report_type, cls):
        report_types[report_type] = cls


class BaseReporter(object):
    def __init__(self, datadir):
        self._datadir = datadir


    def generator(self):
        raise NotImplemented("generator not implemented")


    def write(self, path):
        if path == "-":
            fd = sys.stdout
            closefd = False
        else:
            fd = open(path, "w")
            closefd = True

        try:
            for line in self.generator():
                fd.write(str(line) + "\n")

        finally:
            if closefd:
                fd.close()


class Reporter(object):
    def __init__(self, config):
        self._config = config
        self._datadir = config['data-dir']
        self._modules = ( 'total', 'text', 'html', 'json' )


    def run(self):
        for modname in self._modules:
            if modname in self._config:
                importlib.import_module('bashcat.reporter.' + modname)

                Factory.create(modname, self._datadir).write(
                    self._config[modname]
                )
