from setuptools import find_packages, setup
from pathlib import Path

README_FILE = Path("README.md")
PACKAGE_DIR = Path("winquest")
VERSION_FILE = PACKAGE_DIR / "version.py"

with README_FILE.open() as fd:
    long_description = fd.readline()

with VERSION_FILE.open() as fd:
   version = fd.readline()

setup(
   name="winquest",
   description="Questions printer.",
   long_description=long_description,
   license="License :: OSI Approved :: MIT License",
   author="Giancarlo Ossino",
   author_email="gcossino@gmail.com",
   version=version,
   packages=find_packages(),
   python_requires=">=3.6"
)
