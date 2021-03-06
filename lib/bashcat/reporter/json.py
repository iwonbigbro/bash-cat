#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

from __future__ import absolute_import
import json, os, sys, bashcat.datafile

from json import encoder
encoder.FLOAT_REPR = lambda f: format(f, '.1f')

from bashcat.reporter import BaseReporter, Factory
from bashcat.reporter.total import TotalReporter


class JsonReporter(TotalReporter):
    def __init__(self, *args, **kwargs):
        super(JsonReporter, self).__init__(*args, **kwargs)

        self._data = []
        self._datafile = None
        self._dataline = None


    def _generator_yield(self, event, stats, **kwargs):
        if event == 'datafile-enter':
            df = kwargs['datafile']

            self._datafile = {
                'path': df.path,
                'digest': df.digest,
                'lines': []
            }

        elif event == 'datafile-exit':
            self._datafile.update({
                'summary': {
                    'lines': {
                        'total': stats['total'],
                        'executable': stats['executable'],
                        'unexecutable': stats['unexecutable'],
                        'covered': stats['covered']
                    },
                    'coverage': stats['covered%']
                }
            })
            self._data.append(self._datafile)
            self._datafile = None

        elif event == 'dataline-enter':
            dl = kwargs['dataline']

            self._dataline = { 
                'heredoc': dl.is_heredoc,
                'executable': dl.is_executable,
                'branch': dl.is_branch,
                'count': dl.count,
                'source': dl.source
            }

        elif event == 'dataline-exit':
            self._datafile['lines'].append(self._dataline)
            self._dataline = None

        elif event == 'report-exit':
            return json.dumps(self._data)

        return None


Factory.register('json', JsonReporter)
