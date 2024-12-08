from setuptools import setup, find_packages

setup(
    name="pastify",  
    version="0.1.2",
    author="Tushar Singh Bisht",
    author_email="aabisht2006@gmail.com",
    description="Pastify is a minimalistic clone of web dev frameworks like flask and express for creating web servers, having all the essential features of a webD framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tusharsinghbisht/pastify",
    packages=find_packages(),
    install_requires=[
        "setuptools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
