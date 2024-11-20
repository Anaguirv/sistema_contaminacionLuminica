from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import RestrictedError
from .forms import FiscalizacionForm
from .models import Fiscalizacion
from proyectos.models import Proyecto
from mediciones.models import Medicion
from services.fiscalizacion.fiscalizacion_service import FiscalizacionService
from services.fiscalizacion.mapa_service import MapaService
from mediciones.forms import MedicionForm

def cargar_fiscalizacion(request):
    """Vista para cargar fiscalizaciones con mediciones y renderizar el mapa."""
    
    fiscalizaciones_con_mediciones, todas_las_mediciones = FiscalizacionService.obtener_fiscalizaciones_con_mediciones()

    mapa = MapaService.crear_mapa()
    MapaService.agregar_areas_rectangulares(mapa, Proyecto.objects.all())
    MapaService.agregar_marcadores_mediciones(mapa, todas_las_mediciones)

    map_html = mapa._repr_html_()
    form = FiscalizacionForm()

    return render(request, 'fiscalizacion/mantenedor_fiscalizacion.html', {
        'fiscalizaciones_con_mediciones': fiscalizaciones_con_mediciones,
        'map': map_html,
        'form': form,
    })


def crear_fiscalizacion(request):
    """Vista para crear una nueva fiscalización."""

    if request.method == 'POST':
        form = FiscalizacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto ingresado exitosamente a fiscalizaciones.')
            return redirect('')  
        else:
            messages.error(request, 'Hubo un error al crear la fiscalización. Revisa los datos ingresados.')

    form = FiscalizacionForm()
    return render(request, 'fiscalizacion/crear_fiscalizacion.html', {'form': form})


def detalle_fiscalizacion(request, proyecto_id):
    """Vista para mostrar el detalle de una fiscalización asociada a un proyecto."""

    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    mediciones = Medicion.objects.filter(fiscalizacion__proyecto=proyecto).select_related('fiscalizacion__usuario')

    return render(request, 'fiscalizacion/detalle_fiscalizacion.html', {
        'proyecto': proyecto,
        'mediciones': mediciones,
    })


def eliminar_fiscalizacion(request, fiscalizacion_id):
    """Vista para eliminar una fiscalización."""

    fiscalizacion = get_object_or_404(Fiscalizacion, id=fiscalizacion_id)

    if request.method == 'POST':
        try:
            fiscalizacion.delete()
            messages.success(request, f'El registro {fiscalizacion.proyecto} se eliminó correctamente.')
            return redirect('') 
        except RestrictedError as e:
            messages.error(request, f'No se puede eliminar el registro: {e.args[0]}')

    return render(request, 'fiscalizacion/fiscalizacionDel.html', {'fiscalizacion': fiscalizacion})


def nueva_medicion(request, fiscalizacion_id):
    """Vista para ingresar una nueva medición en un proyecto fiscalizado."""

    fiscalizacion = get_object_or_404(Fiscalizacion, id=fiscalizacion_id)
    current_url = request.META.get('HTTP_REFERER', '/')  # Captura la URL actual o usa '/' como predeterminado

    if request.method == "POST":
        form = MedicionForm(request.POST, request.FILES)
        if form.is_valid():
            medicion = form.save(commit=False)
            medicion.fiscalizacion = fiscalizacion
            medicion.save()
            messages.success(request, 'Medición Ingresada. Presiona "Volver" para salir o sigue ingresando mediciones')
            
            return HttpResponseRedirect(current_url)  # Redirige a la misma página
    else:
        form = MedicionForm()

    return render(request, 'mediciones/medicionAdd.html', {
        'fiscalizacion': fiscalizacion,
        'form': form
    })


def eliminar_medicion(request, medicion_id):
    """Vista para eliminar una medición."""
    
    medicion = get_object_or_404(Medicion, id=medicion_id)

    if request.method == 'POST':
        try:
            datosDel = {
                'id': medicion.id
            }
            fiscalizacion_id = medicion.fiscalizacion.id  # Obtiene el ID de la fiscalización

            medicion.delete()
            messages.success(request, f'La medición {datosDel["id"]} se eliminó correctamente.')
            #return redirect(f'fiscalizacion/{fiscalizacion_id}/detalle/')
            return redirect('')

        except RestrictedError as e:
            messages.error(request, f'No se puede eliminar la medición: {e.args[0]}')
        except Exception as e:
            messages.error(request, f'Error al eliminar la medición: {str(e)}')

    return render(request, 'mediciones/medicionDel.html', {'medicion': medicion})