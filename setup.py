import codecs
import os
import re
import sys

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
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
    with open(os.path.join(package, "__init__.py")) as f:
        init_py = f.read()
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
    os.system(f"git tag -a {get_version()} -m 'version {get_version()}'")
    os.system("git push --tags")
    sys.exit()

# Do `python setup.py publish` to send current version to PyPI.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/django-spectator-%s.tar.gz" % (get_version()))
    sys.exit()

# Do `python setup.py testpublish` to send current version to Test PyPI.
if sys.argv[-1] == "testpublish":
    os.system("python setup.py sdist")
    os.system(
        f"twine upload "
        f"--repository-url https://test.pypi.org/legacy/ "
        f"dist/django-spectator-{get_version()}.tar.gz"
    )
    sys.exit()

dev_require = [
    "django-debug-toolbar",
    "pre-commit",
    "python-dotenv",
    "pyupgrade",
    "ruff",
    "unittest-parametrize",
]
tests_require = dev_require + [
    "factory-boy",
    "freezegun",
    "coverage[toml]",
]

setup(
    name="django-spectator",
    version=get_version(),
    packages=["spectator"],
    install_requires=[
        "django-imagekit>=4.0,<6.0",
        "hashids>=1.2.0,<1.4",
        "piexif>=1.1.3,<2.0",
        "pillow>=9.0.0,<11.0",
    ],
    dependency_links=[],
    tests_require=tests_require,
    extras_require={"dev": dev_require + ["Django>=4.1,<=5.0"], "test": tests_require},
    include_package_data=True,
    license=get_license(),
    description="A Django app to track book reading, movie viewing, "
    "gig going, play watching, etc.",
    long_description=read(os.path.join(os.path.dirname(__file__), "README.md")),
    long_description_content_type="text/markdown",
    url="https://github.com/philgyford/django-spectator",
    author=get_author(),
    author_email=get_author_email(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="",
    project_urls={
        "Blog posts": "https://www.gyford.com/phil/writing/tags/django-spectator/",
        "Bug Reports": "https://github.com/philgyford/django-spectator/issues",
        "Documentation": (
            "https://github.com/philgyford/django-spectator/blob/master/README.md"
        ),
        "Source": "https://github.com/philgyford/django-spectator",
    },
)
