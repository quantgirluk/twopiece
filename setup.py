import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twopiece",
    version="1.0.0",
    author="Dialid Santiago ",
    author_email="d.santiago@outlook.com",
    description="Two-Piece Distributions Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantgirluk/twopiece",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)