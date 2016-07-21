
from . import utils
from . import auxiliary
from . import fieldmap
from . import cassette
from . import idmodel
from . import functions

import os as _os
with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()
