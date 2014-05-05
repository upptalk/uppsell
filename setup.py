import os
from setuptools import setup, find_packages

setup(
    name = "uppsell",
    version = "0.1",
    author = "Adam Hayward",
    author_email = "adam@happy.cat",
    description = ("A Flask-based e-commerce API "\
            "and a django-backed admin for managing them."),
    license = "MIT",
    keywords = "example documentation tutorial",
    url = "https://github.com/upptalk/uppsell",
    packages = find_packages(exclude="django_site"),
    long_description="See https://github.com/upptalk/uppsell",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Flask",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Office/Business :: Financial",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

