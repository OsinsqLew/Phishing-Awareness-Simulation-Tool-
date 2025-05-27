from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.DB import DB

app = FastAPI()
db = DB("DB_connection")

def validate_token(token: str) -> bool:
    """
    Validate the authentication token.

    Args:
        token: The authentication token.

    Returns:
        True if the token is valid, False otherwise.
    """
    pass


@app.get("/get_user_data")
def get_user_data(user_id: int, token: str) -> list[dict]:
    """
    Get user data from the database.

    Args:
        user_id: The ID of the user.
        token: The authentication token.

    Returns:
        A dictionary containing user data.
    """
    if validate_token(token):
        return db.get_user_data(user_id)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/get_all_users")
def get_all_users() -> list[dict]:
    """
    Get all users data from the database.

    Returns:
        A list of dictionaries containing user data.
    """
    return db.get_all_users()
from db.DB import DB

@app.get("/statistics")
def get_statistics():
    """Get statistics from the database.

    Returns:
        A dictionary with the statistics.
    """
    data = db.get_all_users()
    return data


if __name__ == "__main__":
    # data = db.get_all_users()
    # print(data)

    # import uvicorn
    # uvicorn.run(app)