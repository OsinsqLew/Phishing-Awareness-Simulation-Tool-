from backend.AI_emails.mail_sender import generate_n_send
import db.database as database
import random

db = database.DB("DB_connection")
def main(user_id):
    email, first_name, last_name, tags = db.get_user_data(user_id, db.secret).values()
    print(f"User ID: {user_id}, Email: {email}, Name: {first_name} {last_name}, Tags: {tags}")
    generate_n_send(
        db,
        first_name + " " + last_name,
        email,
        user_id,
        tags
    )

if __name__ == "__main__":
    # Example usage
    db_users = db.get_users_number()
    if db_users > 0:
        user_id = random.randint(1, db.get_users_number())
        main(user_id)
