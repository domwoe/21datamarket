from setuptools import setup

setup(
    name='datamarket',
    version='0.1',
    py_modules=['datamarketcli'],
        install_requires=[
            'Click',
    ],
    entry_points='''
        [console_scripts]
        datamarket=datamarketcli:cli
    ''',
)
