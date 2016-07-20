
import unittest
import numpy
import idcpp
import idpy

class TestUtils(unittest.TestCase):

    def test_rotx90p(self):
        m = numpy.array([[1,0,0],[0,0,-1],[0,1,0]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.rotx90p[i][j])

    def test_rotx90n(self):
        m = numpy.array([[1,0,0],[0,0,1],[0,-1,0]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.rotx90n[i][j])

    def test_roty90p(self):
        m = numpy.array([[0,0,1],[0,1,0],[-1,0,0]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.roty90p[i][j])

    def test_roty90n(self):
        m = numpy.array([[0,0,-1],[0,1,0],[1,0,0]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.roty90n[i][j])

    def test_rotz90p(self):
        m = numpy.array([[0,-1,0],[1,0,0],[0,0,1]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.rotz90p[i][j])

    def test_rotz90n(self):
        m = numpy.array([[0,1,0],[-1,0,0],[0,0,1]])
        for i in range(numpy.size(m,0)):
            for j in range(numpy.size(m,1)):
                self.assertEqual(m[i][j], idpy.utils.rotz90n[i][j])

    def test_vector_to_CppVector3D(self):
        vector = [9.5928364,5.383864352,0]
        CppVector3D = idpy.utils._vector_to_CppVector3D(vector)
        self.assertIsInstance(CppVector3D, idcpp.CppVector3D)
        self.assertEqual(vector[0], CppVector3D.x)
        self.assertEqual(vector[1], CppVector3D.y)
        self.assertEqual(vector[2], CppVector3D.z)

        vector = [0,0,0,0]
        with self.assertRaises(idpy.utils.UtilsException):
            CppVector3D = idpy.utils._vector_to_CppVector3D(vector)

    def test_matrix_to_CppVectorVector3D(self):
        vector = [9.5928364,5.383864352,0]
        matrix = [vector, vector]
        CppVectorVector3D = idpy.utils._matrix_to_CppVectorVector3D(matrix)
        self.assertIsInstance(CppVectorVector3D, idcpp.CppVectorVector3D)
        self.assertEqual(matrix[0][0], CppVectorVector3D[0].x)
        self.assertEqual(matrix[0][1], CppVectorVector3D[0].y)
        self.assertEqual(matrix[0][2], CppVectorVector3D[0].z)

        matrix = [0,0,0]
        with self.assertRaises(idpy.utils.UtilsException):
            CppVectorVector3D = idpy.utils._matrix_to_CppVectorVector3D(matrix)

        matrix = [[0,0,0], [0,0]]
        with self.assertRaises(idpy.utils.UtilsException):
            CppVectorVector3D = idpy.utils._matrix_to_CppVectorVector3D(matrix)


    def test_matrix_to_CppMatrix3D(self):
        v1 = [9.5928364,5.383864352,0]
        v2 = [3.258262,6.82743673,1.204784]
        v3 = [0,5.27363,0.282945]
        matrix = [v1, v2, v3]
        CppMatrix3D = idpy.utils._matrix_to_CppMatrix3D(matrix)
        self.assertIsInstance(CppMatrix3D , idcpp.CppMatrix3D)
        self.assertEqual(matrix[0][0], CppMatrix3D.row(0).x)
        self.assertEqual(matrix[0][1], CppMatrix3D.row(0).y)
        self.assertEqual(matrix[0][2], CppMatrix3D.row(0).z)
        self.assertEqual(matrix[0][0], CppMatrix3D.column(0).x)
        self.assertEqual(matrix[1][0], CppMatrix3D.column(0).y)
        self.assertEqual(matrix[2][0], CppMatrix3D.column(0).z)

        matrix = [0,0,0]
        with self.assertRaises(idpy.utils.UtilsException):
            CppMatrix3D = idpy.utils._matrix_to_CppMatrix3D(matrix)

        matrix = [[0,0,0], [0,0,0]]
        with self.assertRaises(idpy.utils.UtilsException):
            CppMatrix3D = idpy.utils._matrix_to_CppMatrix3D(matrix)

    def test_matrix_to_CppDoubleVectorVector(self):
        vector = [9.5928364,5.383864352]
        matrix = [vector, vector]
        CppDoubleVectorVector = idpy.utils._matrix_to_CppDoubleVectorVector(matrix)
        self.assertIsInstance(CppDoubleVectorVector, idcpp.CppDoubleVectorVector)
        self.assertEqual(matrix[0][0], CppDoubleVectorVector[0][0])
        self.assertEqual(matrix[0][1], CppDoubleVectorVector[0][1])

    def test_CppVector3D_to_vector(self):
        vector = [9.5928364,5.383864352,0]
        CppVector3D = idpy.utils._vector_to_CppVector3D(vector)
        new_vector = idpy.utils._CppVector3D_to_vector(CppVector3D)
        self.assertIsInstance(new_vector, numpy.ndarray)
        for i in range(len(vector)):
            self.assertEqual(vector[i], new_vector[i])

    def test_CppVectorVector3D_to_matrix(self):
        vector = [9.5928364,5.383864352,0]
        matrix = [vector, vector]
        CppVectorVector3D = idpy.utils._matrix_to_CppVectorVector3D(matrix)
        new_matrix = idpy.utils._CppVectorVector3D_to_matrix(CppVectorVector3D)
        self.assertIsInstance(new_matrix, numpy.ndarray)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.assertEqual(matrix[i][j], new_matrix[i][j])

    def test_CppDoubleVectorVector_to_matrix(self):
        vector = [9.5928364,5.383864352,0]
        matrix = [vector, vector]
        CppDoubleVectorVector = idpy.utils._matrix_to_CppDoubleVectorVector(matrix)
        new_matrix = idpy.utils._CppDoubleVectorVector_to_matrix(CppDoubleVectorVector)
        self.assertIsInstance(new_matrix, numpy.ndarray)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.assertEqual(matrix[i][j], new_matrix[i][j])

    def test_CppMatrix3D_to_matrix(self):
        vector = [9.5928364,5.383864352,0]
        matrix = [vector, vector, vector]
        CppMatrix3D = idpy.utils._matrix_to_CppMatrix3D(matrix)
        new_matrix = idpy.utils._CppMatrix3D_to_matrix(CppMatrix3D)
        self.assertIsInstance(new_matrix, numpy.ndarray)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.assertEqual(matrix[i][j], new_matrix[i][j])

    def test_rotation_matrix(self):
        m = idpy.utils.get_rotation_matrix_x(numpy.pi/4)
        self.assertAlmostEqual(m[0][0], 1)
        self.assertAlmostEqual(m[0][1], 0)
        self.assertAlmostEqual(m[0][2], 0)
        self.assertAlmostEqual(m[1][0], 0)
        self.assertAlmostEqual(m[1][1], 0.7071067811865476)
        self.assertAlmostEqual(m[1][2], -0.7071067811865476)
        self.assertAlmostEqual(m[2][0], 0)
        self.assertAlmostEqual(m[2][1], 0.7071067811865476)
        self.assertAlmostEqual(m[2][2], 0.7071067811865476)

        m = idpy.utils.get_rotation_matrix_x(numpy.pi/8)
        self.assertAlmostEqual(m[0][0], 1)
        self.assertAlmostEqual(m[0][1], 0)
        self.assertAlmostEqual(m[0][2], 0)
        self.assertAlmostEqual(m[1][0], 0)
        self.assertAlmostEqual(m[1][1], 0.9238795325112867)
        self.assertAlmostEqual(m[1][2], -0.3826834323650898)
        self.assertAlmostEqual(m[2][0], 0)
        self.assertAlmostEqual(m[2][1], 0.3826834323650898)
        self.assertAlmostEqual(m[2][2], 0.9238795325112867)

        m = idpy.utils.get_rotation_matrix_y(numpy.pi/8)
        self.assertAlmostEqual(m[0][0], 0.9238795325112867)
        self.assertAlmostEqual(m[0][1], 0)
        self.assertAlmostEqual(m[0][2], 0.3826834323650898)
        self.assertAlmostEqual(m[1][0], 0)
        self.assertAlmostEqual(m[1][1], 1)
        self.assertAlmostEqual(m[1][2], 0)
        self.assertAlmostEqual(m[2][0], -0.3826834323650898)
        self.assertAlmostEqual(m[2][1], 0)
        self.assertAlmostEqual(m[2][2], 0.9238795325112867)

        m = idpy.utils.get_rotation_matrix_z(numpy.pi/8)
        self.assertAlmostEqual(m[0][0], 0.9238795325112867)
        self.assertAlmostEqual(m[0][1], -0.3826834323650898)
        self.assertAlmostEqual(m[0][2], 0)
        self.assertAlmostEqual(m[1][0], 0.3826834323650898)
        self.assertAlmostEqual(m[1][1], 0.9238795325112867)
        self.assertAlmostEqual(m[1][2], 0)
        self.assertAlmostEqual(m[2][0], 0)
        self.assertAlmostEqual(m[2][1], 0)
        self.assertAlmostEqual(m[2][2], 1)


def utils_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    return suite

def get_suite():
    suite_list = []
    suite_list.append(utils_suite())
    return unittest.TestSuite(suite_list)
