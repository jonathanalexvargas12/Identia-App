import subprocess

# 1. Lista de lo que DEFINITIVAMENTE vamos a borrar (Lo que no es Django ni IA facial)
SOBRAS_CONFIRMADAS = [
    'Flask', 'flask-cors', 'beautifulsoup4', 'soupsieve', 
    'Jinja2', 'Werkzeug', 'itsdangerous', 'blinker',
    'deptry', 'pip-check-reqs', 'requirements-parser'
]

def desinstalar():
    print("🚀 Iniciando limpieza de dependencias innecesarias...")
    
    for paquete in SOBRAS_CONFIRMADAS:
        print(f"--- Intentando eliminar: {paquete} ---")
        # Ejecuta el comando de desinstalación de forma silenciosa
        subprocess.run(["pip", "uninstall", paquete, "-y"])

    print("\n✅ Limpieza completada.")
    print("Sugerencia: Ejecuta 'python manage.py runserver' para verificar que todo siga bien.")

if __name__ == "__main__":
    desinstalar()