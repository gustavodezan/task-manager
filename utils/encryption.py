import os
from pathlib import Path
from dotenv import load_dotenv

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

def turn_into_key(key_key):
    password_provided = key_key 
    password = password_provided.encode() # convert to bytes

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.getenv("ENC_SALT").encode(),
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key

def encrypt(data: str) -> bytes:
    # criptografar uma string
    key = os.getenv("ENCRYPTION_KEY").encode()
    encoded = (data.encode())
    enc = Fernet(key)
    encrypted = enc.encrypt(encoded)
    return encrypted

def decrypt(data: bytes) -> str:
    # decrypt a bytes info into a string
    key = os.getenv("ENCRYPTION_KEY").encode()
    dec = Fernet(key)
    decrypted = dec.decrypt(data)
    original_data = decrypted.decode()
    return original_data

def encrypt_user(user: dict) -> dict:
    for key, value in user.items():
        if key == "password" or key == "key" or key == "scopes" or value == None or type(value) == bool or key == "active" or key == "teams":
            continue
        elif type(value) == list:
            temp_list = []
            for i in value:
                temp_list.append(encrypt(str(i)).decode("utf-8"))
            user[key] = temp_list
        else:
            user[key] = encrypt(str(value)).decode("utf-8")
    return user

def decrypt_user(user: dict) -> dict:
    for item in user:
        if item == "id" or item == "key" or item == "password" or item == "scopes" or item == "teams" or item == "active" or user[item] == None:
            continue
        if type(user[item]) == list:
            temp_list = []
            for i in user[item]:
                temp_list.append(decrypt(i))
            user[item] = temp_list
        else:
            user[item] = decrypt(user[item])
    return user

def decrypt_user_preview(user: dict) -> dict:
    for item in user:
        if item == "name" or item == "email":
            user[item] = decrypt(user[item])
    return user

if __name__ == "__main__":
    h = encrypt("Hello World")
    print(h)
    data = decrypt(h)
    print(data)