#!/usr/bin/env python3


from setuptools import (find_packages, setup)


with open(".github/README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "inject_javascript",
    version = "0.0.4",
    author = "S0AndS0",
    author_email = "StrangerThanBland@gmail.com",
    description = "Inject JavaScript within PDF document body",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/pdf-utilities/inject_javascript",
    packages = find_packages(),
    install_requires = [
        'PyPDF2',
        'watch-path',
    ],
    entry_points = {
        'console_scripts': [
            'inject-pdf-javascript = inject_javascript.cli:main'
        ],
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Pre-processors',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
    ],
)
