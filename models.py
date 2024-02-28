from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass, DeclarativeBase
from sqlalchemy import ForeignKey, func
import uuid
from marshmallow import Schema, fields, validate

def generate_uuid():
    return str(uuid.uuid4())

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class TestCase(Base):
    __tablename__ = "test_case"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    scenario: Mapped[str]
    steps: Mapped[str]
    asset: Mapped[Optional[str]]
    asset_id: Mapped[Optional[int]]
    test_data: Mapped[str]
    expected_results: Mapped[str]
    actual_results: Mapped[Optional[str]]
    status: Mapped[Optional[bool]]
    tester_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), default=None
    )
 


class User(Base):
    __tablename__ = "user"
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    tests: Mapped[List["TestCase"]] = relationship(default_factory=list)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), default=None
    )
    id: Mapped[str] = mapped_column(init=True, primary_key=True, default_factory=generate_uuid)
    
    

class TestCaseSchema(Schema):
    scenario = fields.String(required=True)
    steps = fields.String(required=True)
    asset = fields.String()
    asset_id = fields.Integer()
    test_data = fields.String(required=True)
    expected_results = fields.String(required=True)
    actual_results = fields.String()
    status = fields.Boolean()


class UserSchema(Schema):
    name = fields.String(required=True) 
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=4, max=12)
    )