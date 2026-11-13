def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Employee Management API"
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "employee-management-api"
    }
def test_create_employee(client):
    response = client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Ravi"
    assert data["email"] == "ravi@example.com"
    assert data["department"] == "DevOps"
    assert data["salary"] == 45000

def test_get_all_employees(client):
    # Create an employee first
    client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    # Retrieve all employees
    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Ravi"


def test_get_employee_by_id(client):
    # Create an employee first
    create_response = client.post(
        "/employees",
        json={
            "name": "Kalyani",
            "email": "kalyani@example.com",
            "department": "Cloud Engineering",
            "salary": 100000
        }
    )

    employee_id = create_response.json()["id"]

    # Retrieve the employee using the generated ID
    response = client.get(f"/employees/{employee_id}")

    assert response.status_code == 200
    assert response.json()["id"] == employee_id
    assert response.json()["name"] == "Kalyani"

def test_get_employee_not_found(client):
    response = client.get("/employees/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Employee not found"
    }

def test_update_employee(client):
    # First, create an employee
    create_response = client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    employee_id = create_response.json()["id"]

    # Update the employee
    update_response = client.put(
        f"/employees/{employee_id}",
        json={
            "name": "Ravi Kumar",
            "email": "ravi@example.com",
            "department": "Cloud Engineering",
            "salary": 55000
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == employee_id
    assert data["name"] == "Ravi Kumar"
    assert data["department"] == "Cloud Engineering"
    assert data["salary"] == 55000

def test_update_employee_duplicate_email(client):
    # Create the first employee
    first_response = client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    first_employee_id = first_response.json()["id"]

    # Create the second employee
    client.post(
        "/employees",
        json={
            "name": "Sasi",
            "email": "sasi@example.com",
            "department": "Testing",
            "salary": 40000
        }
    )

    # Try updating the first employee with the second employee's email
    response = client.put(
        f"/employees/{first_employee_id}",
        json={
            "name": "Ravi",
            "email": "sasi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "An employee with this email already exists"
    }
def test_delete_employee(client):
    # Create an employee
    create_response = client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    employee_id = create_response.json()["id"]

    # Delete the employee
    delete_response = client.delete(
        f"/employees/{employee_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Employee deleted successfully"
    }

    # Verify that the employee no longer exists
    get_response = client.get(
        f"/employees/{employee_id}"
    )

    assert get_response.status_code == 404
def test_delete_employee_not_found(client):
    response = client.delete("/employees/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Employee not found"
    }

def test_create_employee_duplicate_email(client):
    # Create the first employee
    first_response = client.post(
        "/employees",
        json={
            "name": "Ravi",
            "email": "ravi@example.com",
            "department": "DevOps",
            "salary": 45000
        }
    )

    assert first_response.status_code == 201

    # Try creating another employee with the same email
    response = client.post(
        "/employees",
        json={
            "name": "Sasi",
            "email": "ravi@example.com",
            "department": "Testing",
            "salary": 40000
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "An employee with this email already exists"
    }


