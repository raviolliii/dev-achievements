# setup.py
# --------
# Specifies installation config for building/pypi.

from setuptools import find_packages, setup


# ignore unit tests
excluded_packages = ['tests', 'tests.*']

# load in README as long description
with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='dev_achievements',
    version='1.0.3',
    author='Ravi Patel',
    author_email='ravi.patel1245@gmail.com',
    description='Earn Achievements while learning how to code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/raviolliii/dev-achievements',
    packages=find_packages(exclude=excluded_packages),
    python_requires='>=3.5',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
