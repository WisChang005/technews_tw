from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    required = f.read().splitlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="technews-tw",
    version="1.3.1",
    description="Taiwan tech news crawlers.",
    author="Wis Chang",
    author_email="wistw.chang@gmail.com",
    url="https://github.com/WisChang005/technews_tw",
    include_packages_data=True,
    packages=find_packages(where='.', exclude=(), include=('*',)),
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
