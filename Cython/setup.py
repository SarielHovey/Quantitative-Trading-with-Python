# Used to create python modual via C file created by Cython
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('fib.pyx'))
