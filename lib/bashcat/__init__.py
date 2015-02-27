#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import sys, os, bashcat.options, bashcat.runner


def usage():
    sys.stdout.write("""Usage: {prog} [options] [script [script_args...]]
Summary:
    Generate code coverage analysis data and reports from Bash script execution.

Options:
{options}

Licence:
    New BSD License (BSD-3)
    
Copyright (C) 2015 Craig Phillips.  All rights reserved.
""".format(
        prog=os.path.basename(sys.argv[0]),
        options=bashcat.options.get_usagestr()
    ))


def run(config):
    runner = bashcat.runner.Runner(config)
    runner.run()
    return runner.exitcode


def main(argv=sys.argv):
    config = options.parse(argv)

    if config.has_key('help'):
        usage()
        sys.exit(0)

    sys.exit(run(config))
