rm -r dist
rm -r build

# build
python3 setup.py sdist
python3 setup.py sdist bdist_wheel

# deploy
python3 -m twine upload dist/*
