from pydantic import BaseModel, Field, ConfigDict


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    department: str
    salary: float = Field(gt=0)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: float

    model_config = ConfigDict(from_attributes=True)
