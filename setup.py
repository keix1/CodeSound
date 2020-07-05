from setuptools import setup, find_packages

setup(
    name="CodeSound",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["codesound = codesound.codesound:codesound"]
    }
)