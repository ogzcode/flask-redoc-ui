# CRUD Operations and Using $ref

After defining your Pydantic models, you can reference them in your API endpoint docstrings. This makes your documentation cleaner and easier to maintain.

## Model Definitions

First, let's define the models we'll use:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    street: str = Field(..., description="Street name")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")

class User(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    is_active: bool = Field(default=True, description="Is the user active?")
    address: Optional[Address] = Field(None, description="Address information")

class Post(BaseModel):
    id: int = Field(..., description="Post ID")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    user_id: int = Field(..., description="User ID")

class UserCreate(BaseModel):
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    address: Optional[Address] = Field(None, description="Address information")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    email: Optional[str] = Field(None, description="Email address")
    is_active: Optional[bool] = Field(None, description="Is the user active?")
    address: Optional[Address] = Field(None, description="Address information")
```

## CRUD Endpoints

Now, let's define endpoints that implement CRUD operations using these models:

### User Listing (Read - List)

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
                  $ref: '#/components/schemas/User'
    """
    # Implementation code...
    return jsonify([])
```

### User Creation (Create)

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
              $ref: '#/components/schemas/UserCreate'
      responses:
        201:
          description: User created successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
    """
    # Implementation code...
    return jsonify({}), 201
```

### User Detail (Read - Detail)

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
                    $ref: '#/components/schemas/User'
                  posts:
                    type: array
                    items:
                      $ref: '#/components/schemas/Post'
        404:
          description: User not found.
    """
    # Implementation code...
    return jsonify({})
```

### User Update (Update)

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
              $ref: '#/components/schemas/UserUpdate'
      responses:
        200:
          description: User information updated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        404:
          description: User not found.
    """
    # Implementation code...
    return jsonify({})
```

### User Deletion (Delete)

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
    # Implementation code...
    return "", 204
```

## CRUD Operations with Related Models

Endpoints for managing a user's posts:

### Post Creation

```python
@app.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    """
    Creates a new post for a user.
    ---
    post:
      summary: Create new post.
      description: This endpoint creates a new post for the specified user.
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
                title:
                  type: string
                content:
                  type: string
      responses:
        201:
          description: Post created successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Post'
        404:
          description: User not found.
    """
    # Implementation code...
    return jsonify({}), 201
```

### Listing User's Posts

```python
@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """
    Lists a user's posts.
    ---
    get:
      summary: Get user posts.
      description: This endpoint retrieves all posts for the specified user.
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Posts retrieved successfully.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Post'
        404:
          description: User not found.
    """
    # Implementation code...
    return jsonify([])
```

## Best Practices

1. Always use `$ref` to reference models
2. Write detailed docstrings for endpoints
3. Clearly specify request and response schemas
4. Document error cases
5. Specify parameters and their requirements 