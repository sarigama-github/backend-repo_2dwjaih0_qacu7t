"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Staff Arabia specific schemas

class Job(BaseModel):
    """Jobs collection schema
    Collection name: "job"
    """
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="City / Country")
    category: str = Field(..., description="Job category e.g., Oil & Gas, Construction")
    type: Literal["Full-time", "Part-time", "Contract", "Temporary"] = Field("Full-time", description="Employment type")
    description: Optional[str] = Field(None, description="Short job summary")
    apply_url: Optional[str] = Field(None, description="External application link if any")

class ContactMessage(BaseModel):
    """Contact messages collection schema
    Collection name: "contactmessage" -> use for storing contact form submissions
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    phone: Optional[str] = Field(None, description="Phone / WhatsApp number")
    message: str = Field(..., description="Message content")
    source: Optional[str] = Field("website", description="Submission source identifier")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
