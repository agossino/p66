from setuptools import find_packages, setup
from pathlib import Path

import p66

README_FILE = Path("README.md")

with README_FILE.open() as fd:
    long_description = fd.readline()


setup(
    name="p66",
    description="Questions printer.",
    long_description=long_description,
    license="License :: OSI Approved :: MIT License",
    author="Giancarlo Ossino",
    author_email="gcossino@gmail.com",
    version=p66.__version__,
    packages=find_packages(),
    python_requires=">=3.6"
)
