
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

    def test_copy(self):
        dim = [1,2,3]
        pos = [4,5,6]
        subblock = idpy.cassette.Subblock(dim, pos)
        new_subblock = idpy.cassette.Subblock(subblock=subblock)
        new_subblock.dim = [10,10,10]
        self.assertEqual(subblock.dim[0], 1)
        self.assertEqual(subblock.dim[1], 2)
        self.assertEqual(subblock.dim[2], 3)


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

    def test_field(self):
        # Compared with Radia results
        places = 9

        # cube pos = [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.001,0.001], pos=[0,0,0])
        field = block.field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], 0.12736521535044731, places=places)
        self.assertAlmostEqual(field[1], 0.028643724981960564, places=places)
        self.assertAlmostEqual(field[2], 0.07750508014388427, places=places)

        # rectangle pos = [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0,0,0])
        field = block.field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], -0.015850129558094617, places=places)
        self.assertAlmostEqual(field[1], -0.25777020111156573, places=places)
        self.assertAlmostEqual(field[2], -0.0718890758980946, places=places)

        # rectangle pos != [0,0,0]
        block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0.004,0.005,0.006])
        field = block.field([0.00052, 0.0006, 0.0007])
        self.assertAlmostEqual(field[0], 0.0017288710940030474, places=places)
        self.assertAlmostEqual(field[1], 0.00042510633728255455, places=places)
        self.assertAlmostEqual(field[2], 0.0009985839853064408, places=places)

        # # rectangle pos = vertex
        # block = idpy.cassette.Block(mag=[-0.5,1,0.7], dim=[0.001,0.002,0.003], pos=[0,0,0])
        # field = block.field([0.001/2, 0.002/2, 0.003/2])
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

class TestHalbachCassette(unittest.TestCase):

    def setUp(self):
        mag = [0,1,0]
        pos = [0,0,0]
        rot = idpy.utils.rotx90p
        nr_periods = 3

        dim = [0.06,0.06,0.06]
        self.block_cube = idpy.cassette.Block(mag, dim, pos)
        self.cassette_cube = idpy.cassette.HalbachCassette(self.block_cube, rot, nr_periods)

        dim = [0.06,0.08,0.07]
        self.block_rectangle = idpy.cassette.Block(mag, dim, pos)
        self.cassette_rectangle = idpy.cassette.HalbachCassette(self.block_rectangle, rot, nr_periods)

    def test_block_attributes(self):
        block = self.cassette_cube.genblock
        self.assertIsInstance(block, idpy.cassette.Block)
        self.assertEqual(block.mag[0], self.block_cube.mag[0])
        self.assertEqual(block.mag[1], self.block_cube.mag[1])
        self.assertEqual(block.mag[2], self.block_cube.mag[2])
        self.assertEqual(block.dim[0], self.block_cube.dim[0])
        self.assertEqual(block.dim[1], self.block_cube.dim[1])
        self.assertEqual(block.dim[2], self.block_cube.dim[2])
        self.assertEqual(block.pos[0], self.block_cube.pos[0])
        self.assertEqual(block.pos[1], self.block_cube.pos[1])
        self.assertEqual(block.pos[2], self.block_cube.pos[2])

    def test_set_pos(self):
        cassette = idpy.cassette.HalbachCassette(halbachcassette=self.cassette_cube)
        dim = cassette.get_dim()

        cassette.set_horizontal_pos(100)
        cassette.set_vertical_pos(-5)
        cassette.set_longitudinal_pos(8)
        center_pos = cassette.center_pos
        block_pos = cassette.first_block_pos
        self.assertEqual(cassette.genblock.pos[0], 100)
        self.assertEqual(cassette.genblock.pos[1], -5)
        self.assertEqual(cassette.genblock.pos[2], 8 - dim[2]/2)
        self.assertEqual(center_pos[0], 100)
        self.assertEqual(center_pos[1], -5)
        self.assertEqual(center_pos[2], 8)
        self.assertEqual(block_pos[0], 100)
        self.assertEqual(block_pos[1], -5)
        self.assertEqual(block_pos[2], 8 - dim[2]/2)

        cassette.first_block_pos = [0,0,0]
        center_pos = cassette.center_pos
        block_pos = cassette.first_block_pos
        self.assertEqual(block_pos[0], 0)
        self.assertEqual(block_pos[1], 0)
        self.assertEqual(block_pos[2], 0)
        self.assertEqual(center_pos[2], 0 + dim[2]/2)


    def test_field_vertcial_direction(self):
        # Compared with Radia results
        places = 9

        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        x = 0
        y = 0.08

        Bx_radia = [1.30049e-13, -7.74818e-14, -2.98265e-13, -1.44998e-13,
                    4.62064e-14, 3.48942e-13, 2.49594e-13, 3.44542e-13,
                    2.70621e-13, -3.43085e-13, -6.25783e-13, -2.05004e-13,
                    -1.98829e-13, -9.70776e-14, -9.34111e-14]

        By_radia = [0.04050762672019437, 0.008339898219329745, -0.00894114471014558,
                    -0.005305145921854352, 0.0025769853669985257, 0.01622673647452067,
                    0.000217664816845019, -0.01571376781824713, -0.0017719872174590697,
                    0.006872303601084662, 0.012578619074111308, 0.0014462410865854498,
                    -0.015643013367579433, -0.005335392051906099, -0.02691940857413397]

        Bz_radia = [0.005467054395763381, 0.012673998232596063, 0.012659031851578212,
                    -0.006486218981472727, -0.005852639651378765, 0.005833903581001741,
                    0.004525573401882199, 0.005330194442501681,  -0.007015750430349238,
                    -0.008698569246270157,  0.008636251540939952, 0.006219853821507807,
                    0.0045896812696729185, 0.010180228920163972, 0.0029232033842000885]

        for i in range(len(z)):
            field = self.cassette_cube.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)

    def test_field_horizontal_direction(self):
        # Compared with Radia results
        places = 9

        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        x = 0.08
        y = 0

        Bx_radia = [-0.02267583536929591, -0.004893689584375202, 0.044502981397780174,
                    0.03657696072735495, -0.02530730385131446, -0.044114530587223436,
                    0.00021766486800510465, 0.04462749931464614, 0.026112301975111663,
                    -0.035009802933447375, -0.04086550714792656, 0.014679828853431227,
                    0.04754044875130907, 0.01953722773478487, -0.02492887408306263]

        By_radia = [-0.02668584217652007, -0.007462622850768515, 0.017663994450641624,
                    0.01452770996897797, -0.010768445258060918, -0.021124954091209437,
                    3.0588996796769314e-11, 0.021124954133026935, 0.01076844527369537,
                    -0.014527709932459514, -0.017663994472947517, 0.007462622836390941,
                    0.026685842188568728, 0.017968676881478518, 0.007084838685975191]

        Bz_radia = [-0.0016867571583455015, -0.034390945350447, -0.014357606712345355,
                    0.028264259031775003, 0.03518156676800467, -0.008110306990898947,
                    -0.041018628217512246, -0.008614016061706066, 0.034018455969522125,
                    0.02605190880176584, -0.018380386939093836, -0.04084508983255506,
                    -0.002564130283190331, 0.03500980553496835, 0.013842640429851982]

        for i in range(len(z)):
            field = self.cassette_cube.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)


    def test_field_arbitrary_direction(self):
        # Compared with Radia results
        places = 9

        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        x = 0.07
        y = 0.07

        Bx_radia = [0.015239086466337622, 0.005984533747553157,
                    -0.00016914845278838262, -0.0005436752828819708,
                    0.0013089779955117512, 0.0036146572073705394,
                    0.00017906184459031262, -0.0031973120545974445,
                    -0.0006742157960213232, 0.0017153035724593666,
                    0.0026514816073519563, -0.0003488648962614955,
                    -0.004694983208436868, -0.005999313789114221,
                    -0.012637062966347638]

        By_radia = [0.001011948155698075, 0.0015759148783509877,
                    0.007897940455371772, 0.006244980359662474, -0.004047447325958433,
                    -0.0065536198725253255, 0.00017906186358674112,
                    0.00697096505533258, 0.004682209541869015, -0.0050733520543975626,
                    -0.005415607310466083, 0.004059753964915015, 0.009532155104659597,
                    0.004959068559419961, -0.007411712410503368]

        Bz_radia = [7.076159910430747e-6, -0.000053057299851446614,
                    0.002043204397668986, 0.003762439977567161, 0.00419852764600375,
                    0.00031624325449553095, -0.004063230242454286,
                    -0.00012250081295737025, 0.003213327385329202,
                    0.0019955723076551133, -0.0008025069150555627,
                    -0.003431240533888704, 0.002319253579581008, 0.010065344968708183,
                    0.00484410409783074]

        for i in range(len(z)):
            field = self.cassette_cube.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)

    # def test_field_inside_blocks(self):
    #     # Compared with Radia results
    #     places = 9
    #
    #     z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
    #     x = 0.02
    #     y = 0.01
    #
    #     Bx_radia = [0.008360536195792303, -0.0419406308963095, 0.106721516945529,
    #                 0.15569795511284806, -0.10827120868599616, -0.05488638236945871,
    #                 0.00006079038578511785, 0.055032759915610005, 0.10851536825201567,
    #                 -0.15516882114443895, -0.1052245096303979, 0.048111798541887026,
    #                 0.03942137631399532, 0.04720750870084145, -0.13215781046358085]
    #
    #     By_radia = [0.6838176356035767, -0.06859221478849603, -0.7057767854766674,
    #                 -0.7664798577792293, -0.1488072012169997, 0.6771283137169212,
    #                 0.00003039536709614007, -0.6770551250687963, 0.14892927967242878,
    #                 -0.2332555802686458, 0.7065251939703954, 0.0716736254599617,
    #                 -0.6610135102998642, 0.1070387676123912, -0.03667834274532688]
    #
    #     Bz_radia = [0.10168726783566287, 0.7465175677989531, 0.2549853918504647,
    #                 -0.4605097108950627, -0.6486450794557929, 0.10787505324987284,
    #                 0.7453362580975897, 0.1072335856205666, -0.65020645236017,
    #                 -0.463835967767599, 0.2472882735493802, 0.7240666485292824,
    #                 -0.0025076039698680164, -0.7239083495082733, -0.25250935652850187]
    #
    #     for i in range(len(z)):
    #         field = self.cassette_cube.field([x,y,z[i]])
    #         self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
    #         self.assertAlmostEqual(field[1], By_radia[i], places=places)
    #         self.assertAlmostEqual(field[2], Bz_radia[i], places=places)

    def test_field_rectangular_block(self):
        # Compared with Radia results
        places = 9

        x = 0.07
        y = 0.09
        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]

        Bx_radia = [
            0.016424277530419782, 0.007154771556406419,
            0.00039029390313573644, -0.0039588910563416,
            0.00006601469637097492, 0.0037767058769945998,
            0.004695936397874936, 0.00015146468300237436,
            -0.004356353562821242, -0.003309297702610594,
            0.0006878357652581031, 0.005329416740797426,
            0.0023377063356237776, -0.001529265058365573,
            -0.0066827406938958205, -0.006172727552882329,
            -0.011476920206438087
        ]
        By_radia = [
            0.004859969636660026, 0.002111901329473888, 0.006360603503739992,
            0.005638710275473825, 0.002163907897239742, -0.004291985240902977,
            -0.004485752938318748, 0.00019352635980213724,
            0.0049192800405609294, 0.004887300896420193,
            -0.0012074395204480697, -0.00390997578553378,
            -0.0029509683808509406, 0.004821557431205883,
            0.0069447716647040286, 0.004765086834031235, -0.007275923271958545
        ]
        Bz_radia = [
            0.0006265905515855832, 0.0023304193332510737,
            0.0024169963118642825, 0.0021239366008861393,
            0.0041782842497147445, 0.0012571639548221538,
            0.0007424600848474972, -0.002581675811747594,
            0.0003741193168782884, 0.0004531600739135287,
            0.0027911012324712547, -0.00007906975238024467,
            -0.0007832716577587857, -0.001035320638811146,
            0.002704488547569129, 0.008262428945787267, 0.008038694706564115
        ]

        for i in range(len(z)):
            field = self.cassette_rectangle.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)

        pos = []
        for i in range(len(z)):
            pos.append([x,y,z[i]])
        field = self.cassette_rectangle.field(pos)

        for i in range(len(field)):
            self.assertAlmostEqual(field[i][0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[i][1], By_radia[i], places=places)
            self.assertAlmostEqual(field[i][2], Bz_radia[i], places=places)

    def test_field_without_x_symmetry(self):
        # Compared with Radia results
        places = 8

        pos = [0.01,0,0]
        self.cassette_rectangle.first_block_pos = pos

        x = 0.05
        y = 0.05
        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]


        Bx_radia = [0.13927830767840257, 0.0001535416870135407,
                    -0.00041145479657350763, -0.09717936658388202,
                    0.006769376002273104, 0.037433808864478446, 0.07512751098424003,
                    0.00009760692384337277, -0.07490504393729365,
                    -0.037112926326347905, -0.006210358156721235, 0.09832723817837069,
                    0.0032201105144855154, 0.008369509375153612, -0.10627068862214141,
                    0.0021015807491625293, -0.06913468740523643]

        By_radia = [0.021656337672974663, -0.036724434061261656,
                    0.056877201075925914, 0.01352198443466437, 0.02321607467411651,
                    -0.044868371851654834, -0.02562392083201124,
                    0.00012120887062121902, 0.025899912962794484,
                    0.045265345724613916, -0.022527762977584423,
                    -0.012119755526587738, -0.05349603670915245, 0.04667571079516587,
                    0.014501837445968242, 0.05502997921055581, -0.05816559438206288]

        Bz_radia = [0.025268075464705646, -0.0004732699557123156,
                    0.022199996947266924, -0.019354710946583885, 0.034040672318710136,
                    -0.04035276516698687, 0.04118503108133826, -0.036984166172887134,
                    0.0407066791212218, -0.04143840744934202, 0.032017151299398944,
                    -0.023060525945562044, 0.015103991362735443,
                    -0.014754059165147325, 0.002305105049877767, 0.028083102672821485,
                    0.04048624626256832]

        for i in range(len(z)):
            field = self.cassette_rectangle.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)


    def test_field_without_y_symmetry(self):
        # Compared with Radia results
        places = 8

        pos = [0,-0.02, 0]
        self.cassette_rectangle.first_block_pos = pos

        x = 0.04
        y = 0.04
        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]

        Bx_radia = [0.08709072805816237, 0.008552602463039473,
                    -0.0075349697472185785, -0.0561523592461848,
                    0.0015127422699841863, 0.026793522553039267, 0.04471933930079376,
                    0.00009614176725464269, -0.04450068257558006,
                    -0.026480067450119125, -0.000972196955544976, 0.05724421619360677,
                    0.010130388564428817, -0.0011198169705533513,
                    -0.06228591560507851, -0.007516789786476071, -0.04168744531989118]

        By_radia = [0.039889723536948585, -0.01604994506675768, 0.028032760584092133,
                    -0.006705602454958126, 0.014026388276034968, -0.01645414479991868,
                    -0.0027024153244977656, 0.00014327336573287885,
                    0.0030279535609697475, 0.016919547801398472, -0.01322749307941622,
                    0.008307164243823398, -0.02427681692999307, 0.026531508822903366,
                    -0.006248705194736727, 0.031162725335980447, -0.04345954887323778]

        Bz_radia = [0.017119251265400825, 0.009204310723599283, 0.019448388248476743,
                    -0.011529449104827182, 0.016669503644822663,
                    -0.024106359961451673, 0.02583708647229474, -0.018344061218375576,
                    0.025373925101160856, -0.02515229850067376, 0.014739239127083222,
                    -0.014999945560385003, 0.013036187722605069,
                    -0.0027112814847867883, 0.003001104735131717, 0.01692021307398986,
                    0.027732406887236292]

        for i in range(len(z)):
            field = self.cassette_rectangle.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)

    def test_nr_of_magnetization_directions(self):
        # Compared with Radia results
        places = 8

        mag = [0,1,0]
        pos = [0,0,0]
        dim = [0.06,0.06,0.06]
        block = idpy.cassette.Block(mag, dim, pos)
        nr_periods = 1

        N = 8
        rot = idpy.utils.get_rotation_matrix_x(math.pi/4)
        cassette = idpy.cassette.HalbachCassette(block, rot, nr_periods, N=N)

        x = 0.04
        y = 0.04
        z = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]

        Bx_radia = [0.13876533926413737, 0.09392118167732041, 0.01900865577392811,
                    -0.03682950120958159, -0.08617998382148755, -0.11813579148255404,
                    -0.08660787496285002, -0.0059906864980112, 0.05733145296237398,
                    0.006010236220633004]

        By_radia = [0.006242403596663436, -0.019359972121980037,
                    -0.01470008218448996, 0.021283063149685588, 0.04301436172235289,
                    0.03388320636483008, 0.023822398036941878, 0.017642121401946816,
                    0.00015420929009101608, -0.04489821380869929]

        Bz_radia = [0.004242734637426785, 0.0018316349770404364,
                    0.014985389114742209, 0.022597251319797885, -0.003212240130798907,
                    -0.010550538890278247, 0.0023010613417717395, 0.00109493428163078,
                    -0.0066150877059689035, 0.044432940087220485]

        for i in range(len(z)):
            field = cassette.field([x,y,z[i]])
            self.assertAlmostEqual(field[0], Bx_radia[i], places=places)
            self.assertAlmostEqual(field[1], By_radia[i], places=places)
            self.assertAlmostEqual(field[2], Bz_radia[i], places=places)


def subblock_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSubblock)
    return suite

def block_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlock)
    return suite

def halbach_cassette_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHalbachCassette)
    return suite

def get_suite():
    suite_list = []
    suite_list.append(subblock_suite())
    suite_list.append(block_suite())
    suite_list.append(halbach_cassette_suite())
    return unittest.TestSuite(suite_list)
