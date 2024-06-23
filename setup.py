from setuptools import setup, find_packages

setup(
    name='tg_migrator',
    version='0.1.2',
    author='Mohammad Ashraf',
    description='migration tool for tigergraph',
    packages=find_packages(),
    install_requires=[
        'configparser',
        'pyTigerGraph',
    ],
    entry_points={
        'console_scripts': [
            'tg_migrator = tg_migrator.main:main',
        ],
    },
)
