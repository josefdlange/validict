import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "validict",
        version = "1.2",
        author = "Josef Lange",
        author_email = "josef.d.lange@me.com",
        description = "A simple validation module",
        license = "MIT",
        keywords = "validation dictionary validate valid list json request validator",
        url = "https://github.com/josefdlange/validict",
        packages = find_packages(),
        test_suite = 'tests.core_tests', 
        long_description = read('README.rst'),
        classifiers = [
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License'
            ]
        )

