import json
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db import connection
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import os
from config.decorators import role_required


MODULOS = [
    {'id': 'trabajadores', 'nombre': 'Gestión de Trabajadores'},
    {'id': 'horarios', 'nombre': 'Horarios'},
    {'id': 'incidentes', 'nombre': 'Bitácora de Incidentes'},
    {'id': 'tipos_personal', 'nombre': 'Tipos de Personal'},
    {'id': 'asistencias', 'nombre': 'Bitácora de Asistencias'},
]


@login_required
@role_required('Administrador', 'Seguridad')
def index(request):
    """Vista principal del generador de reportes"""
    return render(request, 'reportes/index.html', {
        'modulos': MODULOS,
    })


@login_required
@role_required('Administrador', 'Seguridad')
def buscar(request):
    """API para buscar trabajadores o tipos de personal"""
    modulo = request.GET.get('modulo', '')
    query = request.GET.get('q', '').strip()
    
    resultados = []
    
    if modulo in ['trabajadores', 'incidentes', 'asistencias']:
        # Buscar trabajadores
        resultados = buscar_trabajadores(query)
    elif modulo in ['horarios', 'tipos_personal']:
        # Buscar tipos de personal
        resultados = buscar_tipos_personal(query)
    
    return JsonResponse(resultados, safe=False)


def buscar_trabajadores(query):
    """Busca trabajadores por nombre, apellido o cédula"""
    with connection.cursor() as cursor:
        if query:
            cursor.execute("""
                SELECT id_pk, cedula, nombres, apellidos
                FROM usuarios
                WHERE cedula LIKE %s OR nombres LIKE %s OR apellidos LIKE %s
                ORDER BY nombres, apellidos
                LIMIT 50
            """, [f'%{query}%', f'%{query}%', f'%{query}%'])
        else:
            cursor.execute("""
                SELECT id_pk, cedula, nombres, apellidos
                FROM usuarios
                ORDER BY nombres, apellidos
                LIMIT 50
            """)
        
        return [
            {
                'id': row[0],
                'texto': f"{row[1]} - {row[2]} {row[3]}"
            }
            for row in cursor.fetchall()
        ]


def buscar_tipos_personal(query):
    """Busca tipos de personal por nombre"""
    with connection.cursor() as cursor:
        if query:
            cursor.execute("""
                SELECT id_nombre_tipo
                FROM tipos_personal
                WHERE id_nombre_tipo LIKE %s
                ORDER BY id_nombre_tipo
                LIMIT 50
            """, [f'%{query}%'])
        else:
            cursor.execute("""
                SELECT id_nombre_tipo
                FROM tipos_personal
                ORDER BY id_nombre_tipo
                LIMIT 50
            """)
        
        return [{'id': row[0], 'texto': row[0]} for row in cursor.fetchall()]


@login_required
@role_required('Administrador', 'Seguridad')
def generar_pdf(request):
    """Genera el reporte en PDF según los parámetros"""
    modulo = request.GET.get('modulo', '')
    seleccion_id = request.GET.get('seleccion_id', '')
    desde = request.GET.get('desde', '').strip()
    hasta = request.GET.get('hasta', '').strip()
    
    # Obtener datos según el módulo
    if modulo == 'trabajadores':
        titulo = 'Gestión de Trabajadores'
        columnas, datos = get_datos_trabajadores(seleccion_id)
        nombre_seleccion = get_nombre_trabajador(seleccion_id) if seleccion_id else 'Todos'
        
    elif modulo == 'horarios':
        titulo = 'Horarios'
        columnas, datos = get_datos_horarios(seleccion_id, desde, hasta)
        nombre_seleccion = seleccion_id if seleccion_id else 'Todos'
        
    elif modulo == 'incidentes':
        titulo = 'Bitácora de Incidentes'
        columnas, datos = get_datos_incidentes(seleccion_id, desde, hasta)
        nombre_seleccion = get_nombre_trabajador(seleccion_id) if seleccion_id else 'Todos'
        
    elif modulo == 'tipos_personal':
        titulo = 'Tipos de Personal'
        columnas, datos = get_datos_tipos_personal(seleccion_id)
        nombre_seleccion = seleccion_id if seleccion_id else 'Todos'
        
    elif modulo == 'asistencias':
        titulo = 'Bitácora de Asistencias'
        columnas, datos = get_datos_asistencias(seleccion_id, desde, hasta)
        nombre_seleccion = get_nombre_trabajador(seleccion_id) if seleccion_id else 'Todos'
    else:
        return JsonResponse({'error': 'Módulo no válido'}, status=400)
    
    # Generar PDF
    return crear_pdf(titulo, columnas, datos, nombre_seleccion)


def get_datos_trabajadores(trabajador_id):
    """Obtiene datos de trabajadores"""
    columnas = ['ID', 'Cédula', 'Nombres', 'Apellidos', 'Correo', 'Teléfono', 'Estado', 'Área', 'Rol', 'Tipo']
    
    with connection.cursor() as cursor:
        if trabajador_id:
            cursor.execute("""
                SELECT u.id_pk, u.cedula, u.nombres, u.apellidos, u.correo, 
                       u.numero, u.estado, u.area_trabajo, u.rol, u.tipo_fk
                FROM usuarios u
                WHERE u.id_pk = %s
                ORDER BY u.nombres, u.apellidos
            """, [trabajador_id])
        else:
            cursor.execute("""
                SELECT u.id_pk, u.cedula, u.nombres, u.apellidos, u.correo, 
                       u.numero, u.estado, u.area_trabajo, u.rol, u.tipo_fk
                FROM usuarios u
                ORDER BY u.nombres, u.apellidos
            """)
        
        return columnas, [list(row) for row in cursor.fetchall()]


def get_datos_horarios(tipo_personal, desde='', hasta=''):
    """Obtiene datos de horarios"""
    columnas = ['ID', 'Tipo Personal', 'Fecha', 'Hora Entrada', 'Tolerancia Entrada', 'Hora Salida', 'Tolerancia Salida']
    
    query = """
        SELECT id_pk, tipo_fk, fecha, hora_entrada, tolerancia_entrada, hora_salida, tolerancia_salida
        FROM horarios_jornada
        WHERE 1=1
    """
    params = []
    
    if tipo_personal:
        query += " AND tipo_fk = %s"
        params.append(tipo_personal)
    if desde:
        query += " AND fecha >= %s"
        params.append(desde)
    if hasta:
        query += " AND fecha <= %s"
        params.append(hasta)
    
    query += " ORDER BY fecha DESC, tipo_fk"
    
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultados = []
        for row in cursor.fetchall():
            resultados.append([
                row[0], row[1] or 'General',
                row[2].strftime('%d/%m/%Y') if row[2] else '-',
                str(row[3]) if row[3] else '-',
                str(row[4]) if row[4] else '-',
                str(row[5]) if row[5] else '-',
                str(row[6]) if row[6] else '-',
            ])
        return columnas, resultados


def get_datos_incidentes(trabajador_id, desde='', hasta=''):
    """Obtiene datos de incidentes"""
    columnas = ['ID', 'Fecha', 'Hora', 'Novedad', 'Detalles', 'IP']
    
    query = """
        SELECT id_pk, fecha, hora, novedad, detalles, ip
        FROM bitacora_incidentes
        WHERE 1=1
    """
    params = []
    
    if trabajador_id:
        query += " AND id_usuario_fk = %s"
        params.append(trabajador_id)
    if desde:
        query += " AND fecha >= %s"
        params.append(desde)
    if hasta:
        query += " AND fecha <= %s"
        params.append(hasta)
    
    query += " ORDER BY fecha DESC, hora DESC"
    
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultados = []
        for row in cursor.fetchall():
            resultados.append([
                row[0],
                row[1].strftime('%d/%m/%Y') if row[1] else '-',
                str(row[2]) if row[2] else '-',
                row[3] or '-',
                (row[4][:50] + '...' if row[4] and len(row[4]) > 50 else row[4]) if row[4] else '-',
                row[5] or '-',
            ])
        return columnas, resultados


def get_datos_tipos_personal(tipo_seleccionado):
    """Obtiene datos de tipos de personal"""
    columnas = ['Nombre del Tipo']
    
    with connection.cursor() as cursor:
        if tipo_seleccionado:
            cursor.execute("""
                SELECT id_nombre_tipo
                FROM tipos_personal
                WHERE id_nombre_tipo = %s
            """, [tipo_seleccionado])
        else:
            cursor.execute("SELECT id_nombre_tipo FROM tipos_personal ORDER BY id_nombre_tipo")
        
        return columnas, [[row[0]] for row in cursor.fetchall()]


def get_datos_asistencias(trabajador_id, desde='', hasta=''):
    """Obtiene datos de asistencias"""
    columnas = ['ID', 'Fecha', 'Hora Entrada', 'Hora Salida', 'Acceso', 'Estado', 'Trabajador']
    
    query = """
        SELECT b.id_pk, b.fecha, b.hora_acceso, b.hora_salida, b.acceso, b.estado_jornada,
               CONCAT(u.nombres, ' ', u.apellidos)
        FROM bitacora_asistencia b
        LEFT JOIN usuarios u ON b.id_usuario_fk = u.id_pk
        WHERE 1=1
    """
    params = []
    
    if trabajador_id:
        query += " AND b.id_usuario_fk = %s"
        params.append(trabajador_id)
    if desde:
        query += " AND b.fecha >= %s"
        params.append(desde)
    if hasta:
        query += " AND b.fecha <= %s"
        params.append(hasta)
    
    query += " ORDER BY b.fecha DESC, b.hora_acceso DESC LIMIT 500"
    
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultados = []
        for row in cursor.fetchall():
            resultados.append([
                row[0],
                row[1].strftime('%d/%m/%Y') if row[1] else '-',
                str(row[2]) if row[2] else '-',
                str(row[3]) if row[3] else '-',
                row[4] or '-',
                row[5] or '-',
                row[6] or '-',
            ])
        return columnas, resultados


def get_nombre_trabajador(trabajador_id):
    """Obtiene el nombre completo de un trabajador"""
    if not trabajador_id:
        return 'Todos'
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT cedula, nombres, apellidos
                FROM usuarios
                WHERE id_pk = %s
            """, [trabajador_id])
            row = cursor.fetchone()
            if row:
                return f"{row[0]} - {row[1]} {row[2]}"
    except:
        pass
    return 'Desconocido'


def crear_pdf(titulo, columnas, datos, nombre_seleccion):
    """Genera el PDF usando reportlab"""
    now = datetime.now()
    fecha = now.strftime('%d/%m/%Y')
    hora = now.strftime('%H:%M')
    fecha_archivo = now.strftime('%d-%m-%Y')
    
    # Crear response
    response = HttpResponse(content_type='application/pdf')
    filename = f"{titulo} - {fecha_archivo} - {nombre_seleccion}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    # Crear documento
    doc = SimpleDocTemplate(
        response, 
        pagesize=landscape(A4),
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        spaceAfter=20,
    )
    
    # Logo
    logo_path = os.path.join('static', 'images', 'identia_logo_no_backgound.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=1.5*inch, height=0.8*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 10))
        except:
            elements.append(Paragraph("IDENTIA", title_style))
    else:
        elements.append(Paragraph("IDENTIA", title_style))
    
    # Título
    elements.append(Paragraph(titulo, title_style))
    elements.append(Paragraph(f"Fecha: {fecha} | Hora: {hora}", subtitle_style))
    elements.append(Paragraph(f"Reporte de: {nombre_seleccion}", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Datos
    if not datos:
        elements.append(Paragraph("No hay datos para mostrar", styles['Normal']))
    else:
        table_data = [columnas]
        table_data.extend(datos)
        
        table = Table(table_data, repeatRows=1)
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 15))
        elements.append(Paragraph(f"Total de registros: {len(datos)}", styles['Normal']))
    
    doc.build(elements)
    return response
