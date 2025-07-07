# 🛡️ Desafío Técnico OffSec v2 [UPDATED] - Agente IA Mono-Agente para Infraestructura LDAP con Capacidades Ofensivas Mejoradas

## 📌 Descripción General

Este proyecto resuelve el desafío técnico del equipo de Offensive Security de **Mercado Libre**, mediante un **sistema mono-agente de IA** que interactúa con un servidor **OpenLDAP** para responder consultas en lenguaje natural utilizando herramientas específicas.

Esta versión [UPDATED] incorpora un agente IA más inteligente y ofensivo, que no solo ejecuta herramientas, sino que también:

- Planifica automáticamente estrategias ofensivas multi-herramienta.
- Realiza análisis ofensivos contextualizados con el framework **MITRE ATT&CK**.
- Detecta usuarios con contraseñas débiles y usuarios críticos.
- Identifica grupos sensibles y mapea relaciones usuario-grupo.
- Genera reportes en diferentes niveles de detalle bajo demanda.

El sistema fue desarrollado en **Python**, con soporte para **Google Gemini 1.5 Flash**, implementando tanto las herramientas base como tools con un enfoque más ofensivo.

---

## 🧠 Arquitectura

```
Mono-agente LDAP
├── Agente Ejecutador
│   ├── Gemini 1.5 Flash
│   ├── Herramientas base y ofensivas extendidas
│   └── Conexión dinámica a OpenLDAP
```

---

## 🧐 Capacidades Implementadas

### Herramientas base (requeridas):
- `get_current_user_info()`: Devuelve la información del usuario actual (admin).
- `get_user_groups(username)`: Devuelve los grupos a los que pertenece un usuario.

### Herramientas ofensivas adicionales:
- `get_all_users()`: Lista todos los usuarios.
- `get_all_groups()`: Lista todos los grupos.
- `get_weak_password_users()`: Detecta usuarios con contraseñas débiles conocidas.
- `get_critical_users()`: Lista usuarios críticos según título y rol.
- `get_sensitive_groups()`: Lista grupos sensibles o con privilegios altos.
- `map_user_group_relations()`: Mapea relaciones entre usuarios y grupos.
- `summarize_attack_surface()`: Resumen ofensivo de superficie de ataque combinada.

### Funcionalidades clave añadidas:
- Planificación automática de consultas simples o planes multi-herramienta.
- Análisis ofensivo con contexto MITRE ATT&CK, en modo resumen o detallado.
- Pregunta interactiva para ampliar análisis ofensivo.
- Listado de herramientas disponibles con ejemplos.
- Manejo básico de errores y sugerencias.

---

## 📁 Estructura del Proyecto

```
offsec_challenge/
├── agents/
│   └── mono_agent.py        # Lógica del agente principal
├── tools/
│   ├── ldap_core.py         # Conexion al servidor LDAP
│   ├── ldap_tools.py        # Implementación de herramientas ofensivas y base
│   └── tool_registry.py     # Registro de herramientas disponibles
├── configs/
│   └── settings.py          # Variables de entorno (dotenv)
├── open_ldap_files/         # Infraestructura LDAP (docker)
├── README.md
├── main.py
├── pyproject.toml
└── poetry.lock
```

---

## 🚀 Ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/Xenr4thIRT/offsec-challenge-v2
cd offsec-challenge
```

### 2. Configura el entorno

```bash
cp .env.example .env
nano .env
# Completen las variables con la configuración (como la API key de Gemini, etc.)
```

### 3. Levanta el entorno LDAP

```bash
cd open_ldap_files
./setup-ldap.sh
```

### 4. Activa el entorno virtual y ejecutá

```bash
poetry install
poetry shell
poetry run python main.py
```

---

## 🦺 Ejemplos de uso

```bash
🔍 Consulta LDAP >> ¿Quién es el usuario actual?
🔍 Consulta LDAP >> ¿Cuáles son todos los usuarios del LDAP?
🔍 Consulta LDAP >> ¿Quiénes son los usuarios críticos en el sistema?
🔍 Consulta LDAP >> ¿Cómo se relacionan los usuarios con los grupos?
🔍 Consulta LDAP >> ¿Qué usuarios con contraseñas débiles pertenecen a grupos sensibles?
🔍 Consulta LDAP >> ¿Cuál es la superficie de ataque de este LDAP?
🔍 Consulta LDAP >> ¿Qué grupos son sensibles o de alto riesgo?
🔍 Consulta LDAP >> Dame un resumen ofensivo de la superficie de ataque.
🔍 Consulta LDAP >> Muéstrame un plan para evaluar la seguridad general del LDAP.
🔍 Consulta LDAP >> ¿Qué pasos seguiría un atacante para escalar privilegios en este entorno?
🔍 Consulta LDAP >> ¿Qué información sensible está expuesta en esta infraestructura LDAP?
🔍 Consulta LDAP >> herramientas
🔍 Consulta LDAP >> salir
```

Luego de cada consulta, el agente pregunta si se desea un análisis ofensivo extendido con tácticas MITRE ATT&CK específicas.

---

## 🧰 Tecnologías

- 🐍 Python 3.10+
- 🧠 Google Gemini 1.5 Flash
- 📆 Poetry
- 📚 OpenLDAP + phpLDAPAdmin (simulado)
- 🔐 python-ldap3

---

## ✅ Checklist del Challenge

| Requisito                                 | Estado      |
|------------------------------------------|-------------|
| Conectividad con servidor LDAP           | ✅ Completo |
| Uso de Gemini (IA generativa)            | ✅ Completo |
| Herramientas base (`get_user_groups`)    | ✅ Completo |
| Herramientas base (`get_current_user_info`) | ✅ Completo |
| Implementación simple y funcional        | ✅ Completo |
| Herramientas ofensivas añadidas        | ✅ Completo |
| Planificación ofensiva multi-herramienta | ✅ Completo |
| Análisis ofensivo contextualizado MITRE  | ✅ Completo |
| Interfaz interactiva y análisis opcional | ✅ Completo |
| Logging / Manejo de errores básico       | ✅ Completo |
| Documentación actualizada                 | ✅ Completo |

---

## 📬 Contacto

Desarrollado por **Miguel Larreal Acosta** - *candidato para el equipo de Offensive Security de Mercado Libre*.
