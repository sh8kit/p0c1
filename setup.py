from setuptools import setup

setup(
    name='datashack',
    packages=['datashack'],
    entry_points={
        'console_scripts': [
            'datashack=datashack.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=[
        'flask',
        'Click>=6.0',
        'rich',
        'inquirer',
        'dacite',
        'pyyaml',
        'dataclasses_avroschema',
        'inquirer'
    ],
)