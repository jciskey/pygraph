from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = []

setup(
    name='PyGraph',
    version='0.2.1',
    description="A graph manipulation library in pure Python",
    url="https://github.com/jciskey/pygraph",
    license="MIT",
    author="Joe Ciskey",
    author_email="forms@sleeplesshacker.com",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
