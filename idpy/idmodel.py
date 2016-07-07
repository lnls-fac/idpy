
import idcpp
import utils

class Subblock(object):

    def __init__(self, dim, pos):
        self.dim = dim
        self.pos = pos
        cpp_dim = utils._vector_to_CppVector3D(self.dim)
        cpp_pos = utils._vector_to_CppVector3D(self.pos)
        self._subblock = idcpp.Subblock(cpp_dim, cpp_pos)

    def get_matrix(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._subblock.get_gmatrix(cpp_pos)
        return utils._CppMatrix3D_to_matrix(cpp_matrix)

class Block(object):

    def __init__(self, mag, dim, pos):
        self.mag = mag
        self.dim = dim
        self.pos = pos
        cpp_mag = utils._vector_to_CppVector3D(self.mag)
        cpp_dim = utils._vector_to_CppVector3D(self.dim)
        cpp_pos = utils._vector_to_CppVector3D(self.pos)
        self._block = idcpp.Block(cpp_mag, cpp_dim, cpp_pos)

    def add_subblock(self, subblock):
        if isinstance(subblock, Subblock):
            self._block.add_subblock(subblock._subblock)
        elif isinstance(subblock, idcpp.Subblock):
            self._block.add_subblock(subblock)

    def get_matrix(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._block.get_gmatrix(cpp_pos)
        return utils._CppMatrix3D_to_matrix(cpp_matrix)

    def get_field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._block.get_field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field

class HalbachCassette(object):

    def __init__(self, block, rot, nr_periods, spacing=0, N=4):
        self.block = block
        self.rot = rot
        self.nr_periods = nr_periods
        self.spacing = spacing
        self.N = N
        cpp_rot = utils._matrix_to_CppMatrix3D(rot)
        self._halbachcassete = idcpp.HalbachCassette(self.block._block, cpp_rot, self.nr_periods, self.spacing, self.N)

    def set_horizontal_pos(self, h_pos):
        self._halbachcassete.set_x(h_pos)

    def set_vertical_pos(self, v_pos):
        self._halbachcassete.set_z(v_pos)

    def set_longitudinal_pos(self, l_pos):
        self._halbachcassete.set_ycenter(l_pos)


class EPU(object):

    def __init__(self, block, nr_periods, magnetic_gap, cassette_separation, block_separation=0.0):
        self.block = block
        self.nr_periods = nr_periods
        self.magnetic_gap = magnetic_gap
        self.cassette_separation = cassette_separation
        self.block_separation = block_separation
        self._epu = idcpp.EPU(self.block._block, self.nr_periods, self.magnetic_gap, self.cassette_separation, self.block_separation)

    def set_phase_csd(self, phase):
        self._epu.set_phase_csd(phase)

    def set_phase_cie(self, phase):
        self._epu.set_phase_cie(phase)

    def get_field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._epu.get_field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field

class DELTA(object):

    def __init__(self, block, nr_periods, vertical_gap, horizontal_gap, block_separation=0.0):
        self.block = block
        self.nr_periods = nr_periods
        self.vertical_gap = vertical_gap
        self.horizontal_gap = horizontal_gap
        self.block_separation = block_separation
        self._delta = idcpp.DELTA(self.block._block, self.nr_periods, self.vertical_gap, self.horizontal_gap, self.block_separation)

    def set_phase_cs(self, phase):
        self._epu.set_phase_cs(phase)

    def set_phase_ci(self, phase):
        self._epu.set_phase_ci(phase)

    def get_field(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        cpp_field = self._epu.get_field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field
