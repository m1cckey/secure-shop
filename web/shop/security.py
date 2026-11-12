import hashlib
import os
import hmac

def hash_pas(password: str) -> str:
    password_enc = password.encode()
    salt_enc = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password_enc, salt_enc, 100000)
    hex_pass = password_hash.hex()
    salt_hex = salt_enc.hex()
    return f'{hex_pass}@{salt_hex}'

def check_password(password_and_salt: str, password: str) -> list:
    hex_password = password_and_salt.split('@')[0]
    hex_salt = password_and_salt.split('@')[1]
    decoded_salt = bytes.fromhex(hex_salt)
    verif_password = password.encode()
    check_pas = hashlib.pbkdf2_hmac('sha256', verif_password, decoded_salt, 100000)
    check_pas_hex = check_pas.hex()
    return hmac.compare_digest(hex_password, check_pas_hex)



