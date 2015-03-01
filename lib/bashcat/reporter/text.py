#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory
from bashcat.reporter.total import TotalReporter


class TextReporter(TotalReporter):
    def _generator_yield(self, event, stats, **kwargs):
        ret_lines = []

        if event == 'datafile-enter':
            ret_lines.extend([
                self._separator('-'),
                kwargs['datafile'].path,
                self._separator('=')
            ])

        elif event == 'dataline-enter':
            dl = kwargs['dataline']

            flags = [ '-', str(dl.count) ]

            if dl.executable:
                flags[0] = '+'

                if stats['multicount'] > 0:
                    flags[1] = str(stats['multicount'])
            else:
                flags[0] = '#'

            stats['flags'] = flags

        elif event == 'dataline-exit':
            ret_lines.extend([
                "[{0: <4}] {1}".format(
                    "".join(stats['flags']),
                    kwargs['dataline'].source
                )
            ])

        elif event == 'datafile-exit':
            ret_lines.extend([
                self._separator('-'),
                "Lines ({total} [executable {executable}, unexecutable {unexecutable}]), Covered ({covered}), Coverage ({covered%}%)".format(**stats)
            ])

        elif event == 'report-exit':
            ret_lines.extend([
                self._separator('-'),
                super(TextReporter, self)._generator_yield(event, stats, **kwargs)
            ])

        if ret_lines:
            return "\n".join(ret_lines)

        return None


Factory.register('text', TextReporter)
