# Python is dynamic typing
# lack for static typing

# For simple code , it is easily to track and understand the variable type.
# But for big applications with many modules, it will be harder.
# difficult with functions. Accidentally create object with incorrect type.

# Pydantic is data validation package
# Benefits : ide type hints, data validation, json serialisation
#

from pydantic import (
    BaseModel,
    EmailStr,
    StrictInt,
    field_validator,
    PositiveInt,
    conlist,
    Field,
    HttpUrl,
    model_validator,
    ValidationError,
    computed_field,
TypeAdapter

)
from uuid import uuid4
from typing import Optional, List, Any
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass,field


class User(BaseModel):
    name: str
    email: EmailStr
    account_id: StrictInt  # Normal int doesnt work, Need to provide StrictInt.

    @field_validator("account_id")
    @classmethod
    def validate_account_id(cls, value):
        if value <= 0:
            raise ValueError(f"Account Id must be positive : {value}")

        return value


# user = User(name='sundar',email='sund',account_id="1231") will fail since the email variable must be valid email
# address user = User(name = 'sundar',email= 'sund@gmail.com',account_id = str(1131241))  Will fail since there
# account_id must be Int user = User(name='Sundar', email='sund@gmail.com', account_id=-122)  Will fail account must
# be greater than 0


user = User(name="Sundar", email="sund@gmail.com", account_id=1231)

print(user)
print(user.model_dump_json())


# Pydantic vs dataclass -
# both provides type hints
# No data validation in dataclass
# Serialisation -
# Dataclass in-built


# without pydantic
class AccountUser:
    def __init__(self, id: int, name="Jane Doe"):
        if not isinstance(id, int):
            raise TypeError(f"Expected id to be an int type. Got {type(id).__name__}")

        if not isinstance(name, str):
            raise TypeError(f"Expected name to be an  type. Got {type(name).__name__}")

        self.id = id
        self.name = name


try:
    user = AccountUser(id="123")
except TypeError as e:
    print(e)


# with pydantic


class AccountUser(BaseModel):
    id: StrictInt
    name: str = "Jane Doe"


try:
    user = AccountUser(id="123")
except TypeError as e:
    print(e)


# user.model_dump - To dict
# user.model_dump_json - as json. Can be used to send to API
# user.model_json_schema - provide the schema.

# Nested Models


class Food(BaseModel):
    name: str
    price: float
    ingredients: Optional[List[str]] = None


class Restaurant(BaseModel):
    name: str
    location: str
    foods: List[Food]


restaurants_instance = Restaurant(
    name="Tasty Bites",
    location="123 , Flavour Street",
    foods=[
        {
            "name": "Cheese Pizza",
            "price": 12.50,
            "ingredients": ["Cheese", "Tomato Sauce", "Dough"],
        },
        {"name": "Vegan Burger", "price": 8.99},
    ],
)

print(restaurants_instance)
print(restaurants_instance.model_dump())


# in build Validator


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Employee(BaseModel):
    name: str
    position: str
    email: EmailStr


class Owner(BaseModel):
    name: str
    email: EmailStr


class Restaurant(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9-' ]+$")
    owner: Owner
    address: Address
    employees: conlist(Employee, min_length=2) # make sure the employee varaible atleast 2 empolyee
    number_of_seats: PositiveInt
    delivery: bool
    website: HttpUrl


restaurant_instance = Restaurant(
    name="Tasty Bites",  # Pattern should be match previous one. If i add `@` it will throw an error
    owner={
        "name": "John Doe",
        "email": "john.doe@example.com",  # should be off valid email address.
    },
    address={
        "street": "123, Flavor Street",
        "city": "Tastytown",
        "state": "TS",
        "zip_code": "12345",
    },
    employees=[
        {
            "name": "Jane Doe",
            "position": "Chef",
            "email": "jane.doe@example.com",  # should be off valid email address.
        },
        {
            "name": "Mike Roe",
            "position": "Waiter",
            "email": "mike.roe@example.com",  # should be off valid email address.
        },
    ],
    number_of_seats=50, # should greater than 0.
    delivery=True,
    website="http://tastybites.com",
)

# Printing the instance
print(restaurant_instance.model_dump_json())


# field validator


class OwnerWithValidator(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' not in v:
            raise ValueError('Owner name must contain a space')
        return v.title()


try:
    owner_instance = OwnerWithValidator(name="JohnDoe", email="john.doe@example.com")
except ValueError as e:
    print(e)


try:
    owner_instance = OwnerWithValidator(name="John Doe", email="john.doe@example.com")
except ValueError as e:
    print(e)

# Model validators - allowing you to create a model before and after field validation

class Owner(BaseModel):
    name: str
    email: EmailStr

    @model_validator(mode='before')
    @classmethod
    def check_sensitive_info_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'password' in data:
                raise ValueError('password should not be included')
            if 'card_number' in data:
                raise ValueError('card_number should not be included')
        return data

    @model_validator(mode='after')
    def check_name_contains_space(self) -> 'Owner':
        if ' ' not in self.name:
            raise ValueError('Owner name must contain a space')
        return self


print(Owner(name="John Doe", email="john.doe@example.com"))

try:
    Owner(name="JohnDoe", email="john.doe@example.com", password="password123")
except ValidationError as e:
    print(e)


# Field

class User(BaseModel):
    name: str = Field(default='John Doe')

user = User()
print(user)




class User(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)

user = User()
print(user)

class User(BaseModel):
    name: str = Field(..., alias='username')  # if you API and database fields differ - you only need one model


user = User(username='johndoe')
print(user)
print(user.model_dump(by_alias=True))


# More parameters

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=10, pattern=r'^\w+$')
    email: EmailStr = Field(...)
    age: int = Field(..., gt=0, le=120)
    height: float = Field(..., gt=0.0)
    is_active: bool = Field(True)
    balance: Decimal = Field(..., max_digits=10, decimal_places=2)
    favorite_numbers: List[int] = Field(..., min_items=1)

user_instance = User(
    username="john_doe", # will valid if the length of the variable is greater than 3 and less than 10
    age=30, # will valid if the age is greater than 0 and less than 120
    height=5.9, # will valid if the height is greater than 0 and less than 120
    weight=160.5, # will valid if the length of the variable is greater than 0 and less than 120
    email="john.doe@example.com",  # Check for valid of email address.
    password="securepassword",
    balance=9999.99, # will valid if the decimal place is round to 2.
    favorite_numbers=[1,2,3]
)

print(user_instance)

# Computed filed





class Person(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year


print(Person(name="John Doe", birth_year=2000).model_dump())


class Person(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year

    @field_validator('birth_year')
    @classmethod
    def validate_age(cls, v: int) -> int:
        current_year = datetime.now().year
        if current_year - v < 18:
            raise ValueError('Person must be 18 years or older')
        return v

try:
    print(Person(name="John Doe", birth_year=2006).model_dump())
except ValidationError as e:
    print(e)

# You also also use dataclasses and pydantics valiation logic - dataclasses do not provide that out of the box

from dataclasses import dataclass, field
from pydantic import Field, TypeAdapter


@dataclass
class User:
    id: int
    name: str = 'John Doe'
    age: Optional[int] = field(
        default=None,
        metadata=dict(title='The age of the user', description='do not lie!', ge=18),
    )
    height: Optional[int] = Field(None, title='The height in cm', ge=50, le=300)
    friends: List[int] = field(default_factory=lambda: [0])

# Example of using TypeAdapter to get json_schema of the User dataclass
print(TypeAdapter(User).json_schema())