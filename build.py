from setuptools import Extension, setup
from Cython.Build import cythonize
from distutils.command.build_ext import build_ext

def build(setup_kwargs):
    ext_modules = [
        Extension("libsniff",
                  sources=["libsniff.pyx","deps/libsniff/libsniff.c"],
                  libraries=["deps/libsniff/libsniff.h"],
                  include_dirs=["deps/libsniff"],
                  )
    ]

    setup_kwargs.update({
            'ext_modules': cythonize(
                ext_modules,
                language_level=3,
                compiler_directives={'linetrace': True},
            ),
            'cmdclass': {'build_ext': build_ext}
        })
