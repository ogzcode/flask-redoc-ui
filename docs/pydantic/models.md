# Pydantic Model Examples

In this section, you will see various Pydantic model examples that you can use with Flask Pydantic ReDoc and how they are converted to OpenAPI schemas.

## Basic Model

A Pydantic model can be defined in its simplest form as follows:

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    is_active: bool = Field(default=True, description="Is the user active?")
```

This model will appear in the OpenAPI schema as follows:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "User ID"
    },
    "username": {
      "type": "string",
      "description": "Username"
    },
    "email": {
      "type": "string",
      "description": "Email address"
    },
    "is_active": {
      "type": "boolean",
      "description": "Is the user active?",
      "default": true
    }
  },
  "required": ["id", "username", "email"]
}
```

## Nested Models

Pydantic supports nested models, and these models are correctly represented in OpenAPI schemas:

```python
class Address(BaseModel):
    street: str = Field(..., description="Street name")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")

class UserDetail(BaseModel):
    user: User = Field(..., description="User information")
    address: Optional[Address] = Field(None, description="Address information")
    interests: List[str] = Field(default_factory=list, description="Interests")
```

This nested model will appear in the OpenAPI schema as follows:

```json
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "User ID"
        },
        "username": {
          "type": "string",
          "description": "Username"
        },
        "email": {
          "type": "string",
          "description": "Email address"
        },
        "is_active": {
          "type": "boolean",
          "description": "Is the user active?",
          "default": true
        }
      },
      "required": ["id", "username", "email"],
      "description": "User information"
    },
    "address": {
      "type": "object",
      "properties": {
        "street": {
          "type": "string",
          "description": "Street name"
        },
        "city": {
          "type": "string",
          "description": "City"
        },
        "country": {
          "type": "string",
          "description": "Country"
        }
      },
      "required": ["street", "city", "country"],
      "description": "Address information"
    },
    "interests": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Interests",
      "default": []
    }
  },
  "required": ["user"]
}
```

## Using Field

You can enrich your model fields with the Pydantic `Field` class:

```python
class Product(BaseModel):
    id: int = Field(..., description="Product ID", gt=0)
    name: str = Field(..., description="Product name", min_length=3)
    price: float = Field(..., description="Product price", ge=0)
    stock: int = Field(default=0, description="Stock quantity", ge=0)
    tags: List[str] = Field(
        default_factory=list,
        description="Product tags",
        max_items=5
    )
```

This model will appear in the OpenAPI schema as follows:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Product ID",
      "exclusiveMinimum": 0
    },
    "name": {
      "type": "string",
      "description": "Product name",
      "minLength": 3
    },
    "price": {
      "type": "number",
      "description": "Product price",
      "minimum": 0
    },
    "stock": {
      "type": "integer",
      "description": "Stock quantity",
      "minimum": 0,
      "default": 0
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Product tags",
      "maxItems": 5,
      "default": []
    }
  },
  "required": ["id", "name", "price"]
}
```

## Complex Model Examples

### Related Models

You can also define more complex related models:

```python
class Comment(BaseModel):
    id: int = Field(..., description="Comment ID")
    content: str = Field(..., description="Comment content")
    created_at: str = Field(..., description="Creation date")

class Post(BaseModel):
    id: int = Field(..., description="Post ID")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    comments: List[Comment] = Field(default_factory=list, description="Comments")
    tags: List[str] = Field(default_factory=list, description="Tags")

class UserProfile(BaseModel):
    user: User = Field(..., description="User information")
    posts: List[Post] = Field(default_factory=list, description="User's posts")
    followers_count: int = Field(default=0, description="Followers count")
    following_count: int = Field(default=0, description="Following count")
```

These related models will appear in the OpenAPI schema as follows:

```json
{
  "UserProfile": {
    "type": "object",
    "properties": {
      "user": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "description": "User ID"
          },
          "username": {
            "type": "string",
            "description": "Username"
          },
          "email": {
            "type": "string",
            "description": "Email address"
          },
          "is_active": {
            "type": "boolean",
            "description": "Is the user active?",
            "default": true
          }
        },
        "required": ["id", "username", "email"],
        "description": "User information"
      },
      "posts": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer",
              "description": "Post ID"
            },
            "title": {
              "type": "string",
              "description": "Post title"
            },
            "content": {
              "type": "string",
              "description": "Post content"
            },
            "comments": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer",
                    "description": "Comment ID"
                  },
                  "content": {
                    "type": "string",
                    "description": "Comment content"
                  },
                  "created_at": {
                    "type": "string",
                    "description": "Creation date"
                  }
                },
                "required": ["id", "content", "created_at"]
              },
              "description": "Comments",
              "default": []
            },
            "tags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Tags",
              "default": []
            }
          },
          "required": ["id", "title", "content"]
        },
        "description": "User's posts",
        "default": []
      },
      "followers_count": {
        "type": "integer",
        "description": "Followers count",
        "default": 0
      },
      "following_count": {
        "type": "integer",
        "description": "Following count",
        "default": 0
      }
    },
    "required": ["user"]
  }
}
```

### Using Enums

Pydantic also supports Python enums:

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class UserWithRole(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    role: UserRole = Field(default=UserRole.USER, description="User role")
```

This model will appear in the OpenAPI schema as follows:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "User ID"
    },
    "username": {
      "type": "string",
      "description": "Username"
    },
    "role": {
      "type": "string",
      "description": "User role",
      "default": "user",
      "enum": ["admin", "moderator", "user"]
    }
  },
  "required": ["id", "username"]
}
```

### Date and Time Fields

Pydantic also supports date and time fields:

```python
from datetime import datetime, date
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: int = Field(..., description="Event ID")
    title: str = Field(..., description="Event title")
    event_date: date = Field(..., description="Event date")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
```

This model will appear in the OpenAPI schema as follows:

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Event ID"
    },
    "title": {
      "type": "string",
      "description": "Event title"
    },
    "event_date": {
      "type": "string",
      "format": "date",
      "description": "Event date"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation time"
    }
  },
  "required": ["id", "title", "event_date"]
}
```

## Best Practices

1. Always add field descriptions (`description`)
2. Set default values appropriately
3. Add necessary validations
4. Organize nested models logically
5. Use type hints correctly 