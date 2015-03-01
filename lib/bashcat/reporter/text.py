#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory


class TextReporter(BaseReporter):
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

            yield "".join([ "-" ] * int(os.environ.get('COLUMNS', 80)))
            yield datafile.path
            yield "".join([ "=" ] * int(os.environ.get('COLUMNS', 80)))

            lines_tot = len(datafile)
            lines_cov = 0
            lines_exec = 0

            for dl in datafile.itervalues():
                flags = [ ' ',' ' ]
                dl.source

                if dl.executable:
                    flags[0] = 'e'
                    flags[1] = str(dl.count)

                    if not dl.multiline:
                        lines_exec += 1

                if dl.count > 0:
                    lines_cov += 1

                yield "[{0}] {1}".format("".join(flags), dl.source)

            datafile_cov = (float(lines_cov) / float(lines_exec)) * 100.0
            covered += datafile_cov
            count += 1

            yield "".join([ "-" ] * int(os.environ.get('COLUMNS', 80)))
            yield "Lines ({0} [executable {1}, non-executable {2}]), Covered ({3}), Coverage ({4}%)".format(
                lines_tot,
                lines_exec,
                lines_tot - lines_exec,
                lines_cov,
                datafile_cov
            )

        yield "".join([ "-" ] * int(os.environ.get('COLUMNS', 80)))
        yield "(%.2f%%) covered" % (covered / float(count))


Factory.register('text', TextReporter)
