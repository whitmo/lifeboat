from setuptools import setup
import os


PROJECT = u'lifeboat'
VERSION = '0.1'
URL = 'http://lifeboat.github.io'
AUTHOR = u'whit morriss'
AUTHOR_EMAIL = u'code@whitmorriss.org'
DESC = "Three philosophers dine on each other on a raft of snakes"


def read_file(file_name, dir=os.path.dirname(__file__)):
    file_path = os.path.join(dir, file_name)
    with open(file_path) as fd:
        return fd.read()

    
setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=read_file('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=read_file('LICENSE'),
    namespace_packages=[],
    packages=[u'lifeboat'],
    #package_dir = {'': os.path.dirname(__file__)},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ZODB',
        'fibers',
        'pyuv',
        'pyzmq',
        'evergreen',
        'more_itertools',
        'uzmq'
    ],
    entry_points = """
    """,
    classifiers=[
        "Programming Language :: Python",
    ],
)
