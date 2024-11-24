from django.shortcuts import get_object_or_404, render, redirect
from services.fiscalizacion.FiscalizacionService import FiscalizacionService
from .forms import FiscalizacionForm
from .models import Fiscalizacion
from mediciones.models import Medicion
from django.contrib import messages
from django.db.models import RestrictedError

def crear_fiscalizacion(request):
    pass


def cargar_fiscalizacion(request):
    fiscalizaciones = Fiscalizacion.objects.all()
    
    return render(request, 'fiscalizacion/mantenedor_fiscalizacion.html', {'fiscalizaciones': fiscalizaciones})


def eliminar_fiscalizacion(request, fiscalizacion_id):
    """Vista para eliminar una fiscalización."""

    fiscalizacion = get_object_or_404(Fiscalizacion, id=fiscalizacion_id)

    if request.method == 'POST':
        try:
            FiscalizacionService.eliminar_fiscalizacion(fiscalizacion_id)
            messages.success(request, f'El registro {fiscalizacion.proyecto} se eliminó correctamente.')
            return redirect('') 
        except RestrictedError as e:
            messages.error(request, f'No se puede eliminar el registro: {e.args[0]}')

    return render(request, 'fiscalizacion/fiscalizacionDel.html', {'fiscalizacion': fiscalizacion})


def detalle_fiscalizacion(request, fiscalizacion_id):
    fiscalizacion = get_object_or_404(Fiscalizacion, id=fiscalizacion_id)
    
    return render(request, 'fiscalizacion/detalle_fiscalizacion.html', {'fiscalizacion': fiscalizacion})

