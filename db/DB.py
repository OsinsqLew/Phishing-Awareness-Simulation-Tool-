import mysql.connector
import setup.config as config
from datetime import datetime, timedelta
import jwt
import random
import string
import hashlib

#zwrocic uwage czy jest zwracany json

def verify_token(self, user_id:str, token:str) -> bool:
    decoded = jwt.decode(token, key=self.secret["secret"], algorithms=["HS256"])
    if user_id == decoded["user_id"] and datetime(decoded["end_time"]) > datetime.now():
        return True
    return False

def generate_salt(length: int = 4):
    characters = string.ascii_letters + string.digits  # Litery i cyfry
    return ''.join(random.choice(characters) for _ in range(length))

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
        if verify_token(user_id, token):
            cursor = self.my_db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            print(result)
            cursor.close()
            return result
        return{ "error": "Invalid token or user ID." }

    def get_all_users(self) -> list[dict]:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT seen, clicked, tags, phishing_type from emails;")
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def add_user(self, email_address, first_name, last_name, password) -> None:
        """Adds a new user to the database."""
        salt = generate_salt()
        hash_pass = hashlib.md5((password + salt).encode('utf-8')).hexdigest().strip()
        query = (
            "INSERT INTO users (username, first_name, last_name, hash_pass, salt) VALUES (%s, %s, %s, %s, %s)"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (email_address, first_name, last_name, hash_pass, salt))
            self.my_db.commit()
        except Exception as e:
            print(e)
            self.my_db.rollback()
        finally:
            cursor.close()
    
    def login(self, user_id, password) -> str | None:
        """Checks if hash of given password is equal to the hash in the database."""
        query = (
            f"SELECT salt, hash_pass FROM Users WHERE id = %s;"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            salt, password_hash = result[0] if result else ("", "")
            password = password + salt
            given_hash = hashlib.md5(password.encode('utf-8')).hexdigest().strip()

            if password_hash == given_hash:
                token = { "id": user_id, "end_time": f"{datetime.now() + timedelta(hours=1)}" }
                token = jwt.encode(token, key=self.secret["secret"], algorithm="HS256")
        except Exception as e:
            print(e)
            token = None
        finally:
            cursor.close()
            return token

if __name__ =="__main__":
    db = DB("db_connection")
    db.get_user_data()