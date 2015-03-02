#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import os, sys
from bashcat.output import err

optlist = (
    [ "-h", "--help", "", "Display usage summary" ],
    [ "-d", "--data-dir", "path", "Path to data directory (see BASHCAT_DATADIR)" ],
    [ "-T", "--total", "(path|-)", "Write aggregated coverage stats to 'path'" ],
    [ "-t", "--text", "(path|-)", "Write text report to 'path'" ],
    [ "-j", "--json", "(path|-)", "Write HTML report to 'path'" ],
    [ "-H", "--html", "(path|-)", "Write HTML report to 'path'" ]
)


def get_optstr():
    optstr = ""

    for opt in optlist:
        optstr += opt[0][1]

        if opt[2] != "":
            optstr += ":"

    return optstr


def get_optlong():
    optarr = []

    for opt in optlist:
        name, val = opt[1:3]

        if val != "":
            name += "="

        optarr.append(name[2:])

    return optarr


def get_usagestr():
    usage_arr = []

    for opt in optlist:
        usage_arr.append("    %-20s %s" % (" ".join(opt[:3]), opt[3]))

    return "\n".join(usage_arr)


def parse(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv[1:], get_optstr(), get_optlong())
    except getopt.GetoptError as e:
        err(e)
        sys.exit(2)

    opt_map = dict([ opt[:2] for opt in optlist ])
    config = {}

    # Convert short options to long options
    for opt in opts:
        config[opt_map.get(opt[0], opt[0])[2:]] = opt[1]

    config['script'] = None
    config['script_args'] = []

    try:
        config['script'] = args[0]
        config['script_args'] = args[1:]
    except IndexError:
        pass

    if 'data-dir' not in config:
        config['data-dir'] = os.environ.get('BASHCAT_DATADIR',
            os.path.join(os.environ.get('TMPDIR', '/tmp'), 'bash-cat')
        )

    return config
