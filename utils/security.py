"""
Security utilities.
Handles password hashing, encryption, and data protection.
"""

import hashlib
import secrets
from typing import Optional

from cryptography.fernet import Fernet
from loguru import logger
from config.settings import settings


class SecurityManager:
    """Security and cryptography manager."""

    def __init__(self):
        """Initialize security manager."""
        # Generate encryption key
        secret = settings.SECRET_KEY.encode()
        key = hashlib.sha256(secret).digest()
        # Use only first 32 bytes for Fernet
        self.cipher = Fernet(self._derive_key(key))
        logger.info("SecurityManager initialized")

    @staticmethod
    def _derive_key(secret: bytes) -> bytes:
        """Derive a valid Fernet key from secret."""
        import base64
        derived = hashlib.sha256(secret).digest()
        return base64.urlsafe_b64encode(derived)

    # ===================== Password Hashing =====================

    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> str:
        """
        Hash password using PBKDF2.
        
        Args:
            password: Plain password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Salted hash of password
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        else:
            if isinstance(salt, str):
                salt = bytes.fromhex(salt)

        # Use PBKDF2 for password hashing
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,
        )

        # Return salt + hash as hex string
        return f"{salt.hex()}${hash_obj.hex()}"

    @staticmethod
    def verify_password(password: str, hash_string: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain password to verify
            hash_string: Stored hash
            
        Returns:
            True if password matches
        """
        try:
            salt_hex, hash_hex = hash_string.split('$')
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)

            # Hash provided password with same salt
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000,
            )

            # Compare hashes
            return new_hash == stored_hash
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    # ===================== Data Encryption =====================

    def encrypt_sensitive_data(self, data: str) -> str:
        """
        Encrypt sensitive data (API keys, tokens).
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data as string
        """
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return ""

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data string
            
        Returns:
            Decrypted data
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return ""

    # ===================== Secure Token Generation =====================

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(length)

    # ===================== Data Validation =====================

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_strong_password(password: str) -> bool:
        """
        Check if password is strong.
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(password) < 8:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)

        return has_upper and has_lower and has_digit and has_special
