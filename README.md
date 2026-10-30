# Taller: Peticiones en Django nativo

**Curso:** Desarrollo de aplicaciones Web I - 4E
**Docente:** Jose Javier Torres Vanstrahlen

Investigación sobre cómo crear endpoints en Django nativo (sin librerías externas como Django REST Framework) usando una vista basada en clase con los métodos `get()`, `post()`, `put()` y `delete()`.

## Archivos modificados

| Archivo | Qué se hizo |
|---|---|
| `gestion/views.py` | Se creó la vista `ProyectoView` (clase) con los 4 verbos HTTP |
| `gestion/urls.py` | Archivo nuevo con las rutas de la app |
| `proyecto/urls.py` | Se agregó `include('gestion.urls')` |

Modelo usado: `Project` (`name`, `description`, `start_date`) de la app `gestion`.

## Verbos HTTP y operaciones CRUD

| Verbo | Método de la vista | CRUD | Caso de uso | Ruta | Respuesta |
|---|---|---|---|---|---|
| GET | `get()` | Read | Consultar la lista o un proyecto | `/gestion/proyectos/` y `/gestion/proyectos/<id>/` | 200, o 404 si no existe |
| POST | `post()` | Create | Crear un proyecto nuevo | `/gestion/proyectos/` | 201, o 400 si los datos son inválidos |
| PUT | `put()` | Update | Reemplazar los datos de un proyecto | `/gestion/proyectos/<id>/` | 200, 400 o 404 |
| DELETE | `delete()` | Delete | Eliminar un proyecto | `/gestion/proyectos/<id>/` | 200, o 404 si no existe |

Cualquier otro verbo (por ejemplo PATCH) recibe automáticamente **405 Method Not Allowed**.

## Módulos, funciones y decoradores usados

### Módulos y clases

| Elemento | Descripción |
|---|---|
| `django.views.View` | Clase base de las vistas basadas en clase. Su método `dispatch()` revisa el verbo de la petición y llama al método con ese nombre (`get`, `post`, `put`, `delete`). Si el verbo no está definido, responde 405. |
| `django.http.JsonResponse` | Subclase de `HttpResponse` que convierte un diccionario a JSON y pone el `Content-Type: application/json`. Acepta `status=` para el código HTTP. |
| `django.urls.path` | Asocia un patrón de URL con una vista. Con `<int:pk>` captura un entero y lo entrega a la vista como argumento `pk`. |
| `django.urls.include` | Incluye el `urls.py` de una app dentro del `urls.py` principal del proyecto. |
| `django.utils.dateparse.parse_date` | Convierte un texto `AAAA-MM-DD` en un objeto `date`; devuelve `None` si no tiene el formato correcto. |
| `json` (librería estándar de Python) | `json.loads()` convierte el cuerpo de la petición (JSON) en un diccionario de Python. |
| `gestion.models.Project` | Modelo del ORM de Django usado para consultar, crear, modificar y borrar registros. |

### Funciones y métodos

| Elemento | Descripción |
|---|---|
| `ProyectoView.as_view()` | Método de clase que convierte la clase en una función que Django puede usar en `urls.py`. |
| `request.body` | Contenido crudo (bytes) de la petición; se usa en POST y PUT para leer el JSON enviado. |
| `Project.objects.all()` | Devuelve todos los registros (GET lista). |
| `Project.objects.get(pk=...)` | Devuelve un registro; lanza `Project.DoesNotExist` si no existe (se responde 404). |
| `Project.objects.create(...)` | Crea y guarda un registro (POST). |
| `proyecto.save()` | Guarda los cambios de un registro existente (PUT). |
| `proyecto.delete()` | Elimina el registro (DELETE). |
| `serializar()` y `leer_datos()` | Funciones auxiliares propias: la primera pasa un `Project` a diccionario; la segunda lee y valida el JSON recibido. |

### Decoradores

| Elemento | Descripción |
|---|---|
| `@csrf_exempt` (`django.views.decorators.csrf`) | Desactiva la verificación del token CSRF en la vista. Sin esto, POST, PUT y DELETE enviados desde Postman o curl serían rechazados con 403. En un proyecto real con sesiones se debería proteger de otra forma. |
| `@method_decorator(csrf_exempt, name='dispatch')` (`django.utils.decorators`) | Los decoradores de funciones no se pueden poner directo sobre una clase. `method_decorator` adapta el decorador para aplicarlo al método `dispatch` de la clase, que es el que recibe todas las peticiones. |

## Cómo probar

```bash
python manage.py runserver
```

```bash
# GET (lista y uno)
curl http://127.0.0.1:8000/gestion/proyectos/
curl http://127.0.0.1:8000/gestion/proyectos/1/

# POST (crear)
curl -X POST http://127.0.0.1:8000/gestion/proyectos/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Proyecto 1", "description": "Primera prueba", "start_date": "2026-10-29"}'

# PUT (actualizar)
curl -X PUT http://127.0.0.1:8000/gestion/proyectos/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Proyecto 1 editado", "description": "Cambiado", "start_date": "2026-11-01"}'

# DELETE (eliminar)
curl -X DELETE http://127.0.0.1:8000/gestion/proyectos/1/
```

## Fuentes consultadas

- Django: Introduction to class-based views. https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/
- Django: Base views (`View`, `dispatch`, `http_method_names`, `http_method_not_allowed`). https://docs.djangoproject.com/en/stable/ref/class-based-views/base/
- Django: Request and response objects (`JsonResponse`, `request.body`). https://docs.djangoproject.com/en/stable/ref/request-response/
- Django: URL dispatcher (`path`, `include`, conversores de ruta). https://docs.djangoproject.com/en/stable/topics/http/urls/
- Django: Cross Site Request Forgery protection (`csrf_exempt`). https://docs.djangoproject.com/en/stable/ref/csrf/
- Django: Decorating the class (`method_decorator`). https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/#decorating-the-class
- Django: Making queries (`get`, `create`, `save`, `delete`). https://docs.djangoproject.com/en/stable/topics/db/queries/
- MDN: Métodos de petición HTTP. https://developer.mozilla.org/es/docs/Web/HTTP/Methods
