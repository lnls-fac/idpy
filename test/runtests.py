#!/usr/bin/env python3

import unittest
import test_utils
import test_cassette
import test_insertiondevice

suite_list = []
suite_list.append(test_utils.get_suite())
suite_list.append(test_cassette.get_suite())
suite_list.append(test_insertiondevice.get_suite())

tests = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(tests)
