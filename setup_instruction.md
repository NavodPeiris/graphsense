for building setup:
    pip install setuptools
    pip install wheel

on root:
    python setup.py sdist bdist_wheel

for publishing:
    pip install twine

for install locally for testing:
    pip install dist/graphsense-0.0.2-py3-none-any.whl

finally run:
    twine upload dist/*

    fill as follows:
        username: __token__
        password: {your token value}