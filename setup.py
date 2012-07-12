#!/usr/bin/env python

from distutils.core import setup

setup(name='Moipy',
      version='0.2',
      description='Python integration with MoIP payment gateway via API',
      author=['Herberth Amaral','Ale Borba'],
      author_email=['herberthamaral@gmail.com','ale.alvesborba@gmail.com'],
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
