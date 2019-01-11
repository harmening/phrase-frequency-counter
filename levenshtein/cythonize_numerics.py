# python cythonize_numerics.py build_ext --inplace
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("levenshtein_numerics.pyx"))
