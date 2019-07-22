import codecs
import os
import re
import sys
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(filepath):
    return codecs.open(filepath, "r", "utf-8").read()


def get_entity(package, entity):
    """
    eg, get_entity('spectator', 'version') returns `__version__` value in
    `__init__.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    find = "__%s__ = ['\"]([^'\"]+)['\"]" % entity
    return re.search(find, init_py).group(1)


def get_version():
    return get_entity("spectator", "version")


def get_license():
    return get_entity("spectator", "license")


def get_author():
    return get_entity("spectator", "author")


def get_author_email():
    return get_entity("spectator", "author_email")


# Do `python setup.py tag` to tag with the current version number.
if sys.argv[-1] == "tag":
    os.system("git tag -a %s -m 'version %s'" % (get_version(), get_version()))
    os.system("git push --tags")
    sys.exit()

# Do `python setup.py publish` to send current version to PyPI.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload -r pypi")
    # os.system("python setup.py bdist_wheel upload")
    sys.exit()

# Do `python setup.py testpublish` to send current version to Test PyPI.
if sys.argv[-1] == "testpublish":
    os.system("python setup.py sdist upload -r pypitest")
    # os.system("python setup.py bdist_wheel upload")
    sys.exit()

setup(
    name="django-spectator",
    version=get_version(),
    packages=["spectator"],
    install_requires=[
        "django-imagekit>=4.0,<4.1",
        "hashids>=1.2.0,<1.3",
        "pillow>=6.1.0,<6.2",
    ],
    dependency_links=[],
    tests_require=[
        "factory-boy>=2.11.1,<3.0",
        "freezegun>=0.3.11,<0.4",
        "coverage"
    ],
    include_package_data=True,
    license=get_license(),
    description="A Django app to track book reading, movie viewing, "
    "gig going, play watching, etc.",
    long_description=read(os.path.join(os.path.dirname(__file__), "README.rst")),
    url="https://github.com/philgyford/django-spectator",
    author=get_author(),
    author_email=get_author_email(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="",
)
