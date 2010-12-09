#!/usr/bin/env python

from distutils.core import setup

setup(name='MoIPy',
      version='0.1',
      description='Python integration with MoIP payment gateway via API',
      author='Herberth Amaral',
      author_email='herberthamaral@gmail.com',
      url='http://labs.moip.com.br/',
      packages=['moipy'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOSX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',  
      ])
