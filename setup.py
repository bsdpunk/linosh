#from distutils.core import setup
from setuptools import setup

#dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
install_requires = ['requests']

setup(
    name='linosh',
    version='0.1',
    packages=['linosh',],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [
        'linosh = linosh.linosh:cli', ],
     },
)
