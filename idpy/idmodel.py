
import numpy as _numpy
import idcpp as _idcpp
import idpy.utils as _utils
import idpy.auxiliary as _auxiliary
import idpy.cassette as _cassette


class IDModelException(Exception):
    pass


class EPU(_cassette.CassetteContainer):

    def __init__(self, block, nr_periods, magnetic_gap, _cassette_separation, block_separation=0.0, phase_csd=0.0, phase_cie=0.0, epu=None):
        if epu is not None:
            if isinstance(epu, EPU):
                self._cppobj = _idcpp.EPU(epu._cppobj)
            elif isinstance(epu, _idcpp.EPU):
                self._cppobj = _idcpp.EPU(epu)
            else:
                raise IDModelException("Invalid argument for EPU constructor")
        else:
            if isinstance(block, _cassette.Block):
                cpp_block = block._cppobj
            elif isinstance(block, _idcpp.Block):
                cpp_block = block
            else:
                raise IDModelException("Invalid argument for EPU constructor")
            self._cppobj = _idcpp.EPU(cpp_block, nr_periods, magnetic_gap, _cassette_separation, block_separation, phase_csd, phase_cie)
        self._csd = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_csd())
        self._cse = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_cse())
        self._cid = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_cid())
        self._cie = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_cie())

    @property
    def csd(self):
        return self._csd

    @property
    def cse(self):
        return self._cse

    @property
    def cid(self):
        return self._cid

    @property
    def cie(self):
        return self._cie

    def set_phase_csd(self, phase):
        self._cppobj.get_csd().set_zcenter(phase)

    def set_phase_cie(self, phase):
        self._cppobj.get_cie().set_zcenter(phase)



class DELTA(_cassette.CassetteContainer):

    def __init__(self, block, nr_periods, vertical_gap, horizontal_gap, block_separation=0.0, phase_cd=0.0, phase_ce=0.0, delta=None):
        if epu is not None:
            if isinstance(delta, DELTA):
                self._cppobj = _idcpp.DELTA(delta._cppobj)
            elif isinstance(delta, _idcpp.DELTA):
                self._cppobj = _idcpp.DELTA(delta)
            else:
                raise IDModelException("Invalid argument for DELTA constructor")
        else:
            if isinstance(block, _cassette.Block):
                cpp_block = block._cppobj
            elif isinstance(block, _idcpp.Block):
                cpp_block = block
            else:
                raise IDModelException("Invalid argument for DELTA constructor")
            self._cppobj = _idcpp.DELTA(cpp_block, nr_periods,  vertical_gap, horizontal_gap, block_separation, phase_cd, phase_ce)
        self._cs = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_cs())
        self._cd = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_cd())
        self._ci = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_ci())
        self._ce = _cassette.HalbachCassette(halbachcassette=self._cppobj.get_ce())

    @property
    def csd(self):
        return self._cs

    @property
    def cse(self):
        return self._cd

    @property
    def cid(self):
        return self._ci

    @property
    def cie(self):
        return self._ce

    def set_phase_cd(self, phase):
        self._cppobj.get_cd().set_zcenter(phase)

    def set_phase_ce(self, phase):
        self._cppobj.get_ce().set_zcenter(phase)
