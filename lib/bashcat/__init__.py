#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import sys, os, bashcat.output, bashcat.options, bashcat.runner


def usage():
    sys.stdout.write("""Usage: {prog} [options] [script [script_args...]]
Summary:
    Generate code coverage analysis data and reports from Bash script execution.

Options:
{options}

Environment:
    BASHCAT_DATADIR           Directory to read and write data files.  If the -o
                              option is specified, then the value of this variable
                              is ignored.

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


def report(config):
    return 0


def main(argv=sys.argv):
    config = options.parse(argv)

    if 'help' in config:
        usage()
        sys.exit(0)

    try:
        if ('text', 'json', 'html') in config:
            sys.exit(report(config))

        sys.exit(run(config))

    except Exception as e:
        if os.environ.get('DEBUG', '0') == '1':
            raise

        bashcat.output.err(e)
        sys.exit(2)
