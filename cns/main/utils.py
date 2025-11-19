from cryptography.fernet import Fernet
from django.conf import settings

def get_cipher():
    return Fernet(settings.GLOBAL_CHAT_KEY.encode())

def encrypt_message(plaintext):
    cipher = get_cipher()
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt_message(ciphertext):
    cipher = get_cipher()
    return cipher.decrypt(ciphertext.encode()).decode()


#print(Fernet.generate_key().decode())
