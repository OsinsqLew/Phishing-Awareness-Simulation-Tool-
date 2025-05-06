import smtplib
from email.mime.text import MIMEText

from config import MAIL_SENDER, MAIL_PASSWORD


def send_email(subject: str, html_body: str, recipients: [str]) -> None:
    """
    Sends an HTML email with the specified subject and body to a list of recipients.

    Parameters:
        subject (str): The subject line of the email.
        html_body (str): The HTML content of the email body.
        recipients (list of str): A list of recipient email addresses.

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

    # connect to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.set_debuglevel(True)  # prints more info
        smtp_server.login(MAIL_SENDER, MAIL_PASSWORD)
        smtp_server.sendmail(MAIL_SENDER, recipients, msg.as_string())

    print("Email sent!")


if __name__ == '__main__':
    message = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <h1>Welcome to Our Service!</h1>
        <p>Hi there,</p>
        <p>Thank you for signing up for our service. We're excited to have you on board!</p>
        <p>To get started, please visit your <a href="https://example.com/dashboard">dashboard</a>.</p>
        <div class="image-container">
        <!-- image src: https://pixabay.com/illustrations/tv-television-televising-video-8760950/ -->
        <img src="https://cdn.pixabay.com/photo/2024/05/14/11/37/tv-8760950_1280.png" width="200" />
    </div>
        <p>If you have any questions, feel free to reply to this email or check out our <a href="https://example.com/help">help center</a>.</p>
        <div class="footer">
            <p>Best regards,</p>
            <p>The Example Team</p>
        </div>
    </body>
    </html>
    """

    send_email("Email Subject", message, ["example@gmail.com"])
