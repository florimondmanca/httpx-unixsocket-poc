from setuptools import find_packages, setup

HTTPX_REMOTE = "https://github.com/florimondmanca/httpx.git"
HTTPX_TAG = "archive/third-parties-connections"

setup(
    name="httpx-unixsocket-poc",
    version="0.0.0",
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[f"httpx @ git+{HTTPX_REMOTE}@{HTTPX_TAG}#egg=httpx", "sniffio"],
    classifiers=["Private :: Do Not Upload", "Development Status :: 7 - Inactive"],
)
