
import unittest
import numpy
import math
import idcpp
import idpy

def get_xyz(r, pos, dim):
    x = [(pos[0] - r[0] - dim[0]/2), (pos[0] - r[0] + dim[0]/2)]
    y = [(pos[1] - r[1] - dim[1]/2), (pos[1] - r[1] + dim[1]/2)]
    z = [(pos[2] - r[2] - dim[2]/2), (pos[2] - r[2] + dim[2]/2)]
    return x, y, z

def get_Qxx(r, pos, dim):
    Qxx = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xx = (-1)**(i+j+k+1)
                try:
                    Qxx += (1/(4*math.pi))*sign_xx*math.atan(y[j]*z[k]*(1/(x[i]*sqrt)))
                except ZeroDivisionError:
                    if y[j]*z[k] != 0:
                        Qxx += (1/(4*math.pi))*sign_xx*(math.pi/2)
                    else:
                        Qxx = numpy.nan
    return Qxx

def get_Qyy(r, pos, dim):
    Qyy = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xx = (-1)**(i+j+k+1)
                try:
                    Qyy += (1/(4*math.pi))*sign_xx*math.atan(x[i]*z[k]*(1/(y[j]*sqrt)))
                except ZeroDivisionError:
                    if x[i]*z[k] != 0:
                        Qyy += (1/(4*math.pi))*sign_xx*(math.pi/2)
                    else:
                        Qyy = numpy.nan
    return Qyy

def get_Qzz(r, pos, dim):
    Qzz = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xx = (-1)**(i+j+k+1)
                try:
                    Qzz += (1/(4*math.pi))*sign_xx*math.atan(y[j]*x[i]*(1/(z[k]*sqrt)))
                except ZeroDivisionError:
                    if y[j]*x[i] != 0:
                        Qzz += (1/(4*math.pi))*sign_xx*(math.pi/2)
                    else:
                        Qzz = numpy.nan
    return Qzz

def get_Qxy(r, pos, dim):
    Qxy = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xy = (-1)**(i+j+k)
                try:
                    Qxy += (1/(4*math.pi))*sign_xy*math.log((z[k]+sqrt))
                except ValueError:
                    Qxy = numpy.nan
    return Qxy

def get_Qxz(r, pos, dim):
    Qxz = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xy = (-1)**(i+j+k)
                try:
                    Qxz += (1/(4*math.pi))*sign_xy*math.log((y[j]+sqrt))
                except ValueError:
                    Qxz = numpy.nan
    return Qxz

def get_Qyz(r, pos, dim):
    Qyz = 0
    x, y, z = get_xyz(r, pos, dim)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sqrt = math.sqrt( x[i]**2 + y[j]**2 + z[k]**2 )
                sign_xy = (-1)**(i+j+k)
                try:
                    Qyz += (1/(4*math.pi))*sign_xy*math.log((x[i]+sqrt))
                except ValueError:
                    Qyz = numpy.nan
    return Qyz


class TestSubblock(unittest.TestCase):

    def test_dimension(self):
        subblock = idpy.cassette.Subblock(dim=[1,2,3])
        cpp_dim = subblock._cppobj.dim
        for i in range(len(subblock.dim)):
            self.assertEqual(subblock.dim[i], idpy.utils._CppVector3D_to_vector(cpp_dim)[i])

    def test_dimension_setter(self):
        subblock = idpy.cassette.Subblock(dim=[1,2,3])
        subblock.dim = [0,0,0]
        cpp_dim = subblock._cppobj.dim
        for i in range(len(subblock.dim)):
            self.assertEqual(subblock.dim[i], idpy.utils._CppVector3D_to_vector(cpp_dim)[i])

    def test_position(self):
        subblock = idpy.cassette.Subblock(dim=[1,2,3], pos=[4,5,6])
        cpp_pos = subblock._cppobj.pos
        for i in range(len(subblock.pos)):
            self.assertEqual(subblock.pos[i], idpy.utils._CppVector3D_to_vector(cpp_pos)[i])

    def test_position_setter(self):
        subblock = idpy.cassette.Subblock(dim=[1,2,3], pos=[4,5,6])
        subblock.pos = [0,0,0]
        cpp_pos = subblock._cppobj.pos
        for i in range(len(subblock.pos)):
            self.assertEqual(subblock.pos[i], idpy.utils._CppVector3D_to_vector(cpp_pos)[i])

    def test_get_matrix(self):
        places = 15
        dim = [1,2,3]
        pos = [4,5,6]
        subblock = idpy.cassette.Subblock(dim, pos)
        r = [1,1,1]
        matrix = subblock.get_matrix(r)
        self.assertAlmostEqual(matrix[0][0], -get_Qxx(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[1][1], -get_Qyy(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[2][2], -get_Qzz(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[0][1], -get_Qxy(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[0][1], -get_Qxy(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[0][2], -get_Qxz(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[2][0], -get_Qxz(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[1][2], -get_Qyz(r, pos, dim), places=places)
        self.assertAlmostEqual(matrix[2][1], -get_Qyz(r, pos, dim), places=places)

class TestBlock(unittest.TestCase):

    def test_magnetization(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6])
        cpp_mag = block._cppobj.get_mag()
        for i in range(len(block.mag)):
            self.assertEqual(block.mag[i], idpy.utils._CppVector3D_to_vector(cpp_mag)[i])

    def test_magnetization_setter(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6])
        block.mag = [0,0,0]
        cpp_mag = block._cppobj.get_mag()
        for i in range(len(block.mag)):
            self.assertEqual(block.mag[i], idpy.utils._CppVector3D_to_vector(cpp_mag)[i])

    def test_dimension(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6])
        block.dim = [0,0,0]
        cpp_dim = block._cppobj.get_dim()
        for i in range(len(block.dim)):
            self.assertEqual(block.dim[i], idpy.utils._CppVector3D_to_vector(cpp_dim)[i])

    def test_dimension_setter(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6])
        cpp_dim = block._cppobj.get_dim()
        for i in range(len(block.dim)):
            self.assertEqual(block.dim[i], idpy.utils._CppVector3D_to_vector(cpp_dim)[i])

    def test_position(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6], pos=[7,8,9])
        cpp_pos = block._cppobj.get_pos()
        for i in range(len(block.pos)):
            self.assertEqual(block.pos[i], idpy.utils._CppVector3D_to_vector(cpp_pos)[i])

    def test_position(self):
        block = idpy.cassette.Block(mag=[1,2,3], dim=[4,5,6], pos=[7,8,9])
        block.pos = [0,0,0]
        cpp_pos = block._cppobj.get_pos()
        for i in range(len(block.pos)):
            self.assertEqual(block.pos[i], idpy.utils._CppVector3D_to_vector(cpp_pos)[i])

    def test_get_field(self):
        # Compared with Radia results
        places = 9

        # cube pos = [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.001,0.001], pos=[0,0,0])
        field = block.get_field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], 0.12736521535044731, places=places)
        self.assertAlmostEqual(field[1], 0.028643724981960564, places=places)
        self.assertAlmostEqual(field[2], 0.07750508014388427, places=places)

        # rectangle pos = [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0,0,0])
        field = block.get_field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], -0.015850129558094617, places=places)
        self.assertAlmostEqual(field[1], -0.25777020111156573, places=places)
        self.assertAlmostEqual(field[2], -0.0718890758980946, places=places)

        # rectangle pos != [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0.004,0.005,0.006])
        field = block.get_field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], 0.0017288710940030474, places=places)
        self.assertAlmostEqual(field[1], 0.00042510633728255455, places=places)
        self.assertAlmostEqual(field[2], 0.0009985839853064408, places=places)

        # # rectangle pos = vertex
        # block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0,0,0])
        # field = block.get_field([0.001/2, 0.002/2, 0.003/2])
        # self.assertAlmostEqual(field[0], 3.1366084983194256, places=places)
        # self.assertAlmostEqual(field[1], 0.3845155172399829, places=places)
        # self.assertAlmostEqual(field[2], 0.800948614051739, places=places)

    def test_get_matrix(self):
        places = 15
        mag = [1,0,0]
        dim = [1,2,3]
        pos = [0,0,0]
        block = idpy.cassette.Block(mag, dim, pos)

        r = [1/2, 2/2, 3/2]
        matrix = block.get_matrix(r)
        Qxx = get_Qxx(r, pos, dim)
        Qyy = get_Qyy(r, pos, dim)
        Qzz = get_Qzz(r, pos, dim)
        Qxy = get_Qxy(r, pos, dim)
        Qxz = get_Qxz(r, pos, dim)
        Qyz = get_Qyz(r, pos, dim)
        if numpy.isnan(Qxx): self.assertTrue(numpy.isnan(matrix[0][0]))
        else: self.assertAlmostEqual(matrix[0][0], -Qxx, places=places)
        if numpy.isnan(Qyy): self.assertTrue(numpy.isnan(matrix[1][1]))
        else: self.assertAlmostEqual(matrix[1][1], -Qyy, places=places)
        if numpy.isnan(Qzz): self.assertTrue(numpy.isnan(matrix[2][2]))
        else: self.assertAlmostEqual(matrix[2][2], -Qzz, places=places)
        if numpy.isnan(Qxy):
            self.assertTrue(numpy.isnan(matrix[0][1]))
            self.assertTrue(numpy.isnan(matrix[1][0]))
        else:
            self.assertAlmostEqual(matrix[0][1], -Qxy, places=places)
            self.assertAlmostEqual(matrix[1][0], -Qxy, places=places)
        if numpy.isnan(Qxz):
            self.assertTrue(numpy.isnan(matrix[0][2]))
            self.assertTrue(numpy.isnan(matrix[2][0]))
        else:
            self.assertAlmostEqual(matrix[0][2], -Qxz, places=places)
            self.assertAlmostEqual(matrix[2][0], -Qxz, places=places)
        if numpy.isnan(Qyz):
            self.assertTrue(numpy.isnan(matrix[1][2]))
            self.assertTrue(numpy.isnan(matrix[2][1]))
        else:
            self.assertAlmostEqual(matrix[1][2], -Qyz, places=places)
            self.assertAlmostEqual(matrix[2][1], -Qyz, places=places)

        r = [0.9, 0.8, 0.7]
        matrix = block.get_matrix(r)
        Qxx = get_Qxx(r, pos, dim)
        Qyy = get_Qyy(r, pos, dim)
        Qzz = get_Qzz(r, pos, dim)
        Qxy = get_Qxy(r, pos, dim)
        Qxz = get_Qxz(r, pos, dim)
        Qyz = get_Qyz(r, pos, dim)
        if numpy.isnan(Qxx): self.assertTrue(numpy.isnan(matrix[0][0]))
        else: self.assertAlmostEqual(matrix[0][0], -Qxx, places=places)
        if numpy.isnan(Qyy): self.assertTrue(numpy.isnan(matrix[1][1]))
        else: self.assertAlmostEqual(matrix[1][1], -Qyy, places=places)
        if numpy.isnan(Qzz): self.assertTrue(numpy.isnan(matrix[2][2]))
        else: self.assertAlmostEqual(matrix[2][2], -Qzz, places=places)
        if numpy.isnan(Qxy):
            self.assertTrue(numpy.isnan(matrix[0][1]))
            self.assertTrue(numpy.isnan(matrix[1][0]))
        else:
            self.assertAlmostEqual(matrix[0][1], -Qxy, places=places)
            self.assertAlmostEqual(matrix[1][0], -Qxy, places=places)
        if numpy.isnan(Qxz):
            self.assertTrue(numpy.isnan(matrix[0][2]))
            self.assertTrue(numpy.isnan(matrix[2][0]))
        else:
            self.assertAlmostEqual(matrix[0][2], -Qxz, places=places)
            self.assertAlmostEqual(matrix[2][0], -Qxz, places=places)
        if numpy.isnan(Qyz):
            self.assertTrue(numpy.isnan(matrix[1][2]))
            self.assertTrue(numpy.isnan(matrix[2][1]))
        else:
            self.assertAlmostEqual(matrix[1][2], -Qyz, places=places)
            self.assertAlmostEqual(matrix[2][1], -Qyz, places=places)


def subblock_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSubblock)
    return suite

def block_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlock)
    return suite

def get_suite():
    suite_list = []
    suite_list.append(subblock_suite())
    suite_list.append(block_suite())
    return unittest.TestSuite(suite_list)
