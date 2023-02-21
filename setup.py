from setuptools import setup, find_packages
import codecs
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = '1.0.0'
DESCRIPTION = r"A File Based, Local, Simple, NoSQL DataBase"

with codecs.open(os.path.join(BASE_DIR, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="filexdb",
    version=VERSION,
    author="Sam (AcePic Studio)",
    author_email="sam@acepicstudio.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'dev-tool', 'database', 'local database'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
