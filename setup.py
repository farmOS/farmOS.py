import setuptools

setup_requires = [
    "pytest-runner",
]

install_requires = ["requests-oauthlib", "pydantic>=1.7.3"]

tests_require = ["pytest", "black>=20"]

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="farmOS",
    version="1.0.0-beta.1",
    author="farmOS team",
    author_email="mike@mstenta.net",
    description="A Python library for interacting with farmOS over API. ",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/farmOS/farmOS.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="pytest",
)
