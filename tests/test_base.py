#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests.test_base
'''
:author:    madkote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2019, madkote

tests.test_base
---------------
Package
'''

from __future__ import absolute_import

import unittest

VERSION = (1, 0, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2019, madkote'


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base(self):
        '''Currently ther is not much to test '''


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
