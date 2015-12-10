from setuptools import setup

setup(
    name='datamarket-cli',
    version='0.1',
    py_modules=['datamarket-cli'],
        install_requires=[
            'Click',
    ],
    entry_points='''
        [console_scripts]
        datamarket-cli=datamarket-cli:cli
    ''',
)