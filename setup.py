#!/usr/bin/env python3

from setuptools import setup
from distutils.version import StrictVersion


idcpp_version = '0.1.0'

try:
    import idcpp
except ImportError:
    raise RuntimeError("idcpp package not found")

if StrictVersion(idcpp.__version__) < StrictVersion(idcpp_version):
    msg = ("idcpp package version must be >= " + idcpp_version +
        " (version installed is " + idcpp.__version__ + ")")
    raise RuntimeError(msg)

with open('VERSION','r') as _f:
    __version__ = _f.read().strip()

setup(
    name='idpy',
    version=__version__,
    author='lnls-fac',
    description='High level Accelerator Physics package',
    url='https://github.com/lnls-fac/idpy',
    download_url='https://github.com/lnls-fac/idpy',
    license='MIT License',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=['idpy'],
    package_data={'idpy': ['VERSION']},
    zip_safe=False
)
