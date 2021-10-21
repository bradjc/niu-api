from setuptools import setup, find_packages
from niuApi import (__author__, __license__, NAME, VERSION, DESCRIPTION)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION.split('\n')[0],
    author=__author__,
    author_email='gino@nauminator.de',
    url='https://github.com/genaumann/niu-api',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
            'niu-api = niuApi.cli:run',
        ]
    },
    include_package_data=True,
    install_requires=['pyyaml', 'argparse'],
    license=__license__,
    zip_safe=False,
)
