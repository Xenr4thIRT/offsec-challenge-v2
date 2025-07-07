from tools.ldap_tools import (
    get_current_user_info,
    get_user_groups,
    get_all_users,
    get_all_groups,
    get_weak_password_users,
    get_critical_users,
    get_sensitive_groups,
    map_user_group_relations,
    summarize_attack_surface,
)

TOOL_REGISTRY = {
    "get_current_user_info": {
        "func": get_current_user_info,
        "description": "Devuelve la información del usuario actual (admin).",
        "example": "¿Quién soy? / ¿Cuál es mi información?"
    },
    "get_user_groups": {
        "func": get_user_groups,
        "description": "Devuelve los grupos a los que pertenece un usuario.",
        "example": "¿Qué grupos tengo? / ¿Qué grupos tiene john.doe?"
    },
    "get_all_users": {
        "func": get_all_users,
        "description": "Devuelve la lista de todos los usuarios en el LDAP.",
        "example": "¿Qué usuarios existen?"
    },
    "get_all_groups": {
        "func": get_all_groups,
        "description": "Devuelve la lista de todos los grupos definidos en el LDAP.",
        "example": "¿Qué grupos existen?"
    },
    "get_weak_password_users": {
        "func": get_weak_password_users,
        "description": "Detecta usuarios con contraseñas débiles conocidas.",
        "example": "¿Qué usuarios tienen contraseñas débiles?"
    },
    "get_critical_users": {
        "func": get_critical_users,
        "description": "Lista usuarios críticos según título y rol.",
        "example": "¿Quiénes son los usuarios críticos?"
    },
    "get_sensitive_groups": {
        "func": get_sensitive_groups,
        "description": "Lista grupos sensibles o con privilegios críticos.",
        "example": "¿Qué grupos son sensibles?"
    },
    "map_user_group_relations": {
        "func": map_user_group_relations,
        "description": "Mapa relaciones entre usuarios y grupos.",
        "example": "¿Cómo se relacionan usuarios y grupos?"
    },
    "summarize_attack_surface": {
        "func": summarize_attack_surface,
        "description": "Resumen ofensivo de superficie de ataque combinada.",
        "example": "¿Cuál es la superficie de ataque?"
    }
}

def list_tools():
    return [
        f"- {name}: {data['description']} | Ejemplo: {data['example']}"
        for name, data in TOOL_REGISTRY.items()
    ]
