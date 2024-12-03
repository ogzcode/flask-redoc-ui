from setuptools import setup, find_packages

setup(
    name='flask_pydantic_redoc',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'apispec',
        'apispec-webframeworks',
        'pydantic',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-flask',
        ],
    },
    package_data={
        'flask_redoc': ['templates/*.html'],
    },
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)