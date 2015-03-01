#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory


class TotalReporter(BaseReporter):
    def _generator_yield(self, event, stats, **kwargs):
        if event == 'report-exit':
            return "\n".join([
                self._separator('-'),
                "({0:.2f}%) covered".format(stats['covered'])
            ])

        return None


Factory.register('total', TotalReporter)
