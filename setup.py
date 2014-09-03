#! /usr/bin/env python

from distutils.core import setup

setup(
    name='hue',
    version='0.0.1',
    author='Sebastian Wiesinger',
    author_email='sebastian@karotte.org',
    packages=['hue'],
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Control Philips Hue system with python',
    long_description=open('README.txt').read(),
)
