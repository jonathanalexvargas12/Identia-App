# usuarios/models.py - VERSIÓN CORREGIDA (SIN MODELO PERSONALIZADO)
"""
Modelos para la aplicación de usuarios.
NO usamos modelo de usuario personalizado porque:
1. Ya tenemos tablas existentes en MariaDB
2. Usamos CustomBackend para autenticación
3. Evitamos conflictos con auth.User de Django
"""

from django.db import models

# ==============================================
# MODELO 1: TiposPersonal
# ==============================================

class TiposPersonal(models.Model):
    """
    Equivalente a tu tabla tipos_personal.
    Clasifica a los usuarios por categorías.
    """
    id_pk = models.AutoField(primary_key=True, db_column='id_pk')
    nombre_tipo = models.CharField(max_length=50, db_column='nombre_tipo')
    
    class Meta:
        db_table = 'tipos_personal'
        verbose_name = 'Tipo de Personal'
        verbose_name_plural = 'Tipos de Personal'
    
    def __str__(self):
        return self.nombre_tipo

# ==============================================
# MODELO 2: Empleado (antes llamado Usuarios)
# ==============================================

class Empleado(models.Model):
    """
    Equivalente a tu tabla 'usuarios'.
    Contiene información personal y laboral.
    NOTA: NO es un modelo de autenticación, solo datos.
    """
    id_pk = models.AutoField(primary_key=True, db_column='id_pk')
    tipo_fk = models.ForeignKey(
        TiposPersonal,
        on_delete=models.CASCADE,
        db_column='tipo_fk',
        related_name='empleados'
    )
    cedula = models.CharField(max_length=8, unique=True, db_column='cedula')
    nombres = models.CharField(max_length=100, db_column='nombres')
    apellidos = models.CharField(max_length=100, db_column='apellidos')
    direccion_habitacional = models.TextField(db_column='direccion_habitacional')
    correo = models.CharField(max_length=150, db_column='correo')
    numero = models.CharField(max_length=20, db_column='numero')
    estado = models.CharField(max_length=20, db_column='estado')
    area_trabajo = models.CharField(max_length=100, db_column='area_trabajo')
    rol = models.CharField(max_length=50, db_column='rol')
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        indexes = [
            models.Index(fields=['cedula']),
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_fk']),
        ]
    
    def __str__(self):
        return f"{self.cedula} - {self.nombres} {self.apellidos}"
    
    def get_full_name(self):
        """Nombre completo del empleado"""
        return f"{self.nombres} {self.apellidos}"
    
    def esta_activo(self):
        """Verifica si el empleado está activo"""
        return self.estado.lower() == 'activo'

# ==============================================
# MODELO 3: UsuariosAdministrativos
# ==============================================

class UsuariosAdministrativos(models.Model):
    """
    Equivalente a tu tabla 'usuarios_administrativos'.
    Almacena credenciales para acceso al sistema.
    """
    id_pk = models.AutoField(primary_key=True, db_column='id_pk')
    id_usuario_fk = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='id_usuario_fk',
        related_name='credenciales_administrativas'
    )
    password = models.CharField(max_length=255, db_column='password')
    
    class Meta:
        db_table = 'usuarios_administrativos'
        verbose_name = 'Credencial Administrativa'
        verbose_name_plural = 'Credenciales Administrativas'
    
    def __str__(self):
        return f"Admin: {self.id_usuario_fk.cedula}"