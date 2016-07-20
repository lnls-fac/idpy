

import numpy
import idcpp
import idpy.utils as utils


class Grid(object):

    def __init__(self, nx, ny, xmin, xmax, ymin, ymax):
        self._cppobj = idcpp.Grid(nx, ny, xmin, xmax, ymin, ymax)

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

    def __init__(self, shape=None, width=0.0, height=0.0, filename=None):
        if shape is not None:
            self._cppobj = idcpp.Mask(shape, width, height)
        elif filename is not None:
            self._cppobj = idcpp.Mask(filename)
        elif shape is None and filename is None:
            self._cppobj = idcpp.Mask("NONE")

    def is_inside(self, pos):
        cpp_pos = utils._vector_to_CppVector3D(pos)
        return self._cppobj.is_inside(cpp_pos)


class KickMap(object):

    def __init__(self, id_length=None, x=None, y=None, kick_x=None, kick_y=None):
        self._id_length = id_length
        self._x = x
        self._y = y
        self._kick_x = kick_x
        self._kick_y = kick_y
        cpp_x = idcpp.CppDoubleVector(self._x)
        cpp_y = idcpp.CppDoubleVector(self._y)
        cpp_kick_x = utils._matrix_to_CppDoubleVectorVector(self._kick_x)
        cpp_kick_y = utils._matrix_to_CppDoubleVectorVector(self._kick_y)
        self._cppobj = idcpp.KickMap(id_length, cpp_x, cpp_y, cpp_kick_x, cpp_kick_y)

    @property
    def id_length(self):
        return self._id_length

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def kick_x(self):
        return self._kick_x

    @property
    def kick_y(self):
        return self._kick_y

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
                if numpy.isnan(self.kick_x[i,j]):
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
                if numpy.isnan(self.kick_y[i,j]):
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
        x = numpy.array([float(l) for l in lines[10].split()])
        ykx = []
        yky = []
        for i in range(ny):
            ykx.append([float(l) for l in lines[i+11].split()])
            yky.append([float(l) for l in lines[i+14+ny].split()])
        ykx = numpy.array(ykx)
        yky = numpy.array(yky)

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
                    kickmap.kick_x[i,j] = numpy.nan
                    kickmap.kick_y[i,j] = numpy.nan
        kickmap.write_to_file(output_filename)
