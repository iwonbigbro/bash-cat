#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory


class TotalReporter(BaseReporter):
    def generator(self):
        covered = 0.0
        count = 0

        for f in os.listdir(self._datadir):
            abs_f = os.path.join(self._datadir, f)

            try:
                datafile = bashcat.datafile.load(abs_f)
            except UnpickleError:
                bashcat.output.err("failed to load: {0}".format(abs_f))
                continue

            lines_tot = len(datafile)
            lines_cov = 0
            lines_exec = 0

            for dl in datafile.itervalues():
                if dl.executable:
                    lines_exec += 1

                if dl.count > 0:
                    lines_cov += 1

            datafile_cov = (float(lines_cov) / float(lines_exec)) * 100.0
            covered += datafile_cov
            count += 1

        yield "(%.2f%%) covered" % (covered / count)


Factory.register('total', TotalReporter)
