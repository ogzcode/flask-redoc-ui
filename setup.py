from setuptools import setup, find_packages


with open('README.md', 'r', encoding="utf-8") as file:
    long_description = file.read()  

setup(
    name='flask_redoc_ui',
    version='0.1.0',
    url='https://github.com/ogzcode/flask-redoc_ui',
    author='Oğuzhan Güç(ogzCode)',
    author_email='oguzguc44@gmail.com',
    packages=find_packages(),
    description="Flask extension for generating OpenAPI documentation with Pydantic models and ReDoc UI",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    include_package_data=True,
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