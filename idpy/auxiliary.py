

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

    def __init__(self, id_length=None, x=None, y=None, kick_x=None, kick_y=None, filename=None):
        if filename is not None:
            id_length, x, y, kick_x, kick_y = self._read_from_file(filename)
        else:
            self.id_length = id_length
            self.x = x
            self.y = y
            self.kick_x = kick_x
            self.kick_y = kick_y
        cpp_x = idcpp.CppDoubleVector(self.x)
        cpp_y = idcpp.CppDoubleVector(self.y)
        cpp_kick_x = utils._matrix_to_CppDoubleVectorVector(self.kick_x)
        cpp_kick_y = utils._matrix_to_CppDoubleVectorVector(self.kick_y)
        self._cppobj = idcpp.KickMap(id_length, cpp_x, cpp_y, cpp_kick_x, cpp_kick_y)

    @staticmethod
    def _read_from_file(filename):
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

        return id_length, x, y, kick_x, kick_y

    @staticmethod
    def pass_through_mask(input_filename, output_filename, mask):
        id_length, x, y, kick_x, kick_y = KickMap._read_from_file(input_filename)
        for i in range(len(y)):
            for j in range(len(x)):
                pos = [x[j], y[i], 0.0]
                if not mask.is_inside(pos):
                    kick_x[i,j] = numpy.nan
                    kick_y[i,j] = numpy.nan

        f = open(output_filename, 'w')
        print("# KICKMAP", file=f)
        print("# Author: Luana N. P. Vilela @ LNLS, Date: ", file=f)
        print("# ID Length [m]", file=f)
        print(id_length, file=f)
        print("# Number of Horizontal Points",file=f)
        print(len(x), file=f)
        print("# Number of Vertical Points",file=f)
        print(len(y), file=f)

        print("# Horizontal KickTable in T2m2", file=f)
        print("START", file=f)
        print(' '*13, end ='', file=f)
        for j in range(len(x)):
            print('%+e'%x[j], end=' ', file=f)
        print('\n', end='', file=f)
        for i in range(len(y)):
            print('%+e'%y[i], end=' ', file=f)
            for j in range(len(x)):
                if numpy.isnan(kick_x[i,j]):
                    print('%+e'%kick_x[i,j] + ' '*9, end=' ', file=f)
                else:
                    print('%+e'%kick_x[i,j], end=' ', file=f)
            print('\n', end='', file =f)

        print("# Vertical KickTable in T2m2", file=f)
        print("START", file=f)
        print(' '*14, end ='', file=f)
        for j in range(len(x)):
            print('%+e'%x[j], end=' ', file=f)
        print('\n', end='', file=f)
        for i in range(len(y)):
            print('%+e'%y[i], end=' ', file=f)
            for j in range(len(x)):
                if numpy.isnan(kick_y[i,j]):
                    print('%+e'%kick_y[i,j] + ' '*9, end=' ', file=f)
                else:
                    print('%+e'%kick_y[i,j], end=' ', file=f)
            print('\n', end='', file =f)
