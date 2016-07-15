
import numpy
import idcpp


class UtilsException(Exception):
    pass


def _vector_to_CppVector3D(vector):
    v = numpy.array(vector)
    if len(v) != 3: raise UtilsException("Can't convert vector to CppVector3D object")
    CppVector3D = idcpp.CppVector3D()
    CppVector3D.x = float(v[0])
    CppVector3D.y = float(v[1])
    CppVector3D.z = float(v[2])
    return CppVector3D

def _matrix_to_CppVectorVector3D(matrix):
    m = numpy.array(matrix)
    if not isinstance(m[0], (list, tuple, numpy.ndarray)) or len(m[0]) != 3:
        raise UtilsException("Can't convert matrix to CppVectorVector3D object")
    CppVectorVector3D = idcpp.CppVectorVector3D()
    for i in range(len(m)):
        CppVectorVector3D.push_back(_vector_to_CppVector3D(m[i]))
    return CppVectorVector3D

def _matrix_to_CppDoubleVectorVector(matrix):
    m = numpy.array(matrix)
    CppDoubleVectorVector = idcpp.CppDoubleVectorVector()
    for i in range(len(m)):
        CppDoubleVectorVector.push_back(idcpp.CppDoubleVector(m[i]))
    return CppDoubleVectorVector

def _matrix_to_CppMatrix3D(matrix):
    m = numpy.array(matrix)
    if len(m) != 3 or not isinstance(m[0], (list, tuple, numpy.ndarray)) or len(m[0]) != 3:
        raise UtilsException("Can't convert matrix to CppMatrix3D object")
    vx_cpp = _vector_to_CppVector3D(m[0])
    vy_cpp = _vector_to_CppVector3D(m[1])
    vz_cpp = _vector_to_CppVector3D(m[2])
    CppMatrix3D = idcpp.CppMatrix3D(vx_cpp, vy_cpp, vz_cpp)
    return CppMatrix3D

def _CppVector3D_to_vector(CppVector3D):
    v = []
    v.append(CppVector3D.x)
    v.append(CppVector3D.y)
    v.append(CppVector3D.z)
    vector = numpy.array(v)
    return vector

def _CppVectorVector3D_to_matrix(CppVectorVector3D):
    m = []
    for i in range(CppVectorVector3D.size()):
        m.append(_CppVector3D_to_vector(CppVectorVector3D[i]))
    matrix = numpy.array(m)
    return matrix

def _CppDoubleVectorVector_to_matrix(CppDoubleVectorVector):
    m = []
    for i in range(CppDoubleVectorVector.size()):
        m.append(numpy.array(CppDoubleVectorVector[i]))
    matrix = numpy.array(m)
    return matrix

def _CppMatrix3D_to_matrix(CppMatrix3D):
    m = []
    for i in range(3):
        m.append(_CppVector3D_to_vector(CppMatrix3D.row(i)))
    matrix = numpy.array(m)
    return matrix

def get_rotation_matrix_x(angle):
    I = idcpp.CppMatrix3D.I()
    I.set_rotation_x(angle)
    return _CppMatrix3D_to_matrix(I)

def get_rotation_matrix_y(angle):
    I = idcpp.CppMatrix3D.I()
    I.set_rotation_y(angle)
    return _CppMatrix3D_to_matrix(I)

def get_rotation_matrix_z(angle):
    I = idcpp.CppMatrix3D.I()
    I.set_rotation_z(angle)
    return _CppMatrix3D_to_matrix(I)


rotx90p  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotx90p())
rotx90n  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotx90n())
roty90p  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_roty90p())
roty90n  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_roty90n())
rotz90p  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotz90p())
rotz90n  = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotz90n())
