from setuptools import setup, find_packages

setup(
    name='py_elo_db',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'peewee',
        'nose'
    ],
    entry_points='''
        [console_scripts]
        elo=py_elo_db.elo:cli
    ''',
)
