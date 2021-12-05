from setuptools import setup

setup(
   name='illusion_hypar',
   description='Hypergraph partitioning for Illusion system',
   author='Yu-Neng Wang',
   author_email='wynwyn@stanford.edu',
   packages=['illusion_hypar'],
   install_requires=['kahypar']
)