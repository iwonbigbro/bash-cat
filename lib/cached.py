#!/usr/bin/env python

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

import threading

class property(object):
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.value = None
        self.lock = threading.RLock()


    def __get__(self, obj, cls):
        if obj is None:
            return self

        with self.lock:
            try:
                cache = obj._cached_property
            except AttributeError:
                cache = obj._cached_property = {}

            try:
                val = obj._cached_property[self.__name__]
            except KeyError:
                val = obj._cached_property.setdefault(self.__name__, self.func(obj))

            return val
