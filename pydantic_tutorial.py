# Python is dynamic typing
# lack for static typing

# For simple code , it is easily to track and understand the variable type.
# But for big applications with many modules, it will be harder.
# difficult with functions. Accidentally create object with incorrect type.

# Pydantic is data validation package
# Benefits : ide type hints, data validation, json serialisation
#

from pydantic import BaseModel, EmailStr, StrictInt, field_validator


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


# user = User(name='sundar',email='sund',account_id="1231") will fail since the email variable must be valid email address
# user = User(name = 'sundar',email= 'sund@gmail.com',account_id = str(1131241))  Will fail since there account_id must be Int
# user = User(name='Sundar', email='sund@gmail.com', account_id=-122)  Will fail account must be greater than 0
user = User(name="Sundar", email="sund@gmail.com", account_id=1231)

print(user)
print(user.model_dump_json())


# Pydantic vs dataclass -
# both provides type hints
# No data validation in dataclass
# Serialisation -
# Dataclass in-built
