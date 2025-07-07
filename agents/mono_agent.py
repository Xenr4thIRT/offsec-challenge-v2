import google.generativeai as genai
from tools.tool_registry import TOOL_REGISTRY, list_tools
from configs.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")


def generate_offensive_analysis(tool_name, tool_result, detail=False):
    if detail:
        prompt = f"""
Eres un experto en ciberseguridad ofensiva con conocimiento de MITRE ATT&CK.

El agente IA ejecutó la herramienta '{tool_name}' y obtuvo este resultado:

{tool_result}

Provee un análisis técnico que incluya:
- Riesgos específicos
- Impacto potencial
- Abuso real por un atacante
- Códigos de tácticas y técnicas MITRE ATT&CK relevantes

No repitas información innecesaria. Sé directo y técnico.
Responde en español.
"""
    else:
        prompt = f"""
Eres un agente AI ofensivo.

Este fue el resultado de la herramienta '{tool_name}':
{tool_result}

1. Explica brevemente (máx. 8 líneas):
- Qué daño puede causar esta información si cae en manos de un atacante.
- Qué riesgos reales representa.
- Qué técnicas MITRE ATT&CK podrían usarse y por que.
2. Sin rodeos, directo al grano.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generando análisis ofensivo: {e}"


def run_agent():
    print("Mono-agente LDAP listo. Escribí 'salir' para terminar.")
    print("Escribí 'herramientas' para listar capacidades actuales.\n")

    while True:
        query = input("Consulta LDAP >> ").strip()

        if query.lower() in ["exit", "salir", "quit"]:
            print("Saliendo del agente.")
            break

        if query.lower() in ["herramientas", "tools", "capacidades"]:
            print("\nHerramientas disponibles:")
            for tool in list_tools():
                print(tool)
            print("")
            continue

        planner_prompt = f"""
Eres un agente ofensivo con acceso a un conjunto de herramientas LDAP:

{chr(10).join([f"- {name}" for name in TOOL_REGISTRY.keys()])}

Dado el siguiente mensaje del usuario:
\"\"\"{query}\"\"\"

1. Si se puede responder con UNA sola herramienta, responde:
SINGLE_TOOL: <nombre_de_la_herramienta>

2. Si se necesitan varias herramientas para razonar y llegar al resultado, responde:
PLAN:
- tool: <herramienta_1>
- tool: <herramienta_2>
...

RAZONAMIENTO:
<explicación de por qué usar esas herramientas y cómo se conectan entre sí>

Responde solo en uno de esos dos formatos.
"""

        try:
            plan_response = model.generate_content(planner_prompt).text.strip()

            if plan_response.startswith("SINGLE_TOOL:"):
                tool_name = plan_response.split("SINGLE_TOOL:")[1].strip()
                tool = TOOL_REGISTRY.get(tool_name)
                if not tool:
                    print("No tengo una herramienta para responder esa consulta aún.")
                    continue

                print(f"\n[Agente] Elegí la herramienta: {tool_name}")
                result = tool["func"]()
                print(f"\n[Resultado de {tool_name}]:")
                if isinstance(result, list):
                    if not result:
                        print("No se encontraron datos.")
                    else:
                        for item in result:
                            print("-", item)
                elif isinstance(result, dict):
                    if not result:
                        print("No se encontraron datos.")
                    else:
                        for k, v in result.items():
                            print(f"- {k}: {v}")
                else:
                    print(result)

                print("\n[Análisis ofensivo]:")
                summary = generate_offensive_analysis(tool_name, result, detail=False)
                print(summary)

                choice = input("\n¿Quieres un análisis más detallado y tácticas MITRE ATT&CK específicas? (s/n): ").strip().lower()
                if choice == "s":
                    extended = generate_offensive_analysis(tool_name, result, detail=True)
                    print("\n[Análisis extendido]:")
                    print(extended)

            elif "PLAN:" in plan_response:
                import re

                lines = plan_response.splitlines()
                tools_to_run = [re.search(r"tool:\s*(\w+)", line).group(1) for line in lines if line.strip().startswith("- tool:")]
                rationale_index = next((i for i, line in enumerate(lines) if "RAZONAMIENTO" in line), len(lines))
                rationale = "\n".join(lines[rationale_index + 1:]).strip()

                print("\n[Agente] Elaboré un plan ofensivo:")
                print("- Herramientas a ejecutar:", ", ".join(tools_to_run))
                print("- Razonamiento ofensivo:\n", rationale)

                combined_results = {}
                for tool_name in tools_to_run:
                    tool = TOOL_REGISTRY.get(tool_name)
                    if not tool:
                        print(f" - La herramienta '{tool_name}' no existe.")
                        continue
                    print(f"\n[Ejecutando {tool_name}]")
                    try:
                        result = tool["func"]()
                        combined_results[tool_name] = result
                        if isinstance(result, list):
                            for item in result:
                                print("-", item)
                        elif isinstance(result, dict):
                            for k, v in result.items():
                                print(f"- {k}: {v}")
                        else:
                            print(result)
                    except Exception as e:
                        print(f"Error ejecutando {tool_name}: {e}")

                print("\n[Análisis ofensivo del plan completo]:")
                plan_analysis_prompt = f"""
El agente ejecutó este plan ofensivo: {', '.join(tools_to_run)}.

Estos fueron los resultados obtenidos por cada herramienta:
{combined_results}

Haz un análisis ofensivo compacto: qué riesgos se descubrieron, cómo puede usarse en una intrusión, y técnicas MITRE ATT&CK asociadas. Sé directo.

Responde en español.
"""
                try:
                    analysis = model.generate_content(plan_analysis_prompt).text.strip()
                    print(analysis)
                    choice = input("\n¿Quieres un análisis más detallado del plan ofensivo? (s/n): ").strip().lower()
                    if choice == "s":
                        plan_analysis_prompt += "\nAmplía los detalles técnicos, escenarios de abuso y tácticas MITRE ATT&CK precisas."
                        extended = model.generate_content(plan_analysis_prompt).text.strip()
                        print("\n[Análisis extendido del plan]:")
                        print(extended)
                except Exception as e:
                    print(f"Error al generar análisis del plan: {e}")

            else:
                print("No entendí la respuesta del planificador IA.")

        except Exception as e:
            print(f"Error al consultar Gemini: {e}")
            continue

        print("\n" + "=" * 50 + "\n")
