
import numpy as _numpy
import idcpp as _idcpp
import idpy.utils as _utils


class Magnet(object):

    def field(self, pos):
        if isinstance(pos[0], (float, int)):
            cpp_pos = _utils._vector_to_CppVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = _utils._CppVector3D_to_vector(cpp_field)
        else:
            cpp_pos = _utils._matrix_to_CppVectorVector3D(pos)
            cpp_field = self._cppobj.field_vector(cpp_pos)
            field = _utils._CppVectorVector3D_to_matrix(cpp_field)
        return field

    @property
    def xmin(self):
        return self._cppobj.get_xmin()

    @property
    def xmax(self):
        return self._cppobj.get_xmax()

    @property
    def ymin(self):
        return self._cppobj.get_ymin()

    @property
    def ymax(self):
        return self._cppobj.get_ymax()

    @property
    def zmin(self):
        return self._cppobj.get_zmin()

    @property
    def zmax(self):
        return self._cppobj.get_zmax()

    @property
    def physical_length(self):
        return self._cppobj.get_physical_length()


class Grid(object):

    def __init__(self, nx, ny, xmin, xmax, ymin, ymax):
        self._cppobj = _idcpp.Grid(nx, ny, xmin, xmax, ymin, ymax)

    @property
    def nx(self):
        return self._cppobj.nx

    @property
    def ny(self):
        return self._cppobj.ny

    @property
    def x(self):
        cpp_x = self._cppobj.x
        return list(cpp_x)

    @property
    def y(self):
        cpp_y = self._cppobj.y
        return list(cpp_y)


class Mask(object):

    valid_shapes = ["ELLIPSE", "RECTANGLE", "DIAMOND", "TABLE", "NONE"]

    def __init__(self, shape=None, width=0.0, height=0.0, filename=None):
        if shape is not None:
            if shape.upper() not in valid_shapes:
                raise Exception("Invalid shape")
            else:
                self._cppobj = _idcpp.Mask(shape.upper(), width, height)
        elif filename is not None:
            self._cppobj = _idcpp.Mask(filename)
        elif shape is None and filename is None:
            self._cppobj = _idcpp.Mask("NONE", width, height)

    def is_inside(self, pos):
        cpp_pos = _utils._vector_to_CppVector3D(pos)
        return self._cppobj.is_inside(cpp_pos)


class KickMap(object):

    def __init__(self, id_length=None, x=None, y=None, kick_x=None, kick_y=None, kickmap=None):
        if kickmap is not None:
            if isinstance(kickmap, KickMap):
                self._cppobj = _idcpp.KickMap(kickmap._cppobj)
            elif isinstance(kickmap, _idcpp.KickMap):
                self._cppobj = _idcpp.KickMap(kickmap)
            else:
                raise Exception("Invalid argument for KickMap constructor")
        else:
            cpp_x = _idcpp.CppDoubleVector(x)
            cpp_y = _idcpp.CppDoubleVector(y)
            cpp_kick_x = _utils._matrix_to_CppDoubleVectorVector(kick_x)
            cpp_kick_y = _utils._matrix_to_CppDoubleVectorVector(kick_y)
            self._cppobj = _idcpp.KickMap(id_length, cpp_x, cpp_y, cpp_kick_x, cpp_kick_y)

    @property
    def id_length(self):
        return self._cppobj.id_length

    @property
    def x(self):
        return list(self._cppobj.x)

    @property
    def y(self):
        return list(self._cppobj.y)

    @property
    def kick_x(self):
        return _utils._CppDoubleVectorVector_to_matrix(self._cppobj.kick_x)

    @property
    def kick_y(self):
        return _utils._CppDoubleVectorVector_to_matrix(self._cppobj.kick_y)

    def write_to_file(self, filename):
        f = open(filename, 'w')
        print("# KICKMAP", file=f)
        print("# Author: Luana N. P. Vilela @ LNLS, Date: ", file=f)
        print("# ID Length [m]", file=f)
        print(self.id_length, file=f)
        print("# Number of Horizontal Points",file=f)
        print(len(self.x), file=f)
        print("# Number of Vertical Points",file=f)
        print(len(self.y), file=f)

        print("# Horizontal KickTable in T2m2", file=f)
        print("START", file=f)
        print(' '*13, end ='', file=f)
        for j in range(len(self.x)):
            print('%+e'%self.x[j], end=' ', file=f)
        print('\n', end='', file=f)
        for i in range(len(self.y)):
            print('%+e'%self.y[i], end=' ', file=f)
            for j in range(len(self.x)):
                if _numpy.isnan(self.kick_x[i,j]):
                    print('%+e'%self.kick_x[i,j] + ' '*9, end=' ', file=f)
                else:
                    print('%+e'%self.kick_x[i,j], end=' ', file=f)
            print('\n', end='', file =f)

        print("# Vertical KickTable in T2m2", file=f)
        print("START", file=f)
        print(' '*14, end ='', file=f)
        for j in range(len(self.x)):
            print('%+e'%self.x[j], end=' ', file=f)
        print('\n', end='', file=f)
        for i in range(len(self.y)):
            print('%+e'%self.y[i], end=' ', file=f)
            for j in range(len(self.x)):
                if _numpy.isnan(self.kick_y[i,j]):
                    print('%+e'%self.kick_y[i,j] + ' '*9, end=' ', file=f)
                else:
                    print('%+e'%self.kick_y[i,j], end=' ', file=f)
            print('\n', end='', file =f)

    @staticmethod
    def read_from_file(filename):
        with open(filename, encoding='latin-1') as f:
            lines = [line.strip() for line in f]
        lines = [line for line in lines if len(line)!=0]

        id_length = float(lines[3])
        nx = int(lines[5])
        ny = int(lines[7])
        x = _numpy.array([float(l) for l in lines[10].split()])
        ykx = []
        yky = []
        for i in range(ny):
            ykx.append([float(l) for l in lines[i+11].split()])
            yky.append([float(l) for l in lines[i+14+ny].split()])
        ykx = _numpy.array(ykx)
        yky = _numpy.array(yky)

        y = ykx[:,0]
        kick_x = ykx[:,1:]
        kick_y = yky[:,1:]

        kickmap = KickMap(id_length, x, y, kick_x, kick_y)
        return kickmap

    @staticmethod
    def pass_through_mask(input_filename, output_filename, mask):
        kickmap = KickMap.read_from_file(input_filename)
        for i in range(len(kickmap.y)):
            for j in range(len(kickmap.x)):
                pos = [kickmap.x[j], kickmap.y[i], 0.0]
                if not mask.is_inside(pos):
                    kickmap.kick_x[i,j] = _numpy.nan
                    kickmap.kick_y[i,j] = _numpy.nan
        kickmap.write_to_file(output_filename)
