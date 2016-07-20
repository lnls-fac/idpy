

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy
import idcpp
import idpy.utils as utils
import idpy.cassette as cassette


class InsertionDeviceException(Exception):
    pass


class IDModel(object):

    def __init__(self, cassettes, idmodel=None):
        if idmodel is not None:
            if isinstance(idmodel, IDModel):
                self._cppobj = idcpp.InsertionDevice(idmodel._cppobj)
            elif isinstance(idmodel, idcpp.InsertionDevice):
                self._cppobj = idcpp.InsertionDevice(idmodel)
            else:
                raise InsertionDeviceException("Invalid argument for IDModel constructor")
        else:
            cpp_list_cassettes = []
            if isinstance(cassettes, (list, tuple, numpy.ndarray)):
                for cassette in cassettes:
                    if isinstance(cassette, cassette.HalbachCassette):
                        cpp_list_cassettes.append(cassette._cppobj)
                    elif isinstance(cassette, idcpp.HalbachCassette):
                        cpp_list_cassettes.append(cassette)
                    else:
                        raise InsertionDeviceException("Invalid argument for IDModel constructor")
            elif isinstance(cassettes, cassette.HalbachCassette):
                cpp_list_cassettes.append(cassettes._cppobj)
            elif isinstance(cassettes, idcpp.HalbachCassette):
                cpp_list_cassettes.append(cassettes)
            else:
                raise InsertionDeviceException("Invalid argument for IDModel constructor")
            cpp_vector_cassettes  = idcpp.CppVectorHalbachCassette()
            for c in cpp_list_cassettes:
                cpp_vector_cassettes.push_back(c)
            self._cppobj = idcpp.InsertionDevice(cpp_vector_cassettes)

    @property
    def nr_periods(self):
        return int(self._cppobj.cassettes.get_item(0).get_number_of_periods())

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
            raise InsertionDeviceException("The number of periods should be less or equal the number of periods of the insertion device")

        is_interactive = plt.isinteractive()
        plt.interactive = False
        fig = plt.figure()
        ax =  fig.add_subplot(111, projection='3d')

        for i in range(self._cppobj.cassettes.size()):
            c = cassette.HalbachCassette(halbachcassette=self._cppobj.cassettes.get_item(i))
            N = self._cppobj.cassettes.get_item(0).get_number_of_blocks_per_period()
            for i in range(N*nr_periods):
                cpp_block = c.get_item(i)
                block = cassette.Block(block=cpp_block)
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

    # def write_fieldmap_file(self, filename, x_vector, y_vector, z_vector):
    #     cpp_x = idcpp.CppDoubleVector(x_vector)
    #     cpp_y = idcpp.CppDoubleVector(y_vector)
    #     cpp_z = idcpp.CppDoubleVector(z_vector)
    #     self._cppobj.write_fieldmap_file(filename, cpp_x, cpp_y, cpp_z)
    #
    # def write_fieldmap_files(self, filename, x_vector, y_vector, z_vector):
    #     cpp_x = idcpp.CppDoubleVector(x_vector)
    #     cpp_y = idcpp.CppDoubleVector(y_vector)
    #     cpp_z = idcpp.CppDoubleVector(z_vector)
    #     self._cppobj.write_fieldmap_file(filename, cpp_x, cpp_y, cpp_z)
    #
    # def calc_kickmap(self, energy, runge_kutta_step, grid, mask=None):
    #     self._cppobj.calc_kickmap(grid._cppobj, mask._cppobj, energy, runge_kutta_step)
    #     self.kickmap = self._cppobj.kickmap
    #
    # def write_kickmap_file(self, filename):
    #     self.kickmap.write_to_file(filename)



class EPU(IDModel):

    def __init__(self, block, nr_periods, magnetic_gap, cassette_separation, block_separation=0.0, phase_csd=0.0, phase_cie=0.0, epu=None):
        if epu is not None:
            if isinstance(epu, EPU):
                self._cppobj = idcpp.InsertionDevice(epu._cppobj)
            elif isinstance(epu, idcpp.InsertionDevice):
                self._cppobj = idcpp.InsertionDevice(epu)
            else:
                raise InsertionDeviceException("Invalid argument for EPU constructor")
        else:
            insertiondevice_cpp = idcpp.InsertionDevice()
            if isinstance(block, cassette.Block):
                cpp_block = block._cppobj
            elif isinstance(block, idcpp.Block):
                cpp_block = block
            else:
                raise InsertionDeviceException("Invalid argument for EPU constructor")
            idcpp.create_epu(cpp_block, nr_periods, magnetic_gap, cassette_separation, block_separation, phase_csd, phase_cie, insertiondevice_cpp)
            self._cppobj = insertiondevice_cpp

    @property
    def csd(self):
        return self._cppobj.cassettes.get_item(0)

    @property
    def cse(self):
        return self._cppobj.cassettes.get_item(1)

    @property
    def cid(self):
        return self._cppobj.cassettes.get_item(2)

    @property
    def cie(self):
        return self._cppobj.cassettes.get_item(3)

    def set_phase_csd(self, phase):
        self.csd.set_zcenter(phase)

    def set_phase_cie(self, phase):
        self.cie.set_zcenter(phase)



class DELTA(IDModel):

    def __init__(self, block, nr_periods, vertical_gap, horizontal_gap, block_separation=0.0, delta=None):
        if delta is not None:
            if isinstance(delta, DELTA):
                self._cppobj = idcpp.InsertionDevice(delta._cppobj)
            elif isinstance(delta, idcpp.InsertionDevice):
                self._cppobj = idcpp.InsertionDevice(delta)
            else:
                raise InsertionDeviceException("Invalid argument for DELTA constructor")
        else:
            if isinstance(block, cassette.Block):
                cpp_block = block._cppobj
            elif isinstance(block, idcpp.Block):
                cpp_block = block
            else:
                raise InsertionDeviceException("Invalid argument for DELTA constructor")
            insertiondevice_cpp = idcpp.InsertionDevice()
            idcpp.create_delta(cpp_block, nr_periods, magnetic_gap, cassette_separation, block_separation, phase_csd, phase_cie, insertiondevice_cpp)
            self._cppobj = insertiondevice_cpp

    @property
    def cs(self):
        return self._cppobj.cassettes.get_item(0)

    @property
    def cd(self):
        return self._cppobj.cassettes.get_item(1)

    @property
    def ci(self):
        return self._cppobj.cassettes.get_item(2)

    @property
    def ce(self):
        return self._cppobj.cassettes.get_item(3)

    def set_phase_cd(self, phase):
        self.cd.set_zcenter(phase)

    def set_phase_ce(self, phase):
        self.ce.set_zcenter(phase)
