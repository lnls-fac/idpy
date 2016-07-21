
from mpl_toolkits.mplot3d import Axes3D as _Axes3D
import matplotlib.pyplot as _plt
import numpy as _numpy
import idcpp as _idcpp
import idpy.utils as _utils
import idpy.auxiliary as _auxiliary


class CassetteException(Exception):
    pass


class SubVolume(object):

    def __init__(self, dim=None, pos=[0,0,0], strength=1.0, subvolume=None):
        if subvolume is not None:
            if isinstance(subvolume, SubVolume):
                self._cppobj = _idcpp.SubVolume(subvolume._cppobj)
            elif isinstance(subvolume, _idcpp.SubVolume):
                self._cppobj = _idcpp.SubVolume(subvolume)
            else:
                raise CassetteException("Invalid argument for SubVolume constructor")
        else:
            cpp_dim = _utils._vector_to_CppVector3D(dim)
            cpp_pos = _utils._vector_to_CppVector3D(pos)
            self._cppobj = _idcpp.SubVolume(cpp_dim, cpp_pos, strength)

    def get_matrix(self, pos):
        cpp_pos = _utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._cppobj.get_gmatrix(cpp_pos)
        return _utils._CppMatrix3D_to_matrix(cpp_matrix)

    @property
    def dim(self):
        cpp_dim = self._cppobj.dim
        return _utils._CppVector3D_to_vector(cpp_dim)

    @dim.setter
    def dim(self, value):
        if not isinstance(value, (list, tuple, _numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid dimension value for SubVolume object")
        cpp_dim = _utils._vector_to_CppVector3D(value)
        self._cppobj.dim = cpp_dim

    @property
    def pos(self):
        cpp_pos = self._cppobj.pos
        return _utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, _numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid position value for SubVolume object")
        cpp_pos = _utils._vector_to_CppVector3D(value)
        self._cppobj.pos = cpp_pos

    @property
    def strength(self):
        return self._cppobj.str

    @strength.setter
    def strength(self, value):
        if value not in (1,-1):
            raise CassetteException("Invalid value for SubVolume strength")
        else:
            self._cppobj.str = value


class Block(_auxiliary.Magnet):

    def __init__(self, mag=None, dim=None, pos=[0,0,0], block=None):
        if block is not None:
            if isinstance(block, Block):
                self._cppobj = _idcpp.Block(block._cppobj)
            elif isinstance(block, _idcpp.Block):
                self._cppobj = _idcpp.Block(block)
            else:
                raise CassetteException("Invalid argument for Block constructor")
        else:
            cpp_mag = _utils._vector_to_CppVector3D(mag)
            cpp_dim = _utils._vector_to_CppVector3D(dim)
            cpp_pos = _utils._vector_to_CppVector3D(pos)
            self._cppobj = _idcpp.Block(cpp_mag, cpp_dim, cpp_pos)

    def add_subvolume(self, subvolume):
        if isinstance(subvolume, SubVolume):
            self._cppobj.add_subvolume(subvolume._subvolume)
        elif isinstance(subvolume, _idcpp.SubVolume):
            self._cppobj.add_subvolume(subvolume)

    def get_subvolume(self, index):
        return SubVolume(subvolume=self._cppobj.get_subvolume(index))

    def set_subvolume(self, index, subvolume):
        if isinstance(subvolume, SubVolume):
            self._cppobj.set_subvolume(index, subvolume._cppobj)
        elif isinstance(subvolume, _idcpp.SubVolume):
            self._cppobj.set_subvolume(index, subvolume)
        else:
            raise CassetteException("Invalid argument for set_subvolume function")

    def get_matrix(self, pos):
        cpp_pos = _utils._vector_to_CppVector3D(pos)
        cpp_matrix = self._cppobj.get_gmatrix(cpp_pos)
        return _utils._CppMatrix3D_to_matrix(cpp_matrix)

    @property
    def mag(self):
        cpp_mag = self._cppobj.get_mag()
        return _utils._CppVector3D_to_vector(cpp_mag)

    @mag.setter
    def mag(self, value):
        if not isinstance(value, (list, tuple, _numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid magnetization value for Block object")
        cpp_mag = _utils._vector_to_CppVector3D(value)
        self._cppobj.set_mag(cpp_mag)

    @property
    def dim(self):
        cpp_dim = self._cppobj.get_dim()
        return _utils._CppVector3D_to_vector(cpp_dim)

    @dim.setter
    def dim(self, value):
        if not isinstance(value, (list, tuple, _numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid dimension value for Block object")
        cpp_dim = _utils._vector_to_CppVector3D(value)
        self._cppobj.set_dim(cpp_dim)

    @property
    def pos(self):
        cpp_pos = self._cppobj.get_pos()
        return _utils._CppVector3D_to_vector(cpp_pos)

    @pos.setter
    def pos(self, value):
        if not isinstance(value, (list, tuple, _numpy.ndarray)) or len(value)!= 3:
            raise CassetteException("Invalid position value for Block object")
        cpp_pos = _utils._vector_to_CppVector3D(value)
        self._cppobj.set_pos(cpp_pos)


    def plot(self, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3, fig=None, ax=None):
        is_interactive = _plt.isinteractive()
        _plt.interactive = False

        if fig is None:
            fig = _plt.figure()
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
        X, Y = _numpy.meshgrid([x1, x2], [y1, y2])
        ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
        ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
        X, Z = _numpy.meshgrid([x1, x2], [z1, z2])
        ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
        ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
        Y, Z = _numpy.meshgrid([y1, y2], [z1, z2])
        ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
        ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
        ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            _plt.interactive = True
            _plt.draw()
            _plt.show()

        return fig, ax


class BlockContainer(_auxiliary.Magnet):

    def __init__(self, blocks, blockcontainer=None):
        if blockcontainer is not None:
            if isinstance(blockcontainer, BlockContainer):
                self._cppobj = _idcpp.BlockContainer(blockcontainer._cppobj)
            elif isinstance(blockcontainer, _idcpp.BlockContainer):
                self._cppobj = _idcpp.BlockContainer(blockcontainer)
            else:
                raise CassetteException("Invalid argument for BlockContainer constructor")
        else:
            self._cppobj = _idcpp.BlockContainer()
            for block in blocks:
                if isinstance(block, Block):
                    self._cppobj.add_element(block._cppobj)
                elif isinstance(block, _idcpp.Block):
                    self._cppobj.add_element(block)
                else:
                    raise CassetteException("Invalid argument for BlockContainer constructor")

    @property
    def size(self):
        return self._cppobj.size()

    def add_element(self, block):
        if isinstance(block, Block):
            self._cppobj.add_element(block._cppobj)
        elif isinstance(block, _idcpp.Block):
            self._cppobj.add_element(block)
        else:
            raise CassetteException("Invalid argument for add_element function")

    def get_item(self, index):
        return Block(block=self._cppobj.get_item(index))

    def shift_pos(self, pos):
        cpp_pos = _utils._vector_to_CppVector3D(pos)
        self._cppobj.shift_pos(cpp_pos)

    def plot(self, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3, fig=None, ax=None):
        is_interactive = _plt.isinteractive()
        _plt.interactive = False

        if fig is None:
            fig = _plt.figure()
            ax =  fig.add_subplot(111, projection='3d')

        for i in range(self.size):
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
            X, Y = _numpy.meshgrid([x1, x2], [y1, y2])
            ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
            ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
            X, Z = _numpy.meshgrid([x1, x2], [z1, z2])
            ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
            ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
            Y, Z = _numpy.meshgrid([y1, y2], [z1, z2])
            ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
            ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
            ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            _plt.interactive = True
            _plt.draw()
            _plt.show()

        return fig, ax


class HalbachCassette(BlockContainer):

    def __init__(self, block=None, rot=None, nr_periods=None, spacing=0, N=4, halbachcassette=None):
        if halbachcassette is not None:
            if isinstance(halbachcassette, HalbachCassette):
                self._cppobj = _idcpp.HalbachCassette(halbachcassette._cppobj)
            elif isinstance(halbachcassette, _idcpp.HalbachCassette):
                self._cppobj = _idcpp.HalbachCassette(halbachcassette)
            else:
                raise CassetteException("Invalid argument for HalbachCassette constructor")
        else:
            if isinstance(block, Block): block = block._cppobj
            if isinstance(rot, (list, tuple, _numpy.ndarray)): rot = _utils._matrix_to_CppMatrix3D(rot)
            self._cppobj = _idcpp.HalbachCassette(block, rot, nr_periods, spacing, N)

    @property
    def nr_periods(self):
        return int(self._cppobj.get_number_of_periods())

    @property
    def spacing(self):
        return float(self._cppobj.get_block_separation())

    @property
    def N(self):
        return int(self._cppobj.get_number_of_blocks_per_period())

    @property
    def magnetization_vector(self):
        mag = []
        for i in range(self._cppobj.size()):
            mag_cpp = self._cppobj.get_item(i).get_mag()
            mag.append(_utils._CppVector3D_to_vector(mag_cpp))
        return _numpy.array(mag)

    @property
    def center_pos(self):
        pos_cpp = self._cppobj.get_center_pos()
        return _utils._CppVector3D_to_vector(pos_cpp)

    @center_pos.setter
    def center_pos(self, pos):
        pos_cpp = _utils._vector_to_CppVector3D(pos)
        self._cppobj.set_center_pos(pos_cpp)

    def set_xcenter(self, x):
        self._cppobj.set_xcenter(x)

    def set_ycenter(self, y):
        self._cppobj.set_ycenter(y)

    def set_zcenter(self, z):
        self._cppobj.set_zcenter(z)

    def get_dim(self):
        cpp_dim = self._cppobj.get_dim()
        return _utils._CppVector3D_to_vector(cpp_dim)

    def plot(self, nr_periods=1, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3, fig=None, ax=None):
        if nr_periods > self.nr_periods:
            raise CassetteException("The number of periods should be less or equal the number of periods of the Halbach cassette")

        is_interactive = _plt.isinteractive()
        _plt.interactive = False

        if fig is None:
            fig = _plt.figure()
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
            X, Y = _numpy.meshgrid([x1, x2], [y1, y2])
            ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
            ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
            X, Z = _numpy.meshgrid([x1, x2], [z1, z2])
            ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
            ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
            Y, Z = _numpy.meshgrid([y1, y2], [z1, z2])
            ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
            ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
            ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            _plt.interactive = True
            _plt.draw()
            _plt.show()

        return fig, ax


class CassetteContainer(_auxiliary.Magnet):

    def __init__(self, cassettes, cassettecontainer=None):
        if cassettecontainer is not None:
            if isinstance(cassettecontainer, CassetteContainer):
                self._cppobj = _idcpp.CassetteContainer(cassettecontainer._cppobj)
            elif isinstance(cassettescontainer, _idcpp.CassetteContainer):
                self._cppobj = _idcpp.CassetteContainer(cassettecontainer)
            else:
                raise CassetteException("Invalid argument for CassetteContainer constructor")
        else:
            cpp_list_cassettes = []
            if isinstance(cassettes, (list, tuple, _numpy.ndarray)):
                for cassette in cassettes:
                    if isinstance(cassette, HalbachCassette):
                        cpp_list_cassettes.append(cassette._cppobj)
                    elif isinstance(cassette, _idcpp.HalbachCassette):
                        cpp_list_cassettes.append(cassette)
                    else:
                        raise CassetteException("Invalid argument for CassetteContainer constructor")
            elif isinstance(cassettes, HalbachCassette):
                cpp_list_cassettes.append(cassettes._cppobj)
            elif isinstance(cassettes, _idcpp.HalbachCassette):
                cpp_list_cassettes.append(cassettes)
            else:
                raise CassetteException("Invalid argument for CassetteContainer constructor")
            cpp_vector_cassettes  = _idcpp.CppVectorHalbachCassette()
            for c in cpp_list_cassettes:
                cpp_vector_cassettes.push_back(c)
            self._cppobj = _idcpp.CassetteContainer(cpp_vector_cassettes)

    @property
    def size(self):
        return self._cppobj.size()

    @property
    def nr_periods(self):
        return int(self._cppobj.get_item(0).get_number_of_periods())

    def add_element(self, cassette):
        if isinstance(cassette, HalbachCassette):
            self._cppobj.add_element(cassette._cppobj)
        elif isinstance(cassette, _idcpp.HalbachCassette):
            self._cppobj.add_element(cassette)
        else:
            raise CassetteException("Invalid argument for add_element function")

    def get_item(self, index):
        return HalbachCassette(halbachcassette=self._cppobj.get_item(index))

    def plot(self, nr_periods=1, block_color='blue', alpha=0.1, arrow_color='black', arrow_width=3):
        if nr_periods > self.nr_periods:
            raise CassetteException("Invalid number of periods")

        is_interactive = _plt.isinteractive()
        _plt.interactive = False
        fig = _plt.figure()
        ax =  fig.add_subplot(111, projection='3d')

        for i in range(self.size):
            c = HalbachCassette(halbachcassette=self._cppobj.get_item(i))
            N = self._cppobj.get_item(0).get_number_of_blocks_per_period()
            for i in range(N*nr_periods):
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
                X, Y = _numpy.meshgrid([x1, x2], [y1, y2])
                ax.plot_surface(X,z1,Y, alpha=alpha, color=block_color)
                ax.plot_surface(X,z2,Y, alpha=alpha, color=block_color)
                X, Z = _numpy.meshgrid([x1, x2], [z1, z2])
                ax.plot_surface(X,Z,y1, alpha=alpha, color=block_color)
                ax.plot_surface(X,Z,y2, alpha=alpha, color=block_color)
                Y, Z = _numpy.meshgrid([y1, y2], [z1, z2])
                ax.plot_surface(x1,Z,Y, alpha=alpha, color=block_color)
                ax.plot_surface(x2,Z,Y, alpha=alpha, color=block_color)
                ax.quiver(pos[0], pos[2], pos[1], mag[0], mag[2], mag[1], length=0.9*min(dim), pivot='middle', color=arrow_color, linewidths=arrow_width)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_zlabel('y [mm]')

        if is_interactive:
            _plt.interactive = True
            _plt.draw()
            _plt.show()
        return fig, ax
