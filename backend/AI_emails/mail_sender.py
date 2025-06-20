import smtplib
from email.mime.text import MIMEText

from backend.AI_emails.mail_content_generator import MailContentGenerator

import setup.config as config

MAIL_SENDER = config.get_from_config("config.ini", "gmail")["mail_sender"]
MAIL_PASSWORD = config.get_from_config("config.ini", "gmail")["mail_password"]

PUBLIC_IP_ADDRESS = config.get_from_config("config.ini", "server")["ip_addr"]


def send_email(subject: str, html_body: str, recipients: list[str]) -> None:
    """
    Sends an HTML email with the specified subject and body to a list of recipients.

    Parameters:
        subject (str): The subject line of the email.
        html_body (str): The HTML content of the email body.
        recipients (list of str):  A list of recipient email addresses.

    Returns:
        None

    Raises:
        smtplib.SMTPException: If there is an error during the email sending process.

    Notes:
        - This function uses the `smtplib.SMTP_SSL` class to connect to the Gmail SMTP server.
        - Ensure that the `MAIL_SENDER` and `MAIL_PASSWORD` variables are properly configured
          with the sender's email address and password, respectively.
        - The sender's email account must allow less secure app access or use an app-specific
          password if two-factor authentication is enabled.

    Example:
        send_email(
            subject="Welcome!",
            html_body="<h1>Welcome to our service!</h1><p>We're glad to have you.</p>",
            recipients=["example1@gmail.com", "example2@gmail.com"]
        )
    """
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = MAIL_SENDER
    msg['To'] = ', '.join(recipients)
    print(f"Sending email to: {', '.join(recipients)}")

    # connect to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.set_debuglevel(True)  # prints more info
        smtp_server.login(MAIL_SENDER, MAIL_PASSWORD)
        smtp_server.sendmail(MAIL_SENDER, recipients, msg.as_string())

    print("Email sent!")


def generate_n_send(db, recipient, recipient_email, recipient_id, user_tags):
    mcg = MailContentGenerator()
    link = db.generate_phishing_link(recipient_id)
    ref = link.split("?")[-1]
    print(f"Generated link: {link}")
    subject, message, tags = mcg.generate_email(recipient, link, user_tags)
    print(f"Tags: {tags}")
    message = f'''
    <html>
        <body>{message}</body>
        <img src="http://{PUBLIC_IP_ADDRESS}:8000/track/report_phising.png?reference={ref}" width="10" height="10">
    </html>'''
    send_email(subject, message, [recipient_email])
    db.add_user_email(recipient_id, tags["persona"], user_tags)
