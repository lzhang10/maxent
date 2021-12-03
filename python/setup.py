#!/bin/env python
# This is the building script for Python maxent extension module. 
# Simply type "python setup.py build" at command line to build the extension.
# After that you can type "python setup.py install" to install the extension
# module.
#
# The script assume you use gcc on unix and msvc on win32 platform.

from sys import platform, exec_prefix
from distutils.core import setup, Extension

# change the lines below according to your boost location
if platform == "win32":
    libmaxent_name = 'libmaxent'
    extra_compile_args = [
              "-DWIN32",
              "-DPYTHON_MODULE",
              "-DHAVE_FORTRAN=1",
              "-DBOOST_DISABLE_THREADS",
              "-DBOOST_DISABLE_ASSERTS", 
              "/GR", 
              ]
    data_files = [('Lib/site-packages/maxent' ,
           ['stlport_vc7146.dll', 
          'libifcoremd.dll', 
          'libmmd.dll']), 
          ]
    opt_lib = []

else: # unix
    libmaxent_name = 'maxent'
    extra_compile_args = [
              "-DNDEBUG",
              "-DPYTHON_MODULE",
              "-DBOOST_DISABLE_THREADS",
              ]
    data_files = []

    # various options detected from running ../configure
    opt_lib = []
    opt_lib_path = []
    ac_cv_lib_z_main = "@ac_cv_lib_z_main@"
    if ac_cv_lib_z_main == 'yes':
        opt_lib.append('z')

    fclibs = "/usr/lib/x86_64-linux-gnu/libboost_chrono.a"
    opt_lib_path.append("/usr/lib/x86_64-linux-gnu/")
    opt_lib.append('boost_chrono')
    opt_lib.append('boost_timer')

    # if fclibs != '':
    #     for s in fclibs.split():
    #         if s[:2] == '-L':
    #             opt_lib_path.append(s[2:])
    #         elif s[:2] == '-l':
    #             opt_lib.append(s[2:])
    #         else:
    #             raise 'unknow FCLIBS item: %s' % s

setup(name = "maxent",
      version = "version-devel", 
      author = "Le Zhang",
      author_email = "ejoy@users.sourceforge.net",
      url = "http://homepages.inf.ed.ac.uk/lzhang10/maxent_toolkit.html", 
      description = "A Maximum Entropy Modeling toolkit in python",
      long_description = """Maxent is a powerful, flexible, and easy-to-use
Maximum Entropy Modeling library for Python. The core engine is written in C++
with speed and portability in mind.

The win32 version of this module was compiled with MSVC7.1, Intel Fortran 8.0,
STLPort 4.6.
""",
      license = "LGPL",

      packages = ['maxent'],

      ext_modules=[
      Extension("maxent._cmaxent",
          ["maxent_wrap.cxx"],

          include_dirs=[
          "../src",
          ], 

          library_dirs=[
          "../build/src",
          ] + opt_lib_path,

          libraries = [libmaxent_name] + opt_lib,

          extra_compile_args = extra_compile_args, 

          )
          ], 
          data_files = data_files, 
         )

