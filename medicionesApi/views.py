import json
from django.shortcuts import render
from django.http import JsonResponse
from fiscalizacion.models import Fiscalizacion
from mediciones.models import InstrumentoMedicion, Medicion, MedicionSensor, Sensor
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def cargar_instrumentos_medicion(request):
    instrumentos = InstrumentoMedicion.objects.all()
    data = {
        'instrumentos': list(
            instrumentos.values(
                'id', 'tipo', 'marca', 'modelo', 'num_serie'
            )
        )
    }
    return JsonResponse(data)


def cargar_mediciones(request):
    mediciones = Medicion.objects.all()
    data = {
        'mediciones': list(
            mediciones.values(
                'id', 'tipo', 'latitud', 'longitud', 'temperatura', 'humedad',
                'valor_medido', 'cumplimiento', 'observacion', 'foto', 
                'instrumento_medicion_id', 'fiscalizacion_id', 'creado'
            )
        )
    }
    return JsonResponse(data)

#Vista que carga la Api
def cargar_mediciones_completas(request):
    # Obtener datos básicos de instrumentos y mediciones
    instrumentos_data = {instrumento["id"]: instrumento for instrumento in json.loads(cargar_instrumentos_medicion(request).content)["instrumentos"]}
    mediciones_data = json.loads(cargar_mediciones(request).content)["mediciones"]

    # Construir la respuesta con relaciones anidadas
    for medicion in mediciones_data:
        medicion["instrumento_medicion"] = instrumentos_data.get(medicion["instrumento_medicion_id"], {})
        # Eliminar los IDs relacionados para evitar redundancia en la API


    return JsonResponse({"mediciones_completas": mediciones_data})


@csrf_exempt
def guardar_medicion(request):
    if request.method == "POST":
        try:
            # Obtener datos de la solicitud
            instrumento_medicion_id = request.POST.get("instrumento_medicion_id")
            fiscalizacion_id = request.POST.get("fiscalizacion_id")
            tipo = request.POST.get("tipo")
            latitud = request.POST.get("latitud")
            longitud = request.POST.get("longitud")
            temperatura = request.POST.get("temperatura")
            humedad = request.POST.get("humedad")
            valor_medido = request.POST.get("valor_medido")
            cumplimiento = request.POST.get("cumplimiento")
            observacion = request.POST.get("observacion")
            foto = request.FILES.get("foto")

            # Validar campos requeridos
            if not (instrumento_medicion_id and fiscalizacion_id and latitud and longitud and valor_medido):
                return JsonResponse({"error": "Faltan campos requeridos"}, status=400)

            # Verificar relaciones de claves foráneas
            try:
                instrumento_medicion = InstrumentoMedicion.objects.get(id=instrumento_medicion_id)
            except InstrumentoMedicion.DoesNotExist:
                return JsonResponse({"error": "Instrumento de medición no encontrado"}, status=404)

            try:
                fiscalizacion = Fiscalizacion.objects.get(id=fiscalizacion_id)
            except Fiscalizacion.DoesNotExist:
                return JsonResponse({"error": "Fiscalización no encontrada"}, status=404)

            # Crear instancia de Medición
            medicion = Medicion(
                tipo=tipo,
                latitud=latitud,
                longitud=longitud,
                temperatura=temperatura,
                humedad=humedad,
                valor_medido=valor_medido,
                cumplimiento=cumplimiento,
                observacion=observacion,
                instrumento_medicion=instrumento_medicion,
                fiscalizacion=fiscalizacion,
            )

            # Guardar foto si se proporciona
            if foto:
                medicion.foto.save(foto.name, foto, save=False)

            # Guardar medición en la base de datos
            medicion.save()

            return JsonResponse({
                "mensaje": "Medición guardada exitosamente",
                "medicion_id": medicion.id,
                "foto_url": medicion.foto.url if foto else None
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Error al guardar la medición: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)







@csrf_exempt
def guardar_medicion_sensor(request):
    if request.method == 'POST':
        try:
            # Decodificar datos JSON
            data = json.loads(request.body)

            # Extraer datos
            sensor_id = data.get('sensor_id')
            temperatura = data.get('temperatura')
            humedad = data.get('humedad')
            luminancia = data.get('luminancia')
            iluminancia = data.get('iluminancia')

            # Validar campos obligatorios
            if not (sensor_id and luminancia and iluminancia):
                return JsonResponse({'error': 'Faltan campos requeridos.'}, status=400)

            # Validar existencia del sensor
            try:
                sensor = Sensor.objects.get(id=sensor_id)
            except Sensor.DoesNotExist:
                return JsonResponse({'error': 'El sensor no existe.'}, status=404)

            # Crear medición
            MedicionSensor.objects.create(
                sensor=sensor,
                temperatura=temperatura,
                humedad=humedad,
                luminancia=luminancia,
                iluminancia=iluminancia,
            )

            return JsonResponse(
                {'mensaje': 'Medición registrada con éxito.'},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos, no es JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def cargar_mediciones_sensor(request):
    mediciones = MedicionSensor.objects.all()
    data = {
        'mediciones_sensor': list(
            mediciones.values(
                'id', 'temperatura', 'humedad', 'luminancia', 'iluminancia', 'creado', 'sensor_id'
            )
        )
    }
    return JsonResponse(data)



def cargar_mediciones(request, proyecto_id):
    # Obtener todas las fiscalizaciones relacionadas con el proyecto
    fiscalizaciones = Fiscalizacion.objects.filter(proyecto_id=proyecto_id).values_list('id', flat=True)
    
    # Obtener todas las mediciones relacionadas con esas fiscalizaciones
    mediciones = Medicion.objects.filter(fiscalizacion_id__in=fiscalizaciones)

    # Preparar la respuesta
    data = {
        'mediciones': list(
            mediciones.values(
                'id', 
                'tipo', 
                'latitud', 
                'longitud', 
                'temperatura', 
                'humedad', 
                'valor_medido', 
                'cumplimiento', 
                'observacion', 
                'foto', 
                'instrumento_medicion_id', 
                'fiscalizacion_id', 
                'creado'
            )
        )
    }
    return JsonResponse(data)



def cargar_medicion_por_id(request, medicion_id):
    try:
        # Buscar la medición específica por ID
        medicion = Medicion.objects.get(id=medicion_id)

        # Preparar la respuesta con los datos de la medición
        data = {
            'medicion': {
                'id': medicion.id,
                'tipo': medicion.tipo,
                'latitud': medicion.latitud,
                'longitud': medicion.longitud,
                'temperatura': medicion.temperatura,
                'humedad': medicion.humedad,
                'valor_medido': medicion.valor_medido,
                'cumplimiento': medicion.cumplimiento,
                'observacion': medicion.observacion,
                'foto': medicion.foto.url if medicion.foto else None,
                'instrumento_medicion_id': medicion.instrumento_medicion_id,
                'fiscalizacion_id': medicion.fiscalizacion_id,
                'creado': medicion.creado.strftime('%Y-%m-%d %H:%M:%S'),
            }
        }
        return JsonResponse(data)
    except Medicion.DoesNotExist:
        # Responder con un error si no se encuentra la medición
        return JsonResponse({'error': 'Medición no encontrada'}, status=404)

