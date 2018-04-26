from setuptools import find_packages, setup
from package import Package

setup(
    name='sampleproject',
    version='1.0',
    description='A sample Python project',
    author='Chris Brake',
    author_email='author@email.com',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'package': Package
    }
)
