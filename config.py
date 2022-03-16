# Import modules
import os


class Config:
    """Set configuration variables from .env file"""

    # Load variables
    USER = os.getenv("ADMIN_USER")
    PASS = os.getenv("ADMIN_PASS")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

