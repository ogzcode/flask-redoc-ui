# Getting Started Guide

This guide explains how to integrate Flask Pydantic ReDoc into your project and its basic usage.

## Basic Setup

First, initialize Redoc in your Flask application:

```python
from flask import Flask
from flask_pydantic_redoc import Redoc
from pydantic import BaseModel, Field

app = Flask(__name__)
redoc = Redoc(app)
```

## Defining Models

Define your Pydantic models:

```python
class User(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
```

## Route Documentation

Document your routes using docstrings:

```python
@app.route('/users', methods=['GET'])
def get_users():
    """
    Returns the list of users.
    ---
    get:
      summary: Get list of users.
      description: This endpoint retrieves the list of users from the database.
      responses:
        200:
          description: Successful user list response.
          content:
            application/json:
              schema: 
                type: array
                items: 
                  type: object
                  properties:
                    id:
                      type: integer
                    username:
                      type: string
                    email:
                      type: string
    """
    users = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    return jsonify(users)
```

### CRUD Operations Examples

#### Create User

```python
@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a new user.
    ---
    post:
      summary: Create new user.
      description: This endpoint creates a new user record.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                address:
                  type: object
                  properties:
                    street:
                      type: string
                    city:
                      type: string
                    country:
                      type: string
      responses:
        201:
          description: User created successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  email:
                    type: string
                  address:
                    type: object
                    properties:
                      street:
                        type: string
                      city:
                        type: string
                      country:
                        type: string
    """
    return jsonify({"message": "User created"}), 201
```

#### Get User by ID

```python
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves information for a specific user.
    ---
    get:
      summary: Get user information.
      description: This endpoint retrieves information for the user with the specified ID.
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: User information retrieved successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    type: object
                    properties:
                      id:
                        type: integer
                      username:
                        type: string
                      email:
                        type: string
                  posts:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        title:
                          type: string
                        content:
                          type: string
        404:
          description: User not found.
    """
    return jsonify({"message": "User information retrieved"})
```

#### Update User

```python
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates user information.
    ---
    put:
      summary: Update user information.
      description: This endpoint updates information for the user with the specified ID.
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                settings:
                  type: object
                  properties:
                    notifications:
                      type: boolean
                    theme:
                      type: string
                    language:
                      type: string
      responses:
        200:
          description: User information updated successfully.
        404:
          description: User not found.
    """
    return jsonify({"message": "User updated"})
```

#### Delete User

```python
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user.
    ---
    delete:
      summary: Delete user.
      description: This endpoint deletes the user with the specified ID.
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: User deleted successfully.
        404:
          description: User not found.
    """
    return "", 204
```

## Accessing Documentation

After starting your application:

- Access the ReDoc UI via the `/docs` endpoint
- Access the OpenAPI JSON schema via the `/docs/json` endpoint

## Configuration

Configuration options to customize Redoc:

```python
config = {
    'title': 'API Documentation',
    'version': '1.0.0',
    'openapi_version': '3.0.2',
    'info': {
        'title': 'API Documentation',
        'version': '1.0.0',
        'description': 'API documentation description'
    }
}

redoc = Redoc(app, schemas=[User], config=config)
```

## Advanced Topics

For more detailed information, you can review the [Pydantic Integration](pydantic/index.md) section. 