
import numpy as _numpy
import idcpp as _idcpp
import idpy.utils as _utils
import idpy.auxiliary as _auxiliary
import idpy.cassette as _cassette
import idpy.idmodel as _idmodel

def calc_brho(energy):
    brho_p = _idcpp.new_doublep()
    beta_p = _idcpp.new_doublep()
    _idcpp.calc_brho(energy, brho_p, beta_p)
    brho = _idcpp.doublep_value(brho_p)
    beta = _idcpp.doublep_value(beta_p)
    return brho, beta

def runge_kutta(magnet, energy, r, p, zmax, step, mask=None, trajectory_flag=False):
    brho, beta = calc_brho(energy)

    if isinstance(magnet, _auxiliary.Magnet):
        cpp_magnet = magnet._cppobj
    elif isinstance(magnet, _idcpp.Magnet):
        cpp_magnet = magnet
    else:
        raise Exception("Invalid argument for runge_kutta")

    if mask is not None:
        if isinstance(mask, _auxiliary.Mask):
            cpp_mask = mask._cppobj
        elif isinstance(mask, _idcpp.Mask):
            cpp_mask = mask
        else:
            raise Exception("Invalid argument for runge_kutta")
    else:
        cpp_mask = _auxiliary.Mask()._cppobj

    cpp_r = _utils._vector_to_CppVector3D(r)
    cpp_p = _utils._vector_to_CppVector3D(p)
    cpp_kick = _idcpp.CppVector3D()

    if trajectory_flag:
        cpp_trajectory = _idcpp.CppDoubleVectorVector()
        _idcpp.runge_kutta(cpp_magnet, energy, cpp_r, cpp_p, zmax, step, cpp_mask, cpp_trajectory)
        kick = _utils._CppVector3D_to_vector(cpp_kick)
        trajectory = _utils._CppDoubleVectorVector_to_matrix(trajectory)
        return trajectory
    else:
        _idcpp.runge_kutta(cpp_magnet, energy, cpp_r, cpp_p, zmax, step, cpp_mask, cpp_kick)
        kick = _utils._CppVector3D_to_vector(cpp_kick)
        return kick

def calc_kickmap(magnet, energy, grid, zmin, zmax, rk_step, mask=None):
    if isinstance(magnet, _auxiliary.Magnet):
        cpp_magnet = magnet._cppobj
    elif isinstance(magnet, _idcpp.Magnet):
        cpp_magnet = magnet
    else:
        raise Exception("Invalid argument for calc_kickmap")

    if isinstance(grid, _auxiliary.Grid):
        cpp_grid = grid._cppobj
    elif isinstance(grid, _idcpp.Grid):
        cpp_grid = grid
    else:
        raise Exception("Invalid argument for calc_kickmap")

    if mask is not None:
        if isinstance(mask, _auxiliary.Mask):
            cpp_mask = mask._cppobj
        elif isinstance(mask, _idcpp.Mask):
            cpp_mask = mask
        else:
            raise Exception("Invalid argument for calc_kickmap")
    else:
        cpp_mask = _auxiliary.Mask()._cppobj

    cpp_kickmap = _idcpp.KickMap()
    _idcpp.calc_kickmap(cpp_magnet, energy, cpp_grid, zmin, zmax, rk_step, cpp_mask, cpp_kickmap)
    kickmap = _auxiliary.KickMap(kickmap=cpp_kickmap)
    return kickmap
