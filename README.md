# flask-pydantic-redoc

Flask extension for generating OpenAPI documentation using Pydantic models and ReDoc UI.

> This package works with docstrings found in flask routes.

### Installation

```
pip install https://github.com/ogzcode/flask-pydantic-redoc
```

### Getting Started

Load in your app:

```
from flask import Flask
from flask_pydantic_redoc import Redoc
from pydantic import Base


app = Flask(__name__)



class User(BaseModel):
    id: int = Field(..., description="The ID of the user")
    username: str = Field(..., description="The username of the user")
    email: str = Field(..., description="The email of the user")



redoc = Redoc(app, schemas=[User])



@app.route('/getAll', methods=['GET'])
def get_users():
    """
    Returns a list of users.
    ---
    get:
      summary: Retrieve a list of users.
      description: This API endpoint retrieves a list of users from the database.
      responses:
        200:
          description: A list of users.
          content:
            application/json:
              schema: 
                type: array
                items: 
                  $ref: '#/components/schemas/User'
    """
    users = [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]
    return jsonify(users)

```

If you go to the `/docs` page from the url, you will see the reDoc documentation, if you go to `/docs/json` you will see the json version.

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
