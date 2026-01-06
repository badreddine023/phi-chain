import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LiveKeyManager")

class LiveKeyManager:
    """
    Manages cryptographic keys with AES-256 encryption and rotation.
    """
    def __init__(self, master_password: str):
        self.master_password = master_password.encode()
        self.salt = os.urandom(16)
        self.key = self._derive_key()

    def _derive_key(self):
        """Derive a 256-bit key from the master password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.master_password)

    def encrypt_key(self, plain_key: str) -> str:
        """Encrypt a key using AES-256."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_key = encryptor.update(plain_key.encode()) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_key).decode()

    def decrypt_key(self, encrypted_data: str) -> str:
        """Decrypt a key using AES-256."""
        data = base64.b64decode(encrypted_data)
        iv = data[:16]
        encrypted_key = data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(encrypted_key) + decryptor.finalize()).decode()

    def rotate_keys(self):
        """Rotate the master key (placeholder logic)."""
        logger.info("Rotating keys...")
        self.salt = os.urandom(16)
        self.key = self._derive_key()
        # In a real system, you'd re-encrypt all stored keys with the new master key

if __name__ == "__main__":
    manager = LiveKeyManager("super_secret_password")
    secret = "my_private_blockchain_key"
    encrypted = manager.encrypt_key(secret)
    print(f"Encrypted: {encrypted}")
    decrypted = manager.decrypt_key(encrypted)
    print(f"Decrypted: {decrypted}")
