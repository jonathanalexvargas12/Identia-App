# usuarios/backends.py
"""
Backend personalizado de autenticación para Terminal de Transporte.
Autentica contra las tablas existentes en MariaDB.
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import connection
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class CustomAuthenticationBackend(BaseBackend):
    """
    Backend que autentica usando:
    1. id_usuario_fk (de tabla 'usuarios_administrativos')
    2. Password (de tabla 'usuarios_administrativos')
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica un usuario usando id_usuario_fk como username.
        
        Args:
            username: ID de usuario (id_usuario_fk como string)
            password: Contraseña en texto plano
            
        Returns:
            User object si éxito, None si falla
        """
        if not username or not password:
            logger.warning("Intento de login sin ID de usuario o password")
            return None
        
        logger.info(f"Intento de autenticación para ID usuario: {username}")
        
        try:
            with connection.cursor() as cursor:
                # 1. Validar que el ID es numérico
                try:
                    user_id = int(username)
                except ValueError:
                    logger.warning(f"ID de usuario no válido (no numérico): {username}")
                    if request:
                        messages.error(request, 'ID de usuario debe ser numérico')
                    return None
                
                # 2. Buscar credencial administrativa por id_usuario_fk
                cursor.execute("""
                    SELECT 
                        ua.id_usuario_fk, ua.password,
                        u.id_pk, u.cedula, u.nombres, u.apellidos, 
                        u.correo, u.estado
                    FROM usuarios_administrativos ua
                    INNER JOIN usuarios u ON u.id_pk = ua.id_usuario_fk
                    WHERE ua.id_usuario_fk = %s 
                    AND u.estado = 'Activo'
                    LIMIT 1
                """, [user_id])
                
                resultado = cursor.fetchone()
                
                if not resultado:
                    logger.warning(f"ID de usuario no encontrado o usuario inactivo: {user_id}")
                    if request:
                        messages.error(request, 'ID de usuario no encontrado o usuario inactivo')
                    return None
                
                # Desempaquetar resultado
                (id_usuario_fk, password_hash,
                 emp_id, cedula, nombres, apellidos, 
                 correo, estado) = resultado
                
                # 3. Verificar password
                password_valido = False
                
                # Intentar diferentes formatos de hash
                if password_hash.startswith('pbkdf2_sha256$'):
                    # Formato Django (recomendado)
                    password_valido = check_password(password, password_hash)
                    logger.debug(f"Password en formato Django PBKDF2")
                elif password_hash.startswith('bcrypt$'):
                    # Formato bcrypt
                    password_valido = check_password(password, password_hash)
                    logger.debug(f"Password en formato bcrypt")
                else:
                    # Password en texto plano (solo para desarrollo)
                    # ¡ADVERTENCIA! Esto es INSECURO para producción
                    password_valido = (password == password_hash)
                    if password_valido:
                        logger.warning(f"Password en texto plano para ID {user_id} - ¡INSEGURO!")
                        # Hashear y actualizar el password
                        nuevo_hash = make_password(password)
                        cursor.execute("""
                            UPDATE usuarios_administrativos 
                            SET password = %s 
                            WHERE id_usuario_fk = %s
                        """, [nuevo_hash, user_id])
                        connection.commit()
                
                if not password_valido:
                    logger.warning(f"Password incorrecto para ID usuario: {user_id}")
                    if request:
                        messages.error(request, 'Contraseña incorrecta')
                    return None
                
                logger.info(f"Autenticación exitosa: ID {user_id} - {nombres} {apellidos}")
                
                # 4. Crear o obtener usuario de Django
                # Usamos id_usuario_fk como username para Django
                django_username = str(user_id)
                
                user, created = User.objects.get_or_create(
                    username=django_username,
                    defaults={
                        'email': correo or f"{user_id}@terminal.com",
                        'first_name': nombres,
                        'last_name': apellidos,
                        'is_staff': True,  # Acceso al admin básico
                        'is_active': True,
                    }
                )
                
                if created:
                    logger.info(f"Nuevo usuario Django creado: {django_username}")
                else:
                    # Actualizar datos si el usuario ya existía
                    user.email = correo or f"{user_id}@terminal.com"
                    user.first_name = nombres
                    user.last_name = apellidos
                    user.save()
                
                # 5. Guardar datos adicionales en la sesión
                if request:
                    request.session['empleado_id'] = emp_id
                    request.session['empleado_cedula'] = cedula
                    request.session['empleado_nombres'] = nombres
                    request.session['empleado_apellidos'] = apellidos
                    request.session['empleado_correo'] = correo
                    request.session['empleado_estado'] = estado
                    request.session['id_usuario_fk'] = user_id  # Nuevo campo
                    request.session['is_authenticated_via_custom'] = True
                
                return user
                
        except Exception as e:
            logger.error(f"Error en autenticación para ID {username}: {str(e)}", exc_info=True)
            if request:
                messages.error(request, f'Error en el servidor: {str(e)}')
            return None
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID (requerido por Django).
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None