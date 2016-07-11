
import numpy
import idcpp
import idpy.utils as utils

class CassetteException(Exception):
    pass


class Subblock(object):

    def __init__(self, dim, pos=[0,0,0]):
        cpp_dim = utils._vector_to_CppVector3D(dim)
        cpp_pos = utils._vector_to_CppVector3D(pos)
        self._cppobj = idcpp.Subblock(cpp_dim, cpp_pos)

    def get_matrix(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._cppobj.get_gmatrix(cpp_pos)
        return utils._CppMatrix3D_to_matrix(cpp_matrix)

    @property
    def dim(self):
        cpp_dim = self._cppobj.dim
        return utils._CppVector3D_to_vector(cpp_dim)

    @dim.setter
    def dim(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid dimension value for Subblock object")
        cpp_dim = utils._vector_to_CppVector3D(value)
        self._cppobj.dim = cpp_dim

    @property
    def pos(self):
        cpp_pos = self._cppobj.pos
        return utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid position value for Subblock object")
        cpp_pos = utils._vector_to_CppVector3D(value)
        self._cppobj.pos = cpp_pos


class Block(object):

    def __init__(self, mag, dim, pos=[0,0,0]):
        cpp_mag = utils._vector_to_CppVector3D(mag)
        cpp_dim = utils._vector_to_CppVector3D(dim)
        cpp_pos = utils._vector_to_CppVector3D(pos)
        self._cppobj = idcpp.Block(cpp_mag, cpp_dim, cpp_pos)

    def add_subblock(self, subblock):
        if isinstance(subblock, Subblock):
            self._cppobj.add_subblock(subblock._subblock)
        elif isinstance(subblock, idcpp.Subblock):
            self._cppobj.add_subblock(subblock)

    def get_matrix(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._cppobj.get_gmatrix(cpp_pos)
        return utils._CppMatrix3D_to_matrix(cpp_matrix)

    def get_field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._cppobj.get_field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field

    @property
    def mag(self):
        cpp_mag = self._cppobj.get_mag()
        return utils._CppVector3D_to_vector(cpp_mag)

    @mag.setter
    def mag(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid magnetization value for Block object")
        cpp_mag = utils._vector_to_CppVector3D(value)
        mag = self._cppobj.set_mag()
        mag = cpp_mag

    @property
    def dim(self):
        cpp_dim = self._cppobj.get_dim()
        return utils._CppVector3D_to_vector(cpp_dim)

    @dim.setter
    def dim(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid dimension value for Block object")
        cpp_dim = utils._vector_to_CppVector3D(value)
        dim = self._cppobj.set_dim()
        dim = cpp_dim

    @property
    def pos(self):
        cpp_pos = self._cppobj.get_pos()
        return utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid position value for Block object")
        cpp_pos = utils._vector_to_CppVector3D(value)
        pos = self._cppobj.set_pos()
        pos = cpp_pos


class CassetteCassette(object):

    def __init__(self, block, rot, nr_periods, spacing=0, N=4):
        self.block = block
        self.rot = rot
        self.nr_periods = nr_periods
        self.spacing = spacing
        self.N = N
        cpp_rot = utils._matrix_to_CppMatrix3D(rot)
        self._cppobj = idcpp.CassetteCassette(self.block._cppobj, cpp_rot, self.nr_periods, self.spacing, self.N)

    def set_horizontal_pos(self, h_pos):
        self._cppobj.set_x(h_pos)

    def set_vertical_pos(self, v_pos):
        self._cppobj.set_z(v_pos)

    def set_longitudinal_pos(self, l_pos):
        self._cppobj.set_ycenter(l_pos)



class EPU(object):

    def __init__(self, block, nr_periods, magnetic_gap, cassette_separation, block_separation=0.0):
        self.block = block
        self.nr_periods = nr_periods
        self.magnetic_gap = magnetic_gap
        self.cassette_separation = cassette_separation
        self.block_separation = block_separation
        self._cppobj = idcpp.EPU(self.block._cppobj, self.nr_periods, self.magnetic_gap, self.cassette_separation, self.block_separation)

    def set_phase_csd(self, phase):
        self._cppobj.set_phase_csd(phase)

    def set_phase_cie(self, phase):
        self._cppobj.set_phase_cie(phase)

    def field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._cppobj.field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field


class DELTA(object):

    def __init__(self, block, nr_periods, vertical_gap, horizontal_gap, block_separation=0.0):
        self.block = block
        self.nr_periods = nr_periods
        self.vertical_gap = vertical_gap
        self.horizontal_gap = horizontal_gap
        self.block_separation = block_separation
        self._cppobj = idcpp.DELTA(self.block._cppobj, self.nr_periods, self.vertical_gap, self.horizontal_gap, self.block_separation)

    def set_phase_cs(self, phase):
        self._cppobj.set_phase_cs(phase)

    def set_phase_ci(self, phase):
        self._cppobj.set_phase_ci(phase)

    def field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._cppobj.field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field
