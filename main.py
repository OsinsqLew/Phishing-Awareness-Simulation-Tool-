from backend.AI_emails.mail_content_generator import MailContentGenerator
from backend.AI_emails.mail_sender import send_email
from db.DB import DB

db = DB("DB_connection")
def main(user_id, token):
    generator = MailContentGenerator()

    email, first_name, last_name, tags = db.get_user_data(user_id, token)
    generated_link = db.generate_link(user_id)
    subject, body = generator.generate_email(first_name + last_name, generated_link, tags)

    send_email(subject, body, [email])
