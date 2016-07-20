
import unittest
import numpy
import idcpp
import idpy

class TestIDModel(unittest.TestCase):

    def setUp(self):
        mag = [0,1,0]
        pos = [0,0,0]
        dim = [0.06,0.06,0.06]
        block = idpy.cassette.Block(mag, dim, pos)
        nr_periods = 3
        magnetic_gap = 0.005
        cassette_separation = 0.000002
        self.epu = idpy.insertiondevice.EPU(block, nr_periods, magnetic_gap, cassette_separation)

def idmodel_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIDModel)
    return suite

def get_suite():
    suite_list = []
    suite_list.append(idmodel_suite())
    return unittest.TestSuite(suite_list)
