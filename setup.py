from setuptools import setup, find_packages

setup(
    name="checker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "autoscraper",
        "configparser",
        "telebot",
        "tinydb",
    ],
    entry_points={
        "console_scripts": [
            "checker=checker:main",
            "checker-service=checker.service:main",
        ],
    },
)
