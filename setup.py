from setuptools import find_packages, setup
import quest2pdf

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
   name="winquest",
   description="Questions printer.",
   long_description=long_description,
   license="License :: OSI Approved :: MIT License",
   author="Giancarlo Ossino",
   author_email="gcossino@gmail.com",
   version=quest2pdf.__version__,
   packages=find_packages(),
   python_requires=">=3.6"
)
