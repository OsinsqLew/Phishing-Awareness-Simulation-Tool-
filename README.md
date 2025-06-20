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
Zmodyfikować `config.ini` i następnie `docker-compose up`\
Udostępnić niezbędne porty z `Security Groups`
