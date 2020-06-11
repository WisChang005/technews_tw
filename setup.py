from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    required = f.read().splitlines()


setup(
    name="technews",
    version="1.0.1",
    description="Taiwan tech news scraper",
    author="Wis Chang",
    author_email="wistw.chang@gmail.com",
    include_packages_data=True,
    packages=find_packages(where='.', exclude=(), include=('*',)),
    install_requires=required,
    zip_safe=False
)
