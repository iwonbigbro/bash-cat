#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile


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


    def _generator_yield(self, event, line_stats, **kwargs):
        return None


    def generator(self):
        covered = 0.0
        count = 0

        yield self._generator_yield('report-enter', None)

        for f in os.listdir(self._datadir):
            abs_f = os.path.join(self._datadir, f)

            try:
                datafile = bashcat.datafile.load(abs_f)
            except UnpickleError:
                bashcat.output.err("failed to load: {0}".format(abs_f))
                continue

            line_stats = {
                'total': len(datafile),
                'covered': 0,
                'executable': 0,
                'unexecutable': 0,
                'multicount': 0,
                'covered%': 0.0,
                'heredoc_start': False,
                'heredoc': None
            }

            yield self._generator_yield('datafile-enter', line_stats, datafile=datafile)

            for dl in datafile.itervalues():
                yield self._generator_yield('dataline-enter', line_stats, dataline=dl)

                if line_stats['heredoc']:
                    line_stats['heredoc_start'] = False

                    if dl.source == line_stats['heredoc']:
                        line_stats['heredoc'] = None

                    line_stats['unexecutable'] += 1
                else:
                    if dl.heredoc:
                        line_stats['heredoc'] = dl.heredoc
                        line_stats['heredoc_start'] = True

                    if dl.is_executable:
                        line_stats['executable'] += 1

                        if line_stats['multicount'] > 0:
                            line_stats['covered'] += 1
                    else:
                        line_stats['unexecutable'] += 1

                    if dl.count > 0:
                        line_stats['covered'] += 1

                        if dl.multiline:
                            line_stats['multicount'] = dl.count
                        else:
                            line_stats['multicount'] = 0

                yield self._generator_yield('dataline-exit', line_stats, dataline=dl)

            if line_stats['executable'] > 0:
                line_stats['covered%'] = (float(line_stats['covered']) / \
                    float(line_stats['executable'])) * 100.0

                covered = line_stats['covered%']

            count += 1

            yield self._generator_yield('datafile-exit', line_stats, datafile=datafile)

        if count > 0:
            covered = (covered / float(count))

        yield self._generator_yield('report-exit', { 'covered':covered, 'filecount':count })


    def _separator(self, char='-'):
        return "".join([ char ] * int(os.environ.get('COLUMNS', 80)))


    def write(self, path):
        if path == "-":
            fd = sys.stdout
            closefd = False
        else:
            fd = open(path, "w")
            closefd = True

        try:
            for line in self.generator():
                if line is not None:
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
                __import__('bashcat.reporter.' + modname,
                        globals(), locals(), [], -1)

                Factory.create(modname, self._datadir).write(
                    self._config[modname]
                )
