import pytest
from pydantic import ValidationError
from app.schemas import EmployeeCreate


def test_valid_employee():
    employee = EmployeeCreate(
        name="Ravi",
        email="ravi@example.com",
        department="DevOps",
        salary=45000
    )

    assert employee.name == "Ravi"
    assert employee.salary == 45000


def test_employee_name_too_short():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="R",
            email="ravi@example.com",
            department="DevOps",
            salary=45000
        )


def test_employee_salary_must_be_positive():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            name="Ravi",
            email="ravi@example.com",
            department="DevOps",
            salary=-100
        )
