from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, SecretStr, model_validator
from sqlmodel import Field, SQLModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserIn(UserBase):
    password: SecretStr = Field(min_length=8)
    password_confirmation: SecretStr

    @model_validator(mode='after')
    def check_password_confirmation(self):
        pw1 = self.password
        pw2 = self.password_confirmation
        if pw1 is not None and pw1 != pw2:
            raise ValueError('Password confirmation does not match')
        return self


class UserUpdate(UserIn):
    password: SecretStr | None = Field(default=None, min_length=8)
    password_confirmation: SecretStr | None = None


class User(UserBase):
    id: int


class UserInDB(SQLModel, table=True):
    __tablename__: str = 'users'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    password: str

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
        return self

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)

    def to_model(self) -> User:
        return User(id=self.id, name=self.name, email=self.email)
