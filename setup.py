import os
from setuptools import setup

basedir = os.path.dirname(__file__)


with open(os.path.join(basedir, "djflocash", "__version__.py"), "r") as f:
    exec(f.read())  # this get __version__


with open(os.path.join(basedir, 'README.rst'), 'r') as f:
    long_description = f.read()
with open(os.path.join(basedir, 'CHANGELOG.rst'), 'r') as f:
    long_description += "\n\n" + f.read()


setup(
    name='djflocash',
    version=__version__,  # noqa
    description="Using flocash payment gateway interface with Django",
    long_description=long_description,
    author='Jurismarches',
    author_email='contact@jurismarches.com',
    url='https://github.com/jurismarches/djflocash',
    packages=[
        'djflocash',
        'djflocash.test',
    ],
    install_requires=[
        'pycountry>=18.5.26'
        'django>=1.10',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
