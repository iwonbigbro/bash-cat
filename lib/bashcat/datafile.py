#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import fcntl, copy, os, sys, hashlib, pickle, re, string
import cached, bashcat.output


class NotFoundError(Exception):
    pass


class DataLine(object):
    def __init__(self, source, prev=None):
        self._source = source.rstrip('\n')
        self._data = {}
        self._modified = False
        self._maskinit = [ 0 ] * len(source)
        self._masklen = len(self._maskinit)
        self._mask = self._maskinit[:]
        self._count = 0
        self._multiline = False
        self._heredoc = None

        # Create a linked list so that lines can reference their
        # siblings, ancestors and descendents.
        self._prev = prev
        self._next = None

        if prev is not None:
            prev._next = self

        if self._source.endswith('\\'):
            self._multiline = True

        m = re.search(r" <<-?'?([^']+)'?", self._source)
        if m is not None:
            self._heredoc = m.group(1)


    def preceding(self, filter=None):
        prev = self._prev

        while prev is not None:
            if not callable(filter) or filter(prev):
                return prev

            prev = prev._prev

        raise NotFoundError("No preceding sibling")


    def following(self, filter=None):
        next = self._next

        while next is not None:
            if not callable(filter) or filter(prev):
                return prev

            next = next._next

        raise NotFoundError("No following sibling")


    @property
    def heredoc(self):
        return self._heredoc


    @property
    def multiline(self):
        return self._multiline


    @property
    def source(self):
        return self._source


    @cached.property
    def stripped_source(self):
        src = self._source.strip()
        m = re.search(r'^([^#]*)#.*$', src)

        if m is not None:
            src = m.group(1).strip()

        return src


    @cached.property
    def is_branch(self):
        src = self.stripped_source
        if not src:
            return False

        return (re.search(r'\s*(then|else|;;|in|do)\s*$', src) is not None)


    @cached.property
    def is_executable(self):
        src = self.stripped_source
        if not src:
            return False

        # Bash case statements are ayntactically heavy, with little in
        # the way of runtime interpretation.  We need to specialise these
        # blocks and filter out the pattern logic and decoration.
        try:
            preceding_keyword = \
                self.preceding(lambda x: x.is_branch or x.is_executable) \
                    .command_keyword()

            if preceding_keyword in ('in', ';;'):
                keyword = self.command_keyword(is_case=True, before=';;')
                if keyword is None:
                    return False

                # Denotes a case statement branch.
                return True

        except NotFoundError:
            pass

        # Some statements are closing statements and are just syntax
        # directives to bash.  Therefore, they do not get executed at
        # runtime and should be excluded.
        src = re.sub(r'\s*(fi|then|else|;;|esac|in|do|done)\s*;?', r'', src).strip()
        if not src:
            return False

        return True


    def command_keyword(self, **kwargs):
        src = self._source

        if kwargs.get('is_case'):
            # Match everything after the first unescaped closing bracket.
            m = re.search(r'^(?:\\\)|[^\)])+\)(\s+\S+.*)?$', self._source)
            if m is not None:
                src = m.group(1)
                if src is None:
                    return None

            if src == 'esac':
                return None

        before = kwargs.get('before')
        if before is not None:
            m = re.search(r'^(.*)' + before, src)
            if m is not None:
                src = m.group(1).strip()

        # Default: Obtain the command keyword from the current line.
        m = re.search(r'(\S+)\s*$', src)
        if m is not None:
            return m.group(1)

        return None


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
    def __init__(self, srcfile, lineno, branch, line, *args, **kwargs):
        self._srcfile = srcfile
        self._datadir = kwargs['datadir']
        self._datafile = os.path.join(self._datadir, hashlib.sha1(srcfile).hexdigest())
        self._modified = False

        self._lines = {}

        with open(srcfile, "r") as f:
            sha = hashlib.sha1()
            srclineno = 0

            dl_prev = None
            
            for srcline in f:
                sha.update(srcline)

                dl_curr = DataLine(srcline, dl_prev)

                srclineno += 1
                self._lines[srclineno] = dl_prev = dl_curr

            self._digest = sha.hexdigest()

        if not os.path.exists(self._datadir):
            os.makedirs(self._datadir, 0700)

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


    def update(self, srcfile, lineno, branch, line, *args, **kwargs):
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
        fd = os.open(self._datafile, os.O_CREAT | os.O_RDWR)
        f = os.fdopen(fd, "r+")

        fcntl.lockf(fd, fcntl.LOCK_EX)

        try:
            try:
                datafile = pickle.load(f)

                if datafile.digest == self.digest:
                    self.merge(datafile)

            except EOFError:
                pass

            except Exception as e:
                raise

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
