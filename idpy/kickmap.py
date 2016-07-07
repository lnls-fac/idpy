
import idcpp
import utils

class Grid(object):

    def __init__(self, nx, ny, xmin, xmax, ymin, ymax):
        self.nx = nx
        self.ny = ny
        self._grid = idcpp.Grid(self.nx, self.ny, xmin, xmax, ymin, ymax)
        self.x = self._grid.x
        self.y = self._grid.y


class Mask(object):

    def __init__(self, shape=None, width=None, height=None, filename=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.filename = filename
        if self.shape is not None:
            self._mask = idcpp.Mask(self.shape, self.width, self.height)
        elif self.filename is not None:
            self._mask = idcpp.Mask(self.filename)

    def is_inside(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        return self._mask.is_inside(cpp_pos)


class KickMap(object):

    def __init__(self, fieldmap, grid, mask, energy, step):
        self.fieldmap = fieldmap
        self.grid = grid
        self.mask = mask
        self.energy = energy
        self.step = step
        self._kickmap = idcpp.KickMap(self.fieldmap._fieldmap ,self.grid._grid, self.mask._mask, self.energy, self.step)

    def write_to_file(filename):
        self._kickmap.write_kickmap(filename)
