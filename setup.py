from setuptools import find_packages, setup


setup(
    name="httpx-unixsocket-poc",
    version="0.0.0",
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "httpx @ "
        "git+https://github.com/encode/httpx.git@connectionpool-third-parties"
        "#egg=httpx",
        "sniffio",
    ],
    classifiers=["Private :: Do Not Upload", "Development Status :: 7 - Inactive"],
)
