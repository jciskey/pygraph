from setuptools import setup


setup(
    name='PyGraph',
    version='0.2.0',
    description="A graph manipulation library in pure Python",
    url="https://github.com/jciskey/pygraph",
    license="MIT",
    packages=["pygraph", "pygraph.classes", "pygraph.functions", "pygraph.helpers"],
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
