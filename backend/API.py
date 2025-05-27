from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.DB import DB

app = FastAPI()
db = DB("DB_connection")

class CreateUserRequest(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    password: str

@app.post("/create_user")
def create_user(request: CreateUserRequest) -> dict:
    """
    Create a new user in the database.

    Args:
        request: A CreateUserRequest object containing user details.

    Returns:
        A dictionary with a success message.
    """
    try:
        db.add_user(
            request.email_address,
            request.first_name,
            request.last_name,
            request.password
        )
        return {"message": "User created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
def login(user_id: int, password: str) -> dict:
    """
    Log in a user and return an authentication token.

    Args:
        user_id: The ID of the user.
        password: The user's password.

    Returns:
        A dictionary containing the authentication token.
    """
    token = db.login(user_id, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"token": token}

@app.get("/get_user_data")
def get_user_data(user_id: int, token: str) -> dict:
    """
    Get user data from the database.

    Args:
        user_id: The ID of the user.
        token: The authentication token.

    Returns:
        A dictionary containing user data.
    """
    data = db.get_user_data(user_id, token)
    return data

@app.get("/statistics")
def get_statistics():
    """Get statistics from the database.

    Returns:
        A dictionary with the statistics.
    """
    data = db.get_all_users()
    return data


if __name__ == "__main__":
    pass
    # data = db.get_all_users()
    # print(data)

    # import uvicorn
    # uvicorn.run(app)
