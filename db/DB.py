import mysql.connector
import setup.config as config

class DB:
    def __init__(self, section_name:str):
        data = config.get_from_config("config.ini", section_name)
        self.my_db = mysql.connector.connect(
            host=data["host"],
            port=3306,
            user=data["username"],
            password=data["password"],
            database=data["schema_name"],
            autocommit=True
        )

    def get_user_data(self, user_id:int) -> dict:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM emails WHERE user_id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_all_users(self):
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT seen, clicked, tags, phishing_type from emails;")
        result = cursor.fetchall()
        cursor.close()
        return result