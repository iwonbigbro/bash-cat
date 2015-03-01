#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys, bashcat.datafile

from bashcat.reporter import BaseReporter, Factory
from bashcat.reporter.total import TotalReporter


class HtmlReporter(TotalReporter):
    pass


Factory.register('html', HtmlReporter)
