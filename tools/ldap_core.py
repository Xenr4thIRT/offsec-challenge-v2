from ldap3 import Server, Connection, ALL
from configs.settings import LDAP_SERVER, LDAP_USER, LDAP_PASSWORD

def get_ldap_connection():
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)
    return conn
