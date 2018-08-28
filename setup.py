from distutils.core import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()
    
setup(
    name='DesignBlocks',
    version='1.0',
    description='Python implementation of the educational toy, Design Blocks.'
    license=license
    long_description=long_description,
    url='https://github.com/analphagamma/DesignBlocks',
    author='Peter Bocz'
)
