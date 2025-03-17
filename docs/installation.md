# Installation

You can follow these steps to add Flask Pydantic ReDoc to your project.

## Requirements

- Python 3.7+
- Flask 2.0+
- Pydantic 2.0+

## Installation with Pip

You can install directly from GitHub:

```bash
pip install git+https://github.com/ogzcode/flask-redoc-ui
```

## Manual Installation

If you don't want to install with pip, you can follow these steps for manual installation:

1. First, install the required packages:

```bash
pip install flask pydantic apispec apispec-webframeworks
```

2. Create a folder named `flask_pydantic_redoc` in your project.

3. Copy the following files to this folder:

   - `redoc.py` - Main class for ReDoc integration
   - `pydantic_ext.py` - Plugin that converts Pydantic models to OpenAPI schemas
   - `templates/redoc.html` - ReDoc UI template

4. Create an `__init__.py` file and add the following code:

```python
from .redoc import Redoc
```

### Required Dependencies

Make sure the following packages are installed for manual installation:

```
Flask>=3.0.0
pydantic>=2.0.0
apispec>=6.0.0
apispec-webframeworks>=1.0.0
```

## Dependency Check

After installation, you can test in the Python console to ensure all dependencies are correctly installed:

```python
from flask_pydantic_redoc import Redoc
from flask import Flask

app = Flask(__name__)
redoc = Redoc(app)
```

If you don't get any errors, the installation is successful.

## Next Steps

After completing the installation, you can learn how to use Flask Pydantic ReDoc in your application by reviewing the [Getting Started Guide](getting-started.md). 