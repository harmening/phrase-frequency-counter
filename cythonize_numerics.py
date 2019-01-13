# run c compiler:
# python cythonize_numerics.py build_ext --inplace
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

#setup(name = "numerics", ext_modules = cythonize("numerics.pyx"))

ext_modules=[
    Extension("numerics",
              sources=["numerics.pyx"],
              extra_compile_args=['-std=c99'],
              libraries=["m"] # Unix-like specific
    )
]

setup(
  name = "numerics",
  ext_modules = cythonize(ext_modules)
)
