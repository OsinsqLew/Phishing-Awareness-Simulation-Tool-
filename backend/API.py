import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from db.database import DB

app = FastAPI()
db = DB("DB_connection")


class CreateUserRequest(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    password: str
    tags: str | None = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub ["*"] dla testów
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            request.password,
            request.tags
        )
        return {"message": "User created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def login(email: str, password: str) -> dict:
    """
    Log in a user and return an authentication token.

    Args:
        email: The email address of the user.
        password: The user's password.

    Returns:
        A dictionary containing the authentication token.
    """
    try:
        user_id, token = db.login(email, password)
        return {"user_id": user_id, "token": token}
    except Exception as e:
        if "Invalid credentials" in str(e):
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred during login.")


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
    try:
        data = db.get_user_data(user_id, token)
        return data
    except Exception as e:
        if "Invalid token or user ID" in str(e):
            raise HTTPException(status_code=401, detail="Invalid token or user ID.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while fetching user data.")


@app.get("/user_statistics")
def get_user_statistics(user_id: int, token: str) -> dict:
    """
    Get user statistics from the database.

    Args:
        user_id: The ID of the user.
        token: The authentication token.

    Returns:
        A dictionary containing user statistics.
    """
    try:
        data = db.get_user_stats(user_id, token)
        return data
    except Exception as e:
        if "Invalid token or user ID" in str(e):
            raise HTTPException(status_code=401, detail="Invalid token or user ID.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while fetching user statistics.")


@app.get("/statistics")
def get_statistics():
    """Get statistics from the database.

    Returns:
        A dictionary with the statistics.
    """
    data = db.get_all_user_stats()
    return data


@app.get("/home_page")
def email_clicked(reference: str):
    """
    Endpoint to handle phishing link clicks.
    
    This endpoint is a placeholder for handling clicks on phishing links.
    It currently returns a simple message indicating that the link was clicked.
    
    Returns:
        A dictionary with a message indicating the link was clicked.
    """
    try:
        db.phising_clicked(reference)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing phishing link: {str(e)}")
    return {"message": "Phishing link clicked!"}


@app.get("/track/report_phising.png")
def track_report_phishing(reference: str):
    """
    Tracking image for phishing reports.
    """

    static_path = os.getcwd()
    image_path = os.path.join(static_path, "setup/reportphishbutton.png")
    db.phising_seen(reference)
    return FileResponse(image_path, media_type="image/png")
