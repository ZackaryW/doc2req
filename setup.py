from setuptools import setup, find_packages

setup(
    name="doc2req",
    version="0.9.0",
    description="apidoc to dataclasses and other useful utilities",
    author="Zackary W",
    url="https://github.com/ZackaryW/doc2req",
    packages=find_packages(include=["tool/parser.js"]),
    install_requires=["pydantic", "requests"],
    python_requires=">=3.9",
    long_description=open("README.md").read(),
)
