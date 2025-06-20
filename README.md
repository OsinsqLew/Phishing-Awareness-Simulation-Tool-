# Phishing Awareness Simulation Tool
---

## Klonowanie repozytorium
```shell
git clone https://github.com/OsinsqLew/Phishing-Awareness-Simulation-Tool-
cd Phishing-Awareness-Simulation-Tool-
```

## Pobieranie modelu (opcjonalne, program robi to automatycznie)
```shell
curl -L "https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/resolve/main/zephyr-7b-beta.Q4_K_M.gguf?download=true" --create-dirs -o "./backend/AI_emails/models/zephyr-7b-beta.Q4_K_M.gguf"
```

## Uruchamianie serwisu
> [!NOTE]
> Należy stworzyć plik `config.ini` z niezbędnymi zmiennymi
### Wypełnianie `config.ini`
#### Generowanie App Password
- https://myaccount.google.com/apppasswords

![Generowanie App Password](https://github.com/user-attachments/assets/890283d1-0fb6-4550-82e0-b529ebb33068)

### Stawianie kontenerów
> [!NOTE]
> Do zbudowania i uruchomienia serwisu potrzebny jest [Docker](https://docs.docker.com/get-started/get-docker/) i Docker Compose

```shell
docker-compose up
```
Sprawdź dostępne kontenery oraz porty w [`docker-compose.yml`](./docker-compose.yml)

### Wysyłanie maili (for now)
```shell
docker container exec -it phishing-awareness-simulation-tool--backend-1 /bin/bash
python main.py
```

---
## Skrypt `User Data` do AWS EC2 (Amazon Linux 2023)
> [!NOTE]
> Budowanie, czy samo generowanie maili może trochę potrwać

`Advanced details` -> `User data`
```bash
#!/usr/bin/env bash

sudo yum update -y
sudo yum install -y docker git

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version

sudo systemctl enable --now docker
sudo usermod -a -G docker ec2-user

git clone https://github.com/OsinsqLew/Phishing-Awareness-Simulation-Tool-
cd Phishing-Awareness-Simulation-Tool-
curl -L "https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/resolve/main/zephyr-7b-beta.Q4_K_M.gguf?download=true" --create-dirs -o "./backend/AI_emails/models/zephyr-7b-beta.Q4_K_M.gguf"
```
Połączyć się z instancją po SSH: `ssh -i <key>.pem ec2-user@<ip_addr>`\
Udostępnić niezbędne porty w `Security Groups`\
Zmodyfikować `config.ini` oraz `docker-compose up`\

<br>

## Zrzuty ekranu

![users](https://github.com/user-attachments/assets/c7a455a3-b40d-4d9c-9fa5-9011d46380d4)
![emails](https://github.com/user-attachments/assets/544e2c19-57a5-480b-abc6-8b626f68ca39)

<!--
![IMG_2577](https://github.com/user-attachments/assets/4dccfbc2-9beb-4f1a-98e0-f7336634212e)
![IMG_2578](https://github.com/user-attachments/assets/54831370-b846-4d54-bf9b-784a410bdc7c)
![IMG_2579](https://github.com/user-attachments/assets/c335bfd7-c75e-487f-97ee-a690ac813c87)
-->

<div display="flex">
  <img src="https://github.com/user-attachments/assets/4dccfbc2-9beb-4f1a-98e0-f7336634212e" width="45%" alt="email example 1"/>
  <img src="https://github.com/user-attachments/assets/54831370-b846-4d54-bf9b-784a410bdc7c" width="45%" alt="email example 2"/>
  <img src="https://github.com/user-attachments/assets/c335bfd7-c75e-487f-97ee-a690ac813c87" width="45%" alt="email example 3"/>
</div>


