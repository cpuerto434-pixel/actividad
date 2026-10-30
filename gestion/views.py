# LIBRERIAS
import json

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Project


# FUNCIONES AUXILIARES
def serializar(proyecto):
    """Convierte un objeto Project en un diccionario listo para JSON."""
    return {
        'id': proyecto.id,
        'name': proyecto.name,
        'description': proyecto.description,
        'start_date': proyecto.start_date.isoformat(),
    }


def leer_datos(request):
    """
    Lee y valida el cuerpo JSON de la peticion.
    Devuelve (datos, error): si hay error, datos es None.
    """
    try:
        cuerpo = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, 'El cuerpo de la peticion no es un JSON valido'

    if not isinstance(cuerpo, dict):
        return None, 'El JSON debe ser un objeto con los campos del proyecto'

    faltantes = [c for c in ('name', 'description', 'start_date') if not cuerpo.get(c)]
    if faltantes:
        return None, 'Faltan campos obligatorios: ' + ', '.join(faltantes)

    try:
        fecha = parse_date(cuerpo['start_date'])
    except (ValueError, TypeError):
        fecha = None
    if fecha is None:
        return None, 'start_date debe tener el formato AAAA-MM-DD'

    return {
        'name': cuerpo['name'],
        'description': cuerpo['description'],
        'start_date': fecha,
    }, None


# VISTA
# csrf_exempt sobre dispatch: permite POST, PUT y DELETE sin token CSRF
# (necesario para probar el endpoint con Postman, curl, etc.)
@method_decorator(csrf_exempt, name='dispatch')
class ProyectoView(View):

    # GET -> READ (leer): lista todos, o uno solo si llega pk
    def get(self, request, pk=None):
        if pk is None:
            proyectos = [serializar(p) for p in Project.objects.all()]
            return JsonResponse({'proyectos': proyectos})

        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)
        return JsonResponse(serializar(proyecto))

    # POST -> CREATE (crear)
    def post(self, request, pk=None):
        if pk is not None:
            return JsonResponse({'error': 'POST se usa en /proyectos/, sin id'}, status=405)

        datos, error = leer_datos(request)
        if error:
            return JsonResponse({'error': error}, status=400)

        proyecto = Project.objects.create(**datos)
        return JsonResponse(serializar(proyecto), status=201)

    # PUT -> UPDATE (actualizar): reemplaza todos los campos del proyecto
    def put(self, request, pk=None):
        if pk is None:
            return JsonResponse({'error': 'Debes indicar el id: /proyectos/<id>/'}, status=400)

        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)

        datos, error = leer_datos(request)
        if error:
            return JsonResponse({'error': error}, status=400)

        proyecto.name = datos['name']
        proyecto.description = datos['description']
        proyecto.start_date = datos['start_date']
        proyecto.save()
        return JsonResponse(serializar(proyecto))

    # DELETE -> DELETE (eliminar)
    def delete(self, request, pk=None):
        if pk is None:
            return JsonResponse({'error': 'Debes indicar el id: /proyectos/<id>/'}, status=400)

        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)

        proyecto.delete()
        return JsonResponse({'mensaje': 'Proyecto eliminado correctamente'})
