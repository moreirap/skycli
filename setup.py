from setuptools import setup

setup(
    name='skycli',
    version='0.1',
    py_modules=['skycli'],
    include_package_data=True,
    install_requires=[
        'Click', 'Requests'
    ],
    entry_points='''
        [console_scripts]
        skycli=skycli:skycli
    ''',
)