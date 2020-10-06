rm -r dist
rm -r build

# build
python setup.py sdist
python setup.py sdist bdist_wheel

# deploy
python -m twine upload dist/*
