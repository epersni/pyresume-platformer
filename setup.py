from cx_Freeze import setup, Executable

includefiles = ['./resources']
build_options = {'packages': [], 'excludes': [],'include_files':includefiles}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'pyresume')
]

setup(name='pyresume-platformer',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
