CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY,
email_address VARCHAR(255) UNIQUE,
first_name VARCHAR(63),
last_name VARCHAR(63),
hash_pass VARCHAR(63),
salt VARCHAR(6),
tags VARCHAR(63) DEFAULT NULL,
CHECK (email_address REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
);

CREATE TABLE IF NOT EXISTS emails (
email_id INT NOT NULL,
user_id INT NOT NULL,
seen BOOLEAN DEFAULT FALSE,
clicked BOOLEAN DEFAULT FALSE,
tags VARCHAR(63),
phishing_type VARCHAR(255) DEFAULT NULL,
PRIMARY KEY (email_id, user_id),
FOREIGN KEY (user_id) REFERENCES users(id)
);