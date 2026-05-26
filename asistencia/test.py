def test_registro(request):
    from datetime import date, time
    uid = 42917365  # Reemplaza con un ID real
    fecha = date.today()
    hora = time(10, 30)
    rid = registrar_acceso(uid, fecha, hora, 'salida')
    return JsonResponse({'result': rid})