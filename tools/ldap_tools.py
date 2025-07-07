from .ldap_core import get_ldap_connection
from configs.settings import BASE_DN

def get_current_user_info():
    """
    Devuelve toda la información del usuario actual (admin).
    """
    try:
        conn = get_ldap_connection()
        conn.search(
            search_base=BASE_DN,
            search_filter="(cn=admin)",
            attributes=["*"]
        )
        return conn.entries
    except Exception as e:
        print(f"Error al obtener info del usuario actual: {e}")
        return []

def get_user_groups(username):
    """
    Devuelve los nombres de los grupos a los que pertenece el usuario con cn=username.
    """
    try:
        conn = get_ldap_connection()
        user_dn = f"cn={username},ou=users,{BASE_DN}"
        group_search_base = f"ou=groups,{BASE_DN}"
        group_filter = f"(member={user_dn})"
        conn.search(
            search_base=group_search_base,
            search_filter=group_filter,
            attributes=["cn"]
        )
        return [entry.cn.value for entry in conn.entries]
    except Exception as e:
        print(f"Error al buscar grupos del usuario '{username}': {e}")
        return []

def get_all_users():
    """
    Devuelve una lista con todos los usuarios en LDAP (sus CNs).
    """
    try:
        conn = get_ldap_connection()
        search_base = f"ou=users,{BASE_DN}"
        search_filter = "(objectClass=inetOrgPerson)"
        attributes = ["cn"]
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes
        )
        return [entry.cn.value for entry in conn.entries]
    except Exception as e:
        print(f"Error al obtener la lista de usuarios: {e}")
        return []

def get_all_groups():
    """
    Devuelve una lista con todos los grupos definidos en LDAP (sus CNs).
    """
    try:
        conn = get_ldap_connection()
        search_base = f"ou=groups,{BASE_DN}"
        search_filter = "(objectClass=groupOfNames)"
        attributes = ["cn"]
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes
        )
        return [entry.cn.value for entry in conn.entries]
    except Exception as e:
        print(f"Error al obtener la lista de grupos: {e}")
        return []

def get_weak_password_users():
    """
    Devuelve una lista de usuarios con contraseñas débiles conocidas.
    """
    try:
        weak_passwords = ["password123", "123456", "admin", "itachi", "meli123"]
        conn = get_ldap_connection()
        search_base = f"ou=users,{BASE_DN}"
        search_filter = "(objectClass=inetOrgPerson)"
        attributes = ["cn", "userPassword"]
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes
        )
        weak_users = []
        for entry in conn.entries:
            pwd = entry.userPassword.value
            if isinstance(pwd, bytes):
                pwd = pwd.decode(errors="ignore")
            for weak in weak_passwords:
                if weak in pwd:
                    weak_users.append(entry.cn.value)
                    break
        return weak_users
    except Exception as e:
        print(f"Error al detectar contraseñas débiles: {e}")
        return []

def get_critical_users():
    """
    Devuelve usuarios considerados críticos según su título.
    """
    try:
        keywords = ["Manager", "Security", "Senior", "Administrator", "Engineer"]
        conn = get_ldap_connection()
        search_base = f"ou=users,{BASE_DN}"
        search_filter = "(objectClass=inetOrgPerson)"
        attributes = ["cn", "title"]
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes
        )
        critical_users = []
        for entry in conn.entries:
            title = str(entry.title.value).lower() if entry.title else ""
            if any(k.lower() in title for k in keywords):
                critical_users.append(entry.cn.value)
        return critical_users
    except Exception as e:
        print(f"Error al buscar usuarios críticos: {e}")
        return []

def get_sensitive_groups():
    """
    Devuelve grupos considerados sensibles por su nombre.
    """
    try:
        sensitive_names = ["admins", "hr", "finance", "it", "devops", "security"]
        conn = get_ldap_connection()
        search_base = f"ou=groups,{BASE_DN}"
        search_filter = "(objectClass=groupOfNames)"
        attributes = ["cn"]
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes
        )
        critical_groups = []
        for entry in conn.entries:
            if entry.cn.value.lower() in sensitive_names:
                critical_groups.append(entry.cn.value)
        return critical_groups
    except Exception as e:
        print(f"Error al buscar grupos sensibles: {e}")
        return []

def map_user_group_relations():
    """
    Mapea relaciones entre usuarios y grupos.
    """
    try:
        conn = get_ldap_connection()
        user_base = f"ou=users,{BASE_DN}"
        group_base = f"ou=groups,{BASE_DN}"
        user_filter = "(objectClass=inetOrgPerson)"
        group_filter = "(objectClass=groupOfNames)"
        conn.search(
            search_base=user_base,
            search_filter=user_filter,
            attributes=["cn"]
        )
        users = [entry.cn.value for entry in conn.entries]
        relations = {}
        for user in users:
            user_dn = f"cn={user},ou=users,{BASE_DN}"
            conn.search(
                search_base=group_base,
                search_filter=f"(member={user_dn})",
                attributes=["cn"]
            )
            group_list = [entry.cn.value for entry in conn.entries]
            if group_list:
                relations[user] = group_list
        return relations
    except Exception as e:
        print(f"Error al mapear relaciones usuario-grupo: {e}")
        return {}

def summarize_attack_surface():
    """
    Resume usuarios débiles, críticos y grupos sensibles para evaluar la superficie de ataque.
    """
    try:
        weak = get_weak_password_users()
        critical = get_critical_users()
        sensitive = get_sensitive_groups()
        mapping = map_user_group_relations()
        summary = {
            "usuarios_contraseñas_débiles": weak,
            "usuarios_críticos": critical,
            "grupos_sensibles": sensitive,
            "relaciones_usuario_grupo": mapping
        }
        return summary
    except Exception as e:
        print(f"Error al generar el resumen de superficie de ataque: {e}")
        return {}
