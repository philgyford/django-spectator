import codecs
import os
import re
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

def get_entity(package, entity):
    """
    eg, get_entity('spectator', 'version') returns `__version__` value in
    `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    find = "__%s__ = ['\"]([^'\"]+)['\"]" % entity
    return re.search(find, init_py).group(1)

def get_version():
    return get_entity('spectator', 'version')

def get_license():
    return get_entity('spectator', 'license')

def get_author():
    return get_entity('spectator', 'author')

def get_author_email():
    return get_entity('spectator', 'author_email')

setup(
    name='django-spectator',
    version=get_version(),
    packages=['spectator'],
    install_requires=[
        'pytz',
    ],
    dependency_links=[
    ],
    tests_require=[
        'factory-boy>=2.8.1,<2.9',
        'coverage'
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    license=get_license(),
    description='A Django app to track book reading, movie viewing, gig going and play watching.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    url='https://github.com/philgyford/django-spectator',
    author=get_author(),
    author_email=get_author_email(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='',
)
