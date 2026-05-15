# [ESCRIBE AQUÍ EL TÍTULO DEL PROYECTO]

> [ESCRIBE AQUÍ UNA BREVE DESCRIPCIÓN DEL PROYECTO: Ej. Sistema integral de gestión de asistencia y reconocimiento facial para entornos corporativos.]

---

## ✍️ Información del Autor
* **Nombre:** José Daniel Betancourt Garcia | Jonathan Alexander Vargas
* **Institución:** Independiente
* **Contacto:**  josedanielbetancourt65@gmail.com | jonathanalexvargas@gmail.com

---

## 📂 Estructura del Proyecto

Basado en la arquitectura Django del sistema:

* **config/**: Archivos de configuración principal del proyecto (`settings.py`, `urls.py`).
* **asistencia/**: Módulo para la lógica de gestión de asistencia.
* **usuarios/**: Gestión de perfiles, autenticación y lógica de backends.
* **reconocimiento/**: Procesamiento de datos biométricos y lógica de reconocimiento facial.
* **templates/**: Archivos HTML divididos por módulos (usuarios, reconocimiento).
* **static/**: Recursos estáticos como archivos JavaScript (`update-time.js`) e imágenes.
* **data/** & **logs/**: Almacenamiento de información local y registros de auditoría del sistema.
* **models/**: Definiciones de esquemas de datos.
* **Dockerfile**: Archivo de configuración para la creación de la imagen Docker.
* **.dockerignore**: Lista de archivos excluidos del contenedor (como entornos virtuales locales).

---

## 💻 Tecnologías Utilizadas

* **Lenguaje:** Python 3.11.9
* **Framework Web:** Django 5.1.6
* **Inteligencia Artificial:** DeepFace, TensorFlow, Keras.
* **Base de Datos:** MariaDB / MySQL.
* **Contenedores:** Docker.
* **Variables de Env:** `.env` para la protección de claves y credenciales.

---

## 🔒 Seguridad y Reportes

* **Seguridad:** Configuración avanzada de permisos por roles de usuario y sistema de alertas de seguridad.
* **Reportes:** Generación de informes detallados para auditoría y toma de decisiones.

---

## 🚧 Estado del Desarrollo (Roadmap)

Los módulos del sistema se encuentran actualmente en desarrollo activo. 

### 📢 Próximamente:
* **Control de acceso:** Registro biométrico en tiempo real integrado.
* **Bitácora de Incidentes:** Registro histórico de eventos críticos y seguridad.
* **Bitácora de Asistencias:** Visualización y reporte detallado de entradas y salidas.

> [!NOTE]
> Los módulos de **Bitácora de Incidentes** y **Bitácora de Asistencias** estarán disponibles próximamente como parte de la fase final de implementación.

---

## 🛠️ Instalación y Uso

### Opción A: Ejecución Local
1. Activa el entorno virtual:
   `.\identia_venv\Scripts\activate` (Windows) o `source identia_venv/bin/activate` (Linux/Mac)
2. Instala las dependencias:
   `pip install -r requirements.txt`
3. Ejecuta las migraciones:
   `python manage.py migrate`
4. Inicia el servidor:
   `python manage.py runserver`

### Opción B: Ejecución con Docker (Recomendado)
El proyecto está totalmente dockerizado para garantizar la compatibilidad de las librerías de IA.

1. **Construir la imagen:** (Este proceso puede tardar entre 30 y 60 minutos la primera vez debido al peso de TensorFlow y DeepFace), tambien dependera de su conexion a internet (Esto sólo se hará Es una primera vez, Al menos que se elimine La imagen, Se le haga cambio a las dependencias De ser así se tendrá que repetir este paso).
   ```bash
   docker build -t identia-app .

   Comando de despliegue rápido (Limpiar + Iniciar + Logs):
Ejecute esta línea única para reiniciar el contenedor de cero y ver qué sucede internamente:
docker rm -f identia-container; docker run -d -p 8000:8000 --name identia-container identia-app; docker logs -f identia-container


### ¿Qué hace cada parte?
1.  **`docker rm -f ...`**: Elimina el contenedor viejo (aunque esté prendido) para evitar el error de "Conflict". El `;` le dice a la terminal: "cuando termines esto, haz lo siguiente".
2.  **`docker run -d ...`**: Crea y enciende el contenedor en segundo plano.
3.  **`docker logs -f ...`**: "Engancha" tu terminal a la salida del contenedor para que veas en tiempo real si Django conecta a la base de datos o si hay errores de DeepFace.


### Instalación en Linux (Ubuntu/Debian)
Si se encuentra en Linux, dentro de la carpeta `Recursos necesarios/linux/` encontrará un script de automatización. Para ejecutarlo:
1. Otorgue permisos: `chmod +x install_requirements.sh`
2. Ejecute el script: `./install_requirements.sh`

Finalmente dirigirse a el navegador web de su preferencia, y colocal la ruta:
https://localhost:8000 

[!NOTE]
>Asegurese que para la instalación y uso de la APP, En el terminal en donde vaya a ejecutar los comandos esté abierto como administrador En caso de hacerlo con un terminal externo (Ej. CMD de Windows o El Terminal en Linux), y que se encuentre ubicado en el directorio de la carpeta raíz del proyecto, asi como también, tener los ejecutables especificos necesarios Instalados en su equipo según cual sea su sistema operativo Los cuales se encuentran en el directorio llamado Recursos necesarios, Además de tener importada en el gestor De base de datos El archivo SQL que Se encuentra en el directorio Base de datos. En el caso De decidir ejecutar la aplicación mediante docker Y tener sistema operativo Windows al realizar la ejecución de la aplicación asegúrese de tener Dokkerdesktop Abierto y minimizado para evitar conflictos

