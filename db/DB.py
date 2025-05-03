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

    def get_user_data(self, user_id:int) -> list[dict]:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM emails WHERE user_id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_all_users(self) -> list[dict]:
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT seen, clicked, tags, phishing_type from emails;")
        result = cursor.fetchall()
        cursor.close()
        return result

if __name__ == "__main__":
    db = DB("DB_connection")
    data = db.get_user_data(1)
    print(data)
    all_users = db.get_all_users()
    print(all_users)