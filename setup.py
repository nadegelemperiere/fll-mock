""" -----------------------------------------------------
# TECHNOGIX
# -------------------------------------------------------
# Copyright (c) [2022] Technogix SARL
# All rights reserved
# -------------------------------------------------------
# IT orchestrator module setup file
# -------------------------------------------------------
# Nadège LEMPERIERE, @17 october 2021
# Latest revision: 17 october 2021
# --------------------------------------------------- """

from setuptools import setup, find_packages

setup(
    name = "fll-mock",
    author = "Nadege LEMPERIERE",
    author_email="nadege.lemperiere@gmail.com",
    url="https://github.com/nadegelemperiere/fll-mock/",
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    description = ("Mock for lego bots"),
    license = "MIT",
    keywords = "python spike",
    install_requires=[
        "openpyxl>=3.0.9",
        "webcolors>=1.3"
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Testers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License"
    ],
)