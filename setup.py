import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    'requests>=2.9.1',
    'markdown>=2.6.0',
    'arrow>=0.12.1'
]

setuptools.setup(
    name="callisto-nbimporter",
    version="0.0.1",
    author="",
    author_email="",
    description="Import a notebook from Callisto",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cccs-is/callisto-nbimporter",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
