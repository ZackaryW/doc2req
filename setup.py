from setuptools import setup, find_packages

setup(
    name="doc2req",
    version="0.9.1",
    description="apidoc to dataclasses and other useful utilities",
    author="Zackary W",
    url="https://github.com/ZackaryW/doc2req",
    packages=find_packages(),
    # include js
    package_data={'': ['*.js']},
    include_package_data=True,
    install_requires=["pydantic", "requests", "parse", "orjson"],
    python_requires=">=3.9",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    
)

