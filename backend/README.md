## Modele
### Oryginalny
- [Repozytorium](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)
    - licencja: `MIT`
### Skwantyzowany
- [Repozytorium](https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF)
- https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/blob/main/zephyr-7b-beta.Q4_K_M.gguf
    - licencja: `MIT`

### Pobieranie modelu
```shell
curl -L "https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/resolve/main/zephyr-7b-beta.Q4_K_M.gguf?download=true" --create-dirs -o "./models/zephyr-7b-beta.Q4_K_M.gguf"
```

## Przykładowe użycie generatora maili
```python
from mail_content_generator import MailContentGenerator


generator = MailContentGenerator()
subject, body = generator.generate_email('marek@example.com', 'www.example.com')

print("\nGenerated Email\n" + "-" * 50)
print(f'Subject: {subject}\n' + "-" * 50)
print(f'Body: {body}')
```

```text
Generated Email
--------------------------------------------------
Subject: Urgent: New Remote Work Policy
--------------------------------------------------
Body: Dear marek@example.com,

As a result of the ongoing global health crisis, our company has decided to update our remote work policy. This policy outlines the new guidelines and expectations for employees working from home. It is essential that you read and sign this policy by the end of today to continue working remotely.

The updated policy includes new requirements for work equipment, data security, and communication methods. Failure to adhere to these guidelines will result in termination of remote work privileges.

To access the policy and sign the agreement, please click the following link: www.example.com

Once you have signed the agreement, you will receive a confirmation email with your updated remote work details. If you have any questions or concerns, please contact your HR representative at [FAKE PHONE NUMBER] or [FAKE EMAIL ADDRESS].

Thank you for your prompt attention to this matter.

Best regards,
HR Department
[COMPANY NAME]
```

## Wysyłanie maili
### Generowanie App Password
- https://myaccount.google.com/apppasswords

### Modyfikowanie `config.py`
- Zmienić `MAIL_SENDER` na poprawny adres email
- W `MAIL_PASSWORD` wpisać wygenerowane App Password
```py
# [...]

################################################################
# mail_sender.py
MAIL_SENDER = 'example@gmail.com'
MAIL_PASSWORD = '<PASSWORD>'

# [...]
```

### Przykładowe użycie 
```py
from mail_sender import send_email

send_email("Email Subject", "<h1>Hello There</h1>", ["example@gmail.com"])
```
