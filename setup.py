import os.path
import sys
from typing import Dict, List

import setuptools


MODULE_NAME = "cleanpy"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info: Dict[str, str] = {}


def pytest_runner_requires() -> List[str]:
    if set(["pytest", "test", "ptr"]).intersection(sys.argv):
        return ["pytest-runner"]

    return []


def get_release_command_class() -> Dict:
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with open("README.rst", encoding=ENCODING) as f:
    LONG_DESCRIPTION = f.read()

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    TESTS_REQUIRES = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description="cleanpy is a CLI command to remove cache files and temporary files that related to Python.",
    include_package_data=True,
    keywords=["cleaner", "command"],
    license=pkg_info["__license__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={"Source": REPOSITORY_URL, "Tracker": "{:s}/issues".format(REPOSITORY_URL)},
    python_requires=">=3.6",
    setup_requires=pytest_runner_requires(),
    tests_require=TESTS_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    cmdclass=get_release_command_class(),
    entry_points={"console_scripts": ["cleanpy=cleanpy.main:main"]},
)
