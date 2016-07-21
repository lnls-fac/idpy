
import numpy as _numpy
import matplotlib.pyplot as _plt
import idcpp as _idcpp
import idpy.utils as _utils


class FieldMapException(Exception):
    pass


class FieldMap(object):

    def __init__(self, label, filename_list, fieldmap3D=False):
        self.label = label
        if isinstance(filename_list, str):
            self._filename_list = [filename_list]
        else:
            self._filename_list = filename_list
        cpp_filename_list = _idcpp.CppStringVector(self._filename_list)
        self._cppobj = _idcpp.FieldMapContainer(cpp_filename_list, fieldmap3D)

    @property
    def filename_list(self):
        return self._filename_list

    @property
    def x_min(self):
        return self._cppobj.x_min

    @property
    def x_max(self):
        return self._cppobj.x_max

    @property
    def y_min(self):
        return self._cppobj.y_min

    @property
    def y_max(self):
        return self._cppobj.y_max

    @property
    def z_min(self):
        return self._cppobj.z_min

    @property
    def z_max(self):
        return self._cppobj.z_max


    def _check_limits(self, pos):
        if isinstance(pos[0], (float, int)): positions = [pos]
        else: positions = pos
        for p in positions:
            if p[0] < self.x_min or p[0] > self.x_max:
                raise FieldMapException("x out of range")
            if p[1] < self.y_min or p[1] > self.y_max:
                raise FieldMapException("y out of range")
            if p[2] < self.z_min or p[2] > self.z_max:
                raise FieldMapException("z out of range")

    def field(self, pos):
        self._check_limits(pos)
        if isinstance(pos[0], (float, int)):
            cpp_pos = _utils._vector_to_CppVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = _utils._CppVector3D_to_vector(cpp_field)
        else:
            cpp_pos = _utils._matrix_to_CppVectorVector3D(pos)
            cpp_field = self._cppobj.field(cpp_pos)
            field = _utils._CppVectorVector3D_to_matrix(cpp_field)
        return field

    def _field_profile(self, field_component, direction, pos, x=0.0, y=0.0, z=0.0):
        field_profile_x = []
        field_profile_y = []
        field_profile_z = []
        for i in range(len(pos)):
            if direction == "x":
                field = self.field([pos[i], y, z])
            elif direction == "y":
                field = self.field([x, pos[i], z])
            elif direction == "z":
                field = self.field([x, y, pos[i]])
            else:
                raise FieldMapException("Invalid value for direction.")
            field_profile_x.append(field[0])
            field_profile_y.append(field[1])
            field_profile_z.append(field[2])
        if field_component == "x":
            return _numpy.array([pos, field_profile_x])
        elif field_component == "y":
            return _numpy.array([pos, field_profile_y])
        elif field_component == "z":
            return _numpy.array([pos, field_profile_z])
        else:
            raise FieldMapException("Invalid value for field component.")

    def bx_x(self, y=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.x_min, self.x_max, nrpts)
        field_profile = self._field_profile("x", "x", pos, y=y, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def bx_y(self, x=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.y_min, self.y_max, nrpts)
        field_profile = self._field_profile("x", "y", pos, x=x, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def bx_z(self, x=0.0, y=0.0, mm=False, nrpts = 10000):
        pos = _numpy.linspace(self.z_min, self.z_max, nrpts)
        field_profile = self._field_profile("x", "z", pos, x=x, y=y)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def by_x(self, y=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.x_min, self.x_max, nrpts)
        field_profile = self._field_profile("y", "x", pos, y=y, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def by_y(self, x=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.y_min, self.y_max, nrpts)
        field_profile = self._field_profile("y", "y", pos, x=x, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def by_z(self, x=0.0, y=0.0, mm=False, nrpts = 10000):
        pos = _numpy.linspace(self.z_min, self.z_max, nrpts)
        field_profile = self._field_profile("y", "z", pos, x=x, y=y)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def bz_x(self, y=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.x_min, self.x_max, nrpts)
        field_profile = self._field_profile("z", "x", pos, y=y, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def bz_y(self, x=0.0, z=0.0, mm=False, nrpts = 1000):
        pos = _numpy.linspace(self.y_min, self.y_max, nrpts)
        field_profile = self._field_profile("z", "y", pos, x=x, z=z)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def bz_z(self, x=0.0, y=0.0, mm=False, nrpts = 10000):
        pos = _numpy.linspace(self.z_min, self.z_max, nrpts)
        field_profile = self._field_profile("z", "z", pos, x=x, y=y)
        if mm: field_profile[0] = field_profile[0]*1000.0
        return field_profile

    def plot_field(self):
        bx_x = self.bx_x(mm=True)
        bx_y = self.bx_y(mm=True)
        bx_z = self.bx_z(mm=True)
        by_x = self.by_x(mm=True)
        by_y = self.by_y(mm=True)
        by_z = self.by_z(mm=True)
        bz_x = self.bz_x(mm=True)
        bz_y = self.bz_y(mm=True)
        bz_z = self.bz_z(mm=True)
        pdf_names = ''

        pdf_names = pdf_names + 'bx_x.pdf' + ' '
        __plt.plot(*bx_x), __plt.xlabel('x [mm]'), __plt.ylabel('Bx [T]')
        __plt.title('Horizontal Field'), __plt.savefig('bx_x.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'bx_y.pdf' + ' '
        __plt.plot(*bx_y), __plt.xlabel('y [mm]'), __plt.ylabel('Bx [T]')
        __plt.title('Horizontal Field'), __plt.savefig('bx_y.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'bx_z.pdf' + ' '
        __plt.plot(*bx_z), __plt.xlabel('z [mm]'), __plt.ylabel('Bx [T]')
        __plt.title('Horizontal Field'), __plt.savefig('bx_z.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'by_x.pdf' + ' '
        __plt.plot(*by_x), __plt.xlabel('x [mm]'), __plt.ylabel('By [T]')
        __plt.title('Vertical Field'), __plt.savefig('by_x.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'by_y.pdf' + ' '
        __plt.plot(*by_y), __plt.xlabel('y [mm]'), __plt.ylabel('By [T]')
        __plt.title('Vertical Field'), __plt.savefig('by_y.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'by_z.pdf' + ' '
        __plt.plot(*by_z), __plt.xlabel('z [mm]'), __plt.ylabel('By [T]')
        __plt.title('Vertical Field'), __plt.savefig('by_z.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'bz_x.pdf' + ' '
        __plt.plot(*bz_x), __plt.xlabel('x [mm]'), __plt.ylabel('Bz [T]')
        __plt.title('Longitudinal Field'), __plt.savefig('bz_x.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'bz_y.pdf' + ' '
        __plt.plot(*bz_y), __plt.xlabel('y [mm]'), __plt.ylabel('Bz [T]')
        __plt.title('Longitudinal Field'), __plt.savefig('bz_y.pdf', bbox_inches='tight'), __plt.close(), __plt.figure()

        pdf_names = pdf_names + 'bz_z.pdf' + ' '
        __plt.plot(*bz_z), __plt.xlabel('z [mm]'), __plt.ylabel('Bz [T]')
        __plt.title('Longitudinal Field'), __plt.savefig('bz_z.pdf', bbox_inches='tight'), __plt.close()

        join_pdf = 'pdfunite ' + pdf_names +  self.label + '_field_profile.pdf'
        rm_pdf = 'rm -rf ' + pdf_names
        os.system(join_pdf)
        os.system(rm_pdf)
