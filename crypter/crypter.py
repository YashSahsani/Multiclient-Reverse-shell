import base64
from cryptography.fernet import Fernet
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from cryptography.fernet import Fernet
password_provided = "V3ryS3cur3P4ssw0rd" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = "SocketProgrammingisCool".encode() # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
input_file = sys.argv[1]
output_file = 'payload.encrypted'
with open(input_file, 'rb') as f:
    data = f.read()
fernet = Fernet(key)
encrypted = fernet.encrypt(data)
payload = base64.b64encode(encrypted) 
print(payload)
with open("encrpted_payload.txt","wb") as file_to_write:
          file_to_write.write(payload)
file_to_write.close() 
