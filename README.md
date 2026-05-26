# [ESCRIBE AQUÍ EL TÍTULO DEL PROYECTO]

> [ESCRIBE AQUÍ UNA BREVE DESCRIPCIÓN DEL PROYECTO: Ej. Sistema integral de gestión de asistencia y reconocimiento facial para entornos corporativos.]

---

## ✍️ Información del Autor
* **Nombre:** [ESCRIBE TU NOMBRE AQUÍ]
* **Institución:** [NOMBRE DE TU UNIVERSIDAD / POSGRADO]
* **Contacto:** [TU CORREO O ENLACE A LINKEDIN]

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

## 🔒 Medidas de Seguridad

### Seguridad del Lado del Servidor (Backend)

#### Middlewares de Seguridad
El sistema implementa varios middlewares personalizados para proteger la aplicación:

1. **SecurityHeadersMiddleware**
   - Añade cabeceras HTTP de seguridad
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin
   - Cache-Control: no-store, no-cache

2. **DeveloperOnlyAccessMiddleware**
   - Restringe acceso a rutas de desarrollo (/admin/, /api/debug/, /dev/)
   - Solo permite acceso a usuarios con rol de desarrollador, superusers o staff

3. **RequestValidationMiddleware**
   - Valida headers de requests
   - Bloquea headers sospechosos de herramientas de desarrollo
   - Verifica User-Agent y bloquea agentes no autorizados

4. **DisableSessionCookiesMiddleware**
   - Protege cookies con HttpOnly, Secure y SameSite=Strict
   - Previene robo de cookies por XSS

#### Decoradores de Seguridad
- `@developer_required`: Decorador para vistas que solo desarrolladores pueden acceder
- `@api_developer_required`: Decorador específico para APIs
- Función `is_developer()`: Verifica rol, superuser, staff o grupo

#### Configuración de Cookies
- SESSION_COOKIE_SECURE: True (solo HTTPS)
- SESSION_COOKIE_HTTPONLY: True (no accesible por JS)
- SESSION_COOKIE_SAMESITE: 'Strict'
- AUTH_COOKIE_SECURE: True

---

### Seguridad del Lado del Cliente (Frontend)

Para usuarios que **NO** tienen rol de desarrollador, el sistema bloquea:

1. **Teclas y Combinaciones**
   - F12 (Herramientas de desarrollo)
   - Ctrl+C/V/X (Copiar/Pegar/Cortar)
   - Ctrl+U (Ver código fuente)
   - Ctrl+S (Guardar página)
   - Ctrl+A (Seleccionar todo)
   - Ctrl+I/J (Herramientas de desarrollo)

2. **Menú Contextual**
   - Clic derecho deshabilitado

3. **Selección y Arrastre**
   - Selección de texto deshabilitada
   - Arrastrar y soltar deshabilitado
   - Copy/Paste/Cut fuera de inputs

4. **Detección de DevTools**
   - Detecta apertura de herramientas de desarrollo por tamaño de ventana

### Roles de Usuario

El sistema identifica desarrolladores mediante:
- `request.session.empleado_rol` conteniendo "desarrollador", "developer" o "desarrollo"
- Usuario Django con `is_superuser = True`
- Usuario Django con `is_staff = True`
- Usuario pertenenciente a grupo con "desarrollador" en el nombre

### Limitaciones

> [!IMPORTANT]
> Las medidas de seguridad del lado del cliente (JavaScript) son principalmente **disuasorias** y pueden ser evitadas por usuarios con conocimientos técnicos avanzados.
> 
> La seguridad real está implementada en el backend mediante:
> - Middlewares de protección
> - Decoradores de acceso
> - Cabeceras de seguridad HTTP
> - Cookies seguras

---

## 📊 Reportes

* **Módulo de Reportes:** Generación de informes detallados para auditoría y toma de decisiones.
* **Formatos:** PDF generado con ReportLab.
* **Módulos reportables:**
  - Gestión de Trabajadores
  - Horarios
  - Bitácora de Incidentes
  - Tipos de Personal
  - Bitácora de Asistencias
* **Filtros:** Por trabajador/tipo y rango de fechas.

---

## 🚧 Estado del Desarrollo (Roadmap)

Los módulos del sistema se encuentran actualmente en desarrollo activo. 

### 📢 Próximamente:
* **Control de acceso:** Registro biométrico en tiempo real integrado.
* **Bitácora de Incidentes:** Registro histórico de eventos críticos y seguridad.
* **Bitácora de Asistencias:** Visualización y reporte detallado de entradas y salidas.

> [!NOTE]
> El módulo de **Bitácora de Incidentes** estará disponible próximamente como parte de la fase final de implementación.

---

## 🛠️ Instalación y Uso

### Opción A: Ejecución Local
1. Crear Entorno Virtual:
   python3.11 -m venv identia_venv 
   ALTERNATIVA: py -3.11 -m venv identia_venv
    
2. Activa el entorno virtual:
   `.\identia_venv\Scripts\activate` (Windows) o `source identia_venv/bin/activate` (Linux/Mac)
3. Instala las dependencias:
   `pip install -r requirements.txt`
4. Ejecuta las migraciones:
   `python manage.py migrate`
5. Inicia el servidor:
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

