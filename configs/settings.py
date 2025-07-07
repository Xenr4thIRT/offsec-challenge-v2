import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Falta definir GEMINI_API_KEY en el archivo .env")

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://localhost:389")
LDAP_USER = os.getenv("LDAP_USER", "cn=admin,dc=meli,dc=com")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "itachi")
BASE_DN = os.getenv("BASE_DN", "dc=meli,dc=com")
