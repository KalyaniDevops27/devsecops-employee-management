from fastapi import FastAPI

# Create the FastAPI application
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
