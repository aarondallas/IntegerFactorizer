from setuptools import setup

# Read requirements
with open('requirements.txt', 'r') as fh:
    reqs = [str(x).strip() for x in fh.readlines()]

# Read version string
with open('integer_factorizer/_version.py', 'r') as fh:
    for line in fh:
        if line.startswith('__version__'):
            exec(line)

# noinspection PyUnresolvedReferences
setup(
    name="IntegerFactorizer",
    version=__version__,
    author='Aaron Dallas',
    description='Product prime factors of an integer',
    url='https://github.com/aarondallas/Echo360/IntegerFactorizer',
    packages=['integer_factorizer'],
    install_requires=reqs,
)

