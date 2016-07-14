
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy
import idcpp
import idpy.utils as utils

class HalbachCassetteException(Exception):
    pass


class Subblock(object):

    def __init__(self, dim=None, pos=[0,0,0], subblock=None):
        if subblock is not None:
            if isinstance(subblock, Subblock):
                self._cppobj = subblock._cppobj
            elif isinstance(subblock, idcpp.Subblock):
                self._cppobj = subblock
            else:
                raise HalbachCassetteException("Invalid argument for Subblock constructor")
        else:
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
            raise HalbachCassetteException("Invalid dimension value for Subblock object")
        cpp_dim = utils._vector_to_CppVector3D(value)
        self._cppobj.dim = cpp_dim

    @property
    def pos(self):
        cpp_pos = self._cppobj.pos
        return utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise HalbachCassetteException("Invalid position value for Subblock object")
        cpp_pos = utils._vector_to_CppVector3D(value)
        self._cppobj.pos = cpp_pos


class Block(object):

    def __init__(self, mag=None, dim=None, pos=[0,0,0], block=None):
        if block is not None:
            if isinstance(block, Block):
                self._cppobj = block._cppobj
            elif isinstance(block, idcpp.Block):
                self._cppobj = block
            else:
                raise HalbachCassetteException("Invalid argument for Block constructor")
        else:
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
            raise HalbachCassetteException("Invalid magnetization value for Block object")
        cpp_mag = utils._vector_to_CppVector3D(value)
        self._cppobj.set_mag(cpp_mag)

    @property
    def dim(self):
        cpp_dim = self._cppobj.get_dim()
        return utils._CppVector3D_to_vector(cpp_dim)

    @dim.setter
    def dim(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise HalbachCassetteException("Invalid dimension value for Block object")
        cpp_dim = utils._vector_to_CppVector3D(value)
        self._cppobj.set_dim(cpp_dim)

    @property
    def pos(self):
        cpp_pos = self._cppobj.get_pos()
        return utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, numpy.ndarray)) or len(value)!= 3:
            raise HalbachCassetteException("Invalid position value for Block object")
        cpp_pos = utils._vector_to_CppVector3D(value)
        self._cppobj.set_pos(cpp_pos)


    def plot(self, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3, fig=None, ax=None):
        is_interactive = plt.isinteractive()
        plt.interactive = False

        if fig is None:
            fig = plt.figure()
            ax =  fig.add_subplot(111, projection='3d')

        mag = self.mag
        pos = 1000*self.pos
        dim = 1000*self.dim
        x1 = pos[0] - dim[0]/2.0
        x2 = pos[0] + dim[0]/2.0
        y1 = pos[1] - dim[1]/2.0
        y2 = pos[1] + dim[1]/2.0
        z1 = pos[2] - dim[2]/2.0
        z2 = pos[2] + dim[2]/2.0
        X, Y = numpy.meshgrid([x1, x2], [y1, y2])
        ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
        ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
        X, Z = numpy.meshgrid([x1, x2], [z1, z2])
        ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
        ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
        Y, Z = numpy.meshgrid([y1, y2], [z1, z2])
        ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
        ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
        ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            plt.interactive = True
            plt.draw()
            plt.show()

        return fig, ax


class HalbachCassette(object):

    def __init__(self, block=None, rot=None, nr_periods=None, spacing=0, N=4, halbachcassette=None):
        if halbachcassette is not None:
            if isinstance(halbachcassette, HalbachCassette):
                self._cppobj = halbachcassette._cppobj
            elif isinstance(halbachcassette, idcpp.HalbachCassette):
                self._cppobj = halbachcassette
            else:
                raise HalbachCassetteException("Invalid argument for HalbachCassette constructor")
        else:
            if isinstance(block, Block): block = block._cppobj
            if isinstance(rot, (list, tuple, numpy.ndarray)): rot = utils._matrix_to_CppMatrix3D(rot)
            self._cppobj = idcpp.HalbachCassette(block, rot, nr_periods, spacing, N)

    @property
    def genblock(self):
        return Block(block=self._cppobj.get_genblock())

    @property
    def nr_periods(self):
        return int(self._cppobj.get_number_of_periods())

    @property
    def spacing(self):
        return float(self._cppobj.get_block_separation())

    @property
    def N(self):
        return int(self._cppobj.get_number_of_blocks_per_period())

    def set_horizontal_pos(self, h_pos):
        self._cppobj.set_x(h_pos)

    def set_vertical_pos(self, v_pos):
        self._cppobj.set_y(v_pos)

    def set_longitudinal_pos(self, l_pos):
        self._cppobj.set_zcenter(l_pos)

    def get_pos(self):
        cpp_pos = self._cppobj.get_pos()
        return utils._CppVector3D_to_vector(cpp_pos)

    def get_dim(self):
        cpp_dim = self._cppobj.get_dim()
        return utils._CppVector3D_to_vector(cpp_dim)

    def get_item(self, i):
        cpp_block = self._cppobj.get_item(i)
        return Block(block=cpp_block)

    def field(self, pos):
        if isinstance(pos[0], (float, int)):
            cpp_pos = utils._vector_to_CppVector3D(pos)
            cpp_field = self._cppobj.get_field(cpp_pos)
            field = utils._CppVector3D_to_vector(cpp_field)
        else:
            cpp_pos = utils._matrix_to_CppVectorVector3D(pos)
            cpp_field = self._cppobj.get_field(cpp_pos)
            field = utils._CppVectorVector3D_to_matrix(cpp_field)
        return field

    def plot(self, nr_periods=1, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3, fig=None, ax=None):
        if nr_periods > self.nr_periods:
            raise HalbachCassetteException("The number of periods should be less or equal the number of periods of the Halbach cassette")

        is_interactive = plt.isinteractive()
        plt.interactive = False

        if fig is None:
            fig = plt.figure()
            ax =  fig.add_subplot(111, projection='3d')

        for i in range(self.N*nr_periods):
            cpp_block = self._cppobj.get_item(i)
            block = Block(block=cpp_block)
            mag = block.mag
            pos = 1000*block.pos
            dim = 1000*block.dim

            x1 = pos[0] - dim[0]/2.0
            x2 = pos[0] + dim[0]/2.0
            y1 = pos[1] - dim[1]/2.0
            y2 = pos[1] + dim[1]/2.0
            z1 = pos[2] - dim[2]/2.0
            z2 = pos[2] + dim[2]/2.0
            X, Y = numpy.meshgrid([x1, x2], [y1, y2])
            ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
            ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
            X, Z = numpy.meshgrid([x1, x2], [z1, z2])
            ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
            ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
            Y, Z = numpy.meshgrid([y1, y2], [z1, z2])
            ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
            ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
            ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            plt.interactive = True
            plt.draw()
            plt.show()

        return fig, ax

class EPU(object):

    def __init__(self, block, nr_periods, magnetic_gap, cassette_separation, block_separation=0.0):
        if isinstance(block, Block): block = block._cppobj
        self._cppobj = idcpp.EPU(block, nr_periods, magnetic_gap, cassette_separation, block_separation)

    @property
    def nr_periods(self):
        return int(self._cppobj.get_number_of_periods())

    @property
    def magnetic_gap(self):
        return float(self._cppobj.get_magnetic_gap())

    @property
    def cassette_separation(self):
        return float(self._cppobj.get_cassette_separation())

    @property
    def block_separation(self):
        return float(self._cppobj.get_block_separation())

    def set_phase_csd(self, phase):
        self._cppobj.set_phase_csd(phase)

    def set_phase_cie(self, phase):
        self._cppobj.set_phase_cie(phase)

    def field(self, pos):
        if isinstance(pos[0], (float, int)):
            cpp_pos = utils._vector_to_CppVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = utils._CppVector3D_to_vector(cpp_field)
        else:
            cpp_pos = utils._matrix_to_CppVectorVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = utils._CppVectorVector3D_to_matrix(cpp_field)
        return field

    def plot(self, nr_periods=1, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3):
        if nr_periods > self.nr_periods:
            raise HalbachCassetteException("The number of periods should be less or equal the number of periods of the undulator")

        is_interactive = plt.isinteractive()
        plt.interactive = False
        fig = plt.figure()
        ax =  fig.add_subplot(111, projection='3d')

        csd = HalbachCassette(halbachcassette=self._cppobj.csd)
        cse = HalbachCassette(halbachcassette=self._cppobj.cse)
        cid = HalbachCassette(halbachcassette=self._cppobj.cid)
        cie = HalbachCassette(halbachcassette=self._cppobj.cie)
        cassettes = [csd, cse, cid, cie]

        for c in cassettes:
            for i in range(csd.N*nr_periods):
                cpp_block = c.get_item(i)
                block = Block(block=cpp_block)
                mag = block.mag
                pos = 1000*block.pos
                dim = 1000*block.dim

                x1 = pos[0] - dim[0]/2.0
                x2 = pos[0] + dim[0]/2.0
                y1 = pos[1] - dim[1]/2.0
                y2 = pos[1] + dim[1]/2.0
                z1 = pos[2] - dim[2]/2.0
                z2 = pos[2] + dim[2]/2.0
                X, Y = numpy.meshgrid([x1, x2], [y1, y2])
                ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
                ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
                X, Z = numpy.meshgrid([x1, x2], [z1, z2])
                ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
                ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
                Y, Z = numpy.meshgrid([y1, y2], [z1, z2])
                ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
                ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
                ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            plt.interactive = True
            plt.draw()
            plt.show()

        return fig, ax

class DELTA(object):

    def __init__(self, block, nr_periods, vertical_gap, horizontal_gap, block_separation=0.0):
        if isinstance(block, Block): block = block._cppobj
        self._cppobj = idcpp.DELTA(block, nr_periods, vertical_gap, horizontal_gap, block_separation)

    @property
    def nr_periods(self):
        return int(self._cppobj.get_number_of_periods())

    @property
    def vertical_gap(self):
        return float(self._cppobj.get_vertical_gap())

    @property
    def horizontal_gap(self):
        return float(self._cppobj.get_horizontal_gap())

    @property
    def block_separation(self):
        return float(self._cppobj.get_block_separation())

    def set_phase_cs(self, phase):
        self._cppobj.set_phase_cs(phase)

    def set_phase_ci(self, phase):
        self._cppobj.set_phase_ci(phase)

    def field(self, pos):
        if isinstance(pos[0], (float, int)):
            cpp_pos = utils._vector_to_CppVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = utils._CppVector3D_to_vector(cpp_field)
        else:
            cpp_pos = utils._matrix_to_CppVectorVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = utils._CppVectorVector3D_to_matrix(cpp_field)
        return field

    def plot(self, nr_periods=1, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3):
        if nr_periods > self.nr_periods:
            raise HalbachCassetteException("The number of periods should be less or equal the number of periods of the undulator")

        is_interactive = plt.isinteractive()
        plt.interactive = False
        fig = plt.figure()
        ax =  fig.add_subplot(111, projection='3d')

        cs = HalbachCassette(halbachcassette=self._cppobj.cs)
        ci = HalbachCassette(halbachcassette=self._cppobj.ci)
        cd = HalbachCassette(halbachcassette=self._cppobj.cd)
        ce = HalbachCassette(halbachcassette=self._cppobj.ce)
        cassettes = [cs, ci, cd, ce]

        for c in cassettes:
            for i in range(csd.N*nr_periods):
                cpp_block = c.get_item(i)
                block = Block(block=cpp_block)
                mag = block.mag
                pos = 1000*block.pos
                dim = 1000*block.dim

                x1 = pos[0] - dim[0]/2.0
                x2 = pos[0] + dim[0]/2.0
                y1 = pos[1] - dim[1]/2.0
                y2 = pos[1] + dim[1]/2.0
                z1 = pos[2] - dim[2]/2.0
                z2 = pos[2] + dim[2]/2.0
                X, Y = numpy.meshgrid([x1, x2], [y1, y2])
                ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
                ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
                X, Z = numpy.meshgrid([x1, x2], [z1, z2])
                ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
                ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
                Y, Z = numpy.meshgrid([y1, y2], [z1, z2])
                ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
                ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
                ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            plt.interactive = True
            plt.draw()
            plt.show()

        return fig, ax
