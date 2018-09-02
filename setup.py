import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='python-onemapsg',
    version='0.0.1',
    packages=find_packages(),
    description='Python Client for OneMap SG',
    long_description=README,
    author='Thomas Jiang',
    author_email='thomasjiangcy@gmail.com',
    url='https://github.com/windspeed-io/python-onemapsg',
    license='MIT',
    install_requires=[
        'requests>=2.19.1'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
