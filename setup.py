from setuptools import setup, find_packages

setup(
    name='pair-detector',
    version='0.0.0',
    author='Paul Nechifor',
    author_email='paul@nechifor.net',
    description='Image detection for pairs.',
    packages=find_packages(),
    long_description=open('README.rst').read(),
    license='ISC',
    url='http://github.com/paul-nechifor/pair-detector',
    test_suite='nose.collector',
    tests_require=[
        'nose==1.3.7',
        'mock==1.0.1',
    ],
    install_requires=[
        'future==0.15.2',
    ],
)
