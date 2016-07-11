
import idcpp
import idpy.utils as utils


class Grid(object):

    def __init__(self, nx, ny, xmin, xmax, ymin, ymax):
        self.nx = nx
        self.ny = ny
        self._cppobj = idcpp.Grid(self.nx, self.ny, xmin, xmax, ymin, ymax)
        self.x = self._cppobj.x
        self.y = self._cppobj.y


class Mask(object):

    def __init__(self, shape=None, width=0.0, height=0.0, filename=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.filename = filename
        if self.shape is not None:
            self._cppobj = idcpp.Mask(self.shape, self.width, self.height)
        elif self.filename is not None:
            self._cppobj = idcpp.Mask(self.filename)
        elif self.shape is None and self.filename is None:
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

    def write_to_file(self, filename):
        self._cppobj.write_to_file(filename)

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


class InsertionDevice(object):

    def __init__(self, model):
        self.model = model
        self._cppobj = idcpp.InsertionDevice(self.model._cppobj)

    def field(self, pos):
        if isinstance(pos[0], (float, int)) and len(pos) == 3:
            cpp_pos = utils._vector_to_CppVector3D(pos)
        elif len(pos[0]) == 3:
            cpp_pos = utils._matrix_to_CppVectorVector3D(pos)
        else:
            raise Exception("Invalid position")
        cpp_field = self._cppobj.field(cpp_pos)
        field = utils._CppVector3D_to_vector(cpp_field)
        return field

    def write_fieldmap_file(self, filename, x_vector, y, z_vector):
        cpp_x = idcpp.CppDoubleVector(x_vector)
        cpp_z = idcpp.CppDoubleVector(z_vector)
        self._cppobj.write_fieldmap_file(filename, cpp_x, y, cpp_z)

    def write_fieldmap_files(self, filename, x_vector, y_vector, z_vector):
        cpp_x = idcpp.CppDoubleVector(x_vector)
        cpp_y = idcpp.CppDoubleVector(y_vector)
        cpp_z = idcpp.CppDoubleVector(z_vector)
        self._cppobj.write_fieldmap_file(filename, cpp_x, cpp_y, cpp_z)

    def write_fieldmap3D_file(self, filename, x_vector, y_vector, z_vector):
        cpp_x = idcpp.CppDoubleVector(x_vector)
        cpp_y = idcpp.CppDoubleVector(y_vector)
        cpp_z = idcpp.CppDoubleVector(z_vector)
        self._cppobj.write_fieldmap3D_file(filename, cpp_x, cpp_y, cpp_z)

    def calc_kickmap(self, energy, runge_kutta_step, grid, mask=None):
        self._cppobj.calc_kickmap(grid._cppobj, mask._cppobj, energy, runge_kutta_step)
        self.kickmap = self._cppobj.kickmap

    def write_kickmap_file(self, filename):
        self.kickmap.write_to_file(filename)
