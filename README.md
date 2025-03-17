# flask-redoc-ui

Flask extension for generating OpenAPI documentation using Pydantic models and ReDoc UI.

> This package works with docstrings found in flask routes.

### Installation

```
pip install git+https://github.com/ogzcode/flask-pydantic-redoc
```

### Configuration

Default Config

```
DEFAULT_CONFIG = {
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'info': {'title': 'ReDoc', 'version': '1.0.0'},
    }
```
