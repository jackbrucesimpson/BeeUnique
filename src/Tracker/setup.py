from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "pytrack",
           sources=["pytrack.pyx", "track.cpp", "bee.cpp"],
           language="c++",
           extra_compile_args=['-std=c++11']
      )))
