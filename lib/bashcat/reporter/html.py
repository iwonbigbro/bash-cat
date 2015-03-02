#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import base64, os, re, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory
from bashcat.reporter.json import JsonReporter


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


def get_filecontents(path):
    with open(path, "r") as fd:
        return "".join(fd.readlines())


class HtmlReporter(JsonReporter):
    def __init__(self, *args, **kwargs):
        super(HtmlReporter, self).__init__(*args, **kwargs)

        self._gen_html = []
        self._data_index = None

        with open(os.path.join(DATA_DIR, 'index.html')) as fd:
            for line in fd:
                line = line.strip()

                if line.startswith('<link '):
                    m = re.search(r' href="([^"]+)" ', line)
                    if m is not None:
                        content = get_filecontents(os.path.join(DATA_DIR, m.group(1)))
                        self._gen_html.append(
                            '<style type="text/css">\n' + content + '\n</style>'
                        )
                        continue

                if line.startswith('<input id="bash-cat-data" '):
                    self._data_index = len(self._gen_html)

                if line.startswith('<script type="text/javascript" src='):
                    m = re.search(r' src="([^"]+)"', line)
                    if m is not None:
                        content = get_filecontents(os.path.join(DATA_DIR, m.group(1)))
                        self._gen_html.append(
                            '<script type="text/javascript">' + content + '</script>'
                        )
                        continue

                self._gen_html.append(line)


    def _generator_yield(self, event, stats, **kwargs):
        ret = super(HtmlReporter, self)._generator_yield(event, stats, **kwargs)

        if event == 'report-exit':
            encoded_json = base64.standard_b64encode(ret)
            self._gen_html[self._data_index] = \
                '<input id="bash-cat-data" type="hidden" value="{0}"/>'.format(
                    encoded_json
                )

            return self._gen_html[0] + "\n" + "\n".join(self._gen_html[1:])


Factory.register('html', HtmlReporter)
