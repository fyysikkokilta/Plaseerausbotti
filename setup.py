import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Plaseerausbotti",
    version=0.1,
    description="Telegram bot for seating academic dinner parties (sitsit)",
    long_description=read('README.md'),
    author="Fyysikkokilta",
    author_email="it@fyysikkokilta.fi",
    url="https://github.com/fyysikkokilta/Plaseerausbotti",
    packages=['plaseerausbotti'],
    python_requires=">=3.6.9,<3.11",
    install_requires=[
        "matplotlib~=3.4",
        "networkx~=2.6",
        "numpy~=1.21",
        "python-telegram-bot~=13.7",
        "thefuzz[speedup]~=0.19",
    ],
    extras_require={
        "test": [
            "pytest>=6.1",
            "pytest-sugar>=0.9",
            "pytest-cov>=2.12",
            "pytest-xdist>=2.3",
            "pylint>=2.9"
        ],
    },
)
