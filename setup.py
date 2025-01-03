"""Packaging."""

from pathlib import Path

from setuptools import setup

with Path("README.md").open() as file:
    long_description = file.read()

setup(
    name="zenopay",
    version="0.0.5",
    description="A Python wrapper for ZenoPay Payment API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jovyinny/zenopay",
    author="Jovine Mutelani",
    author_email="jovinerobotics@gmail.com",
    license="MIT",
    keywords=[
        "zenopay",
        "zenopay SDK",
        "zeno pay SDK",
        "ZenoPay Wrapper",
    ],
    python_requires=">=3.9",
    install_requires=["requests", "phonenumbers", "pydantic", "email_validator"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
