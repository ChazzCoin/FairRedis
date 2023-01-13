from setuptools import setup, find_packages
import os

current = os.getcwd()

setup(
    name='FairRedis',
    version='1.0.3',
    description='A complete Python Package for RedisDB.',
    url='https://github.com/chazzcoin/FairRedis',
    author='ChazzCoin',
    author_email='chazzcoin@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['redis~=4.4.0', 'FairCore>=5.0.0'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)