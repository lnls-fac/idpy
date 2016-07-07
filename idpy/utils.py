
import numpy
import idcpp


def _vector_to_CppVector3D(vector):
    v = numpy.array(vector)
    CppVector3D = idcpp.CppVector3D()
    CppVector3D.x = float(v[0])
    CppVector3D.y = float(v[1])
    CppVector3D.z = float(v[2])
    return CppVector3D

def _matrix_to_CppVectorVector3D(matrix):
    m = numpy.array(matrix)
    CppVectorVector3D = idcpp.CppVectorVector3D()
    for i in range(len(m)):
        CppVectorVector3D.push_back(_vector_to_CppVector3D(m[i]))
    return CppVectorVector3D

def _matrix_to_CppMatrix3D(matrix):
    m = numpy.array(matrix)
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

def _CppMatrix3D_to_matrix(CppMatrix3D):
    m = []
    for i in range(3):
        m.append(_CppVector3D_to_vector(CppMatrix3D.row(i)))
    matrix = numpy.array(m)
    return matrix


rotx90p = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotx90p())
rotx90n = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotx90n())
roty90p = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_roty90p())
roty90n = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_roty90n())
rotz90p = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotz90p())
rotz90n = _CppMatrix3D_to_matrix(idcpp.CppMatrix3D_rotz90n())
