from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Aplicacion de Usuarios funcionando correctamente")