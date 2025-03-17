# Pydantic Integration

Flask Pydantic ReDoc automatically generates your API schemas using Pydantic models. In this section, you will learn how to effectively use Pydantic models.

## Pydantic Plugin

Flask Pydantic ReDoc uses a special plugin to convert Pydantic models to OpenAPI schemas. This plugin is implemented with the `PydanticPlugin` class and correctly transfers all features of Pydantic models to OpenAPI schemas.

```python
from flask_pydantic_redoc import Redoc
from pydantic import BaseModel, Field

app = Flask(__name__)

# Define your Pydantic models
class User(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")

# Add your models when initializing Redoc
redoc = Redoc(app, schemas=[User])
```

## Contents

You can find detailed information about Pydantic integration in the following sections:

- [Model Examples](models.md) - Pydantic model examples and OpenAPI schema conversions
- [CRUD Operations](crud.md) - Using Pydantic models in API endpoints

## Registering Models with Redoc

To register your models with Redoc:

```python
from flask import Flask
from flask_pydantic_redoc import Redoc

app = Flask(__name__)

# Single model
redoc = Redoc(app, schemas=[User])

# Multiple models
redoc = Redoc(app, schemas=[User, Address, UserDetail, Product])
```

## Best Practices

1. Always add field descriptions (`description`)
2. Set default values appropriately
3. Add necessary validations
4. Organize nested models logically
5. Use type hints correctly 