from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.database import get_db
from app import models, schemas

# Create FastAPI application
app = FastAPI(
    title="Employee Management API",
    description="A DevSecOps learning project",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Employee Management API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "employee-management-api"
    }

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()

    return employees

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    try:
        db_employee.name = employee.name
        db_employee.email = employee.email
        db_employee.department = employee.department
        db_employee.salary = employee.salary

        db.commit()
        db.refresh(db_employee)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists"
        )

    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(db_employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }


@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists"
        )

    return db_employee

