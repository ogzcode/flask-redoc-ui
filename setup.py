from setuptools import setup, find_packages


with open('README.md', 'r', encoding="utf-8") as file:
    long_description = file.read()  

setup(
    name='flask_pydantic_redoc',
    version='0.1.0',
    url='https://github.com/ogzcode/flask-pydantic-redoc',
    author='Oğuzhan Güç(ogzCode)',
    author_email='oguzguc44@gmail.com',
    packages=find_packages(),
    description="Flask extension for generating OpenAPI documentation with Pydantic models and ReDoc UI",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    install_requires=[
        'flask',
        'apispec',
        'apispec-webframeworks',
        'pydantic',
    ],
    extras_require={
        'test': [
            'pytest'
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)