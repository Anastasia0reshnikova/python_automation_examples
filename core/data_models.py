from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

"""
Pydantic is a Python library for validating data (data classes).
Good for working (testing) with DTOs (Data Transfer Objects). 
Good for API testing.
"""

"""
Optional type is used to indicate that a field is optional.
It can be used to specify that a field is optional,
or to specify that a field is optional and has a default value.

Value could be exist or None (not exist)
"""


class Category(BaseModel):
    id: Optional[int] = Field(default=None, ge=0) # означает “число ≥ 0, можно не передавать (или передать null)”.
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: Optional[str] = None


class PetStatus(Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Pet(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    category: Optional[Category] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = None
