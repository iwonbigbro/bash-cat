#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import fcntl, copy, os, sys, hashlib, pickle, re, string, bashcat.output


class DataLine(object):
    def __init__(self, source):
        self._source = source.rstrip('\n')
        self._data = {}
        self._modified = False
        self._maskinit = [ 0 ] * len(source)
        self._masklen = len(self._maskinit)
        self._mask = self._maskinit[:]
        self._count = 0
        self._multiline = False

        if self._source.endswith('\\'):
            self._multiline = True


    @property
    def multiline(self):
        return self._multiline


    @property
    def source(self):
        return self._source


    @property
    def executable(self):
        src = self._source
        m = re.search(r'^([^#]*)#.*$', src)

        if m is not None:
            src = m.group(1)

        if src.strip():
            return True

        return False


    def sync(self):
        if not self._modified:
            return

        mask = self._maskinit[:]
        count = 0

        for v in self._data.itervalues():
            count += v['count']
            vmask = v['mask']
            
            for i in xrange(self._masklen):
                mask[i] |= vmask[i]

        self._mask = mask
        self._count = count
        self._modified = False


    def update(self, statement):
        pid = os.getpid()

        try:
            val = self._data[pid]
        except KeyError:
            val = self._data.setdefault(pid, {
                'count': 0,
                'mask': self._maskinit[:]
            })

        self._modified = True

        val['count'] += 1
        valmask = val['mask']
        offset = string.find(self.source, statement)

        if -1 != offset:
            for i in xrange(offset, offset + len(statement)):
                valmask[i] = 1


    @property
    def count(self):
        self.sync()
        return self._count

    
    @property
    def mask(self):
        self.sync()
        return self._mask


    def merge(self, line):
        if self is line:
            return self._modified

        self._modified = True

        for pid, v in line._data.iteritems():
            sv = self._data.get(pid)

            if sv is None:
                self._data[pid] = copy.deepcopy(v)
                continue

            if v['count'] > sv['count']:
                sv['count'] = v['count']

            vmask = v['mask']
            svmask = sv['mask']

            if vmask != svmask:
                for i in xrange(self._masklen):
                    svmask[i] |= vmask[i]

        return self._modified


    def value(self):
        return { 'source':self.source, 'count':self.count, 'mask':self.mask }


class DataFile(object):
    def __init__(self, srcfile, lineno, branch, line, datadir):
        self._srcfile = srcfile
        self._datadir = datadir
        self._datafile = os.path.join(datadir, hashlib.sha1(srcfile).hexdigest())
        self._modified = False

        self._lines = {}

        with open(srcfile, "r") as f:
            sha = hashlib.sha1()
            srclineno = 0
            
            for srcline in f:
                sha.update(srcline)

                srclineno += 1
                self._lines[srclineno] = DataLine(srcline)

            self._digest = sha.hexdigest()

        if not os.path.exists(datadir):
            os.mkdir(datadir, 0700)

        self.sync()
        self.update(srcfile, lineno, branch, line)


    def __len__(self):
        return len(self._lines)


    @property
    def digest(self):
        return self._digest


    @property
    def path(self):
        return self._srcfile


    def iteritems(self):
        for k, v in self._lines.iteritems():
            yield k, v


    def itervalues(self):
        for v in self._lines.itervalues():
            yield v


    def merge(self, datafile):
        if self._digest != datafile.digest:
            return self._modified

        for k, v in datafile.iteritems():
            if self._lines.setdefault(k, v).merge(v):
                self._modified = True
        
        return self._modified


    def update(self, srcfile, lineno, branch, line):
        try:
            dataline = self._lines[int(lineno)]
        except:
            bashcat.output.err(
                "{0}: invalid line number '{1}'".format(srcfile, lineno)
            )
            return

        dataline.update(branch)

        self._modified = True


    def sync(self):
        # Open the file with write access, creating if it doesn't exist.
        fd = os.open(self._datafile, os.O_CREAT | os.O_RDWR)
        f = os.fdopen(fd, "r+")

        fcntl.lockf(fd, fcntl.LOCK_EX)

        try:
            try:
                datafile = pickle.load(f)

                if datafile.digest == self.digest:
                    self.merge(datafile)

            except Exception as e:
                sys.stderr.write("error: " + str(e))
                pass

            if self._modified:
                for dl in self._lines.itervalues():
                    dl.sync()

                self._modified = False

            f.seek(0)
            pickle.dump(self, f)

        finally:
            # Unlock and close the file.
            f.close()


    def value(self):
        return [ dl.value() for dl in self._lines.values() ]


def load(datafile):
    with open(datafile) as fd:
        return pickle.load(fd)
