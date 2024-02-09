from setuptools import setup, find_packages

setup(
    name='snakeshell',
    version='1.0.0',
    description='Unix Shell written in Python3',
    url='https://github.com/G000D1ESS/snakeshell.git',
    author='G000D1ESS',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='unix shell python3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snakeshell=src.main:main',
        ],
    },
)

