from fastapi import FastAPI
from db.DB import DB

app = FastAPI()
db = DB("db_connection")

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