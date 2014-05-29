import os
from setuptools import setup, find_packages

setup(
    name = "uppsell",
    version = "0.1",
    author = "Adam Hayward",
    author_email = "adam@happy.cat",
    description = ("A django-based e-commerce API and admin backend."),
    license = "MIT",
    keywords = "e-commerce rest api sales",
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
    test_suite='tests.main',
)

