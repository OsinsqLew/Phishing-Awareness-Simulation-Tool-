import mysql.connector
import setup.config as config
from datetime import datetime, timedelta
import jwt

class DB:
    def __init__(self, section_name:str):
        data = config.get_from_config("config.ini", section_name)
        secret = config.get_from_config("config.ini", "jwt")
        self.my_db = mysql.connector.connect(
            host=data["host"],
            port=3306,
            user=data["username"],
            password=data["password"],
            database=data["schema_name"],
            autocommit=True
        )

    def get_user_data(self, user_id:int, token:str) -> dict:
        if self.verify_token(user_id, token):
            cursor = self.my_db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        return{ "error": "Invalid token or user ID." }

    def get_all_users(self) -> list[dict]:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT seen, clicked, tags, phishing_type from emails;")
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def login(self, user_id:str, hash:str) -> bool:
        cursor = self.my_db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s AND password = %s", (user_id, hash))
        result = cursor.fetchone()
        token = None
        if result is not None:
            token = { "id": user_id, "end_time": f"{datetime.now() + timedelta(hours=1)}" }
            token = jwt.encode(token, key=self.secret["secret"], algorithm="HS256")
        cursor.close()
        return token
    
    def verify_token(self, user_id:str, token:str) -> bool:
        decoded = jwt.decode(token, key=self.secret["secret"], algorithms=["HS256"])
        if user_id == decoded["user_id"] and datetime(decoded["end_time"]) > datetime.now():
            return True
        return False