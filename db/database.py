import mysql.connector
import setup.config as config
from datetime import datetime, timedelta
import jwt
import random
import string
import hashlib
import base64
import json

#TODO sprawdzic user id - int, poprawic w verify token

def decode_phishing_link(encoded_link: str) -> dict:
    """
    Decodes a phishing link to extract user and mail IDs.
    
    Args:
        encoded_link (str): The encoded phishing link.

    Returns:
        dict: A dictionary containing user_id and mail_id.
    """
    decoded_data = base64.urlsafe_b64decode(encoded_link).decode()
    print(f"Decoded data: {decoded_data}")
    return json.loads(decoded_data)

def generate_salt(length: int = 4):
    characters = string.ascii_letters + string.digits  # Litery i cyfry
    return ''.join(random.choice(characters) for _ in range(length))

class DB:
    def __init__(self, section_name:str):
        data = config.get_from_config("config.ini", section_name)
        self.secret = config.get_from_config("config.ini", "jwt")["secret"]
        self.my_db = mysql.connector.connect(
            host=data["host"],
            port=3306,
            user=data["username"],
            password=data["password"],
            database=data["schema_name"],
            autocommit=True
        )

    def get_users_number(self) -> int:
        """Returns the number of users in the database."""
        cursor = self.my_db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0

    def verify_token(self, user_id: int, token: str) -> bool:
        try:
            decoded = jwt.decode(token, key=self.secret, algorithms=["HS256"])
        except Exception as e:
            print(f"Token verification failed: {e}")
            return False
        if user_id == decoded["id"] and datetime.strptime(decoded["end_time"], "%Y-%m-%d %H:%M:%S") > datetime.now():
            return True
        return False

    def get_user_data(self, user_id: int, token: str) -> dict:
        if  token == self.secret or self.verify_token(user_id, token):
            try:
                cursor = self.my_db.cursor(dictionary=True)
                cursor.execute("SELECT email_address, first_name, last_name, tags FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                print(f"Fetched user data: {result}")
                cursor.close()
                return result
            except Exception as e:
                raise Exception(f"Error fetching user data: {e}")
        else:
            raise Exception("Invalid token or user ID.")

    def get_all_user_stats(self) -> list[dict]:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT seen, clicked, tags, phishing_type from emails;")
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_user_stats(self, user_id: int, token: str) -> dict[dict]:
        if self.verify_token(user_id, token):
            try:
                cursor = self.my_db.cursor(dictionary=True)
                cursor.execute("SELECT * FROM emails WHERE user_id = %s", (user_id,))
                result = cursor.fetchall()
                cursor.close()
                return {"statisctics": result}
            except Exception as e:
                raise Exception(f"Error fetching user stats: {e}")
        else:
            raise Exception("Invalid token or user ID.")

    
    def add_user(self, email_address, first_name, last_name, password, tags) -> None:
        """Adds a new user to the database."""
        salt = generate_salt()
        hash_pass = hashlib.md5((password + salt).encode('utf-8')).hexdigest().strip()
        query = (
            "INSERT INTO users (email_address, first_name, last_name, hash_pass, salt, tags) VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (email_address, first_name, last_name, hash_pass, salt, tags))
            self.my_db.commit()
        except Exception as e:
            self.my_db.rollback()
            raise Exception(f"Error adding user: {e}")
        finally:
            cursor.close()
    
    def login(self, email, password) -> tuple[str, str] | None:
        """Checks if hash of given password is equal to the hash in the database."""
        query = (
            f"SELECT id, salt, hash_pass FROM Users WHERE email_address = %s;"
        )
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (email,))
            result = cursor.fetchall()
            user_id, salt, password_hash = result[0] if result else ("", "", "")
            password = password + salt
            print(f"Password with salt: {password}")
            given_hash = hashlib.md5(password.encode('utf-8')).hexdigest().strip()
            print(f"Given hash: {given_hash}")
            print(f"Password hash from DB: {password_hash}")

            print(f"{str(password_hash) == given_hash}")
            if str(password_hash) == given_hash:
                token = { "id": user_id, "end_time": f"{(datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")}" }
                token = jwt.encode(token, key=self.secret, algorithm="HS256")
                return user_id, token
            else:
                raise Exception("Invalid credentials.")
        except Exception as e:
            if "Invalid credentials" in str(e):
                raise Exception("Invalid credentials.")
            else:
                raise Exception(f"Error during login: {e}")
        finally:
            cursor.close()

    def phising_clicked(self, reference: str) -> None:
        """Updates the database to indicate that a phishing link was clicked."""
        decoded_data = decode_phishing_link(reference)
        user_id = decoded_data.get("user_id")
        mail_id = decoded_data.get("mail_id")
        if user_id is None or mail_id is None:
            raise Exception("Invalid reference data.")
        
        query = "UPDATE emails SET clicked = 1 WHERE user_id = %s AND email_id = %s"
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (user_id, mail_id))
            self.my_db.commit()
        except Exception as e:
            self.my_db.rollback()
            raise Exception(f"Error updating phishing click status: {e}")
        finally:
            cursor.close()

    def phising_seen(self, reference: str) -> None:
        """Updates the database to indicate that a phishing link was seen."""
        decoded_data = decode_phishing_link(reference)
        user_id = decoded_data.get("user_id")
        mail_id = decoded_data.get("mail_id")
        if user_id is None or mail_id is None:
            raise Exception("Invalid reference data.")
        
        query = "UPDATE emails SET seen = 1 WHERE user_id = %s AND email_id = %s"
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (user_id, mail_id))
            self.my_db.commit()
        except Exception as e:
            self.my_db.rollback()
            raise Exception(f"Error updating phishing seen status: {e}")
        finally:
            cursor.close()

    def get_next_email_id(self, user_id: int) -> int:
        """Retrieves the next email ID for a user."""
        query = "SELECT MAX(email_id) FROM emails WHERE user_id = %s"
        cursor = self.my_db.cursor()
        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] + 1 if result[0] is not None else 1
        except Exception as e:
            raise Exception(f"Error fetching next email ID: {e}")
        finally:
            cursor.close()

    def add_user_email(self, user_id: int, phishing_type: str | None, tags: str | None) -> None:
        """Adds a phishing email record for a user."""
        query = (
            "INSERT INTO emails (user_id, email_id, phishing_type, tags) VALUES (%s, %s, %s, %s)"
        )
        cursor = self.my_db.cursor()
        try:
            email_id = self.get_next_email_id(user_id)
            cursor.execute(query, (user_id, email_id, phishing_type, tags))
            self.my_db.commit()
            print(f"Added user email row: user_id={user_id}, email_id={email_id}, phishing_type={phishing_type}, tags={tags}")
        except Exception as e:
            self.my_db.rollback()
            raise Exception(f"Error adding user email row: {e}")
        finally:
            cursor.close()

    def generate_phishing_link(self, user_id):
        """
        Generates a phishing link for the user.
        
        Args:
            user_id (int): The ID of the user.

        Returns:
            str: A formatted phishing link.
        """
        email_id = self.get_next_email_id(user_id)
        data = {"user_id": user_id, "mail_id": email_id}
        encoded_data = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
        return f"http://localhost:8000/home_page?reference={encoded_data}"
