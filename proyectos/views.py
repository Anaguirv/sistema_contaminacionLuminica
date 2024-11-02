from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto
from .forms import ProyectoForm


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/proyectos/')
    else:
        form = ProyectoForm()

    # retornamos el formulario
    return render(request, 'proyectos/proyectoAdd.html', {'form':form})


def cargar_proyecto(request):
    proyectos = Proyecto.objects.all()
    
    data = {
        'proyectos': proyectos
    }
    return render(request, 'proyectos/mantenedor_proyectos.html', data)


def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        proyecto.delete()
        return redirect('/proyectos/')

    return render(request, 'proyectos/proyectoDel.html', {'proyecto': proyecto} )


def cargar_editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    form = ProyectoForm(instance=proyecto)
    
    return render(request, 'proyectos/proyectoEdit.html', {'form':form, 'proyecto':proyecto})


def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('/proyectos/')
    else:
        form = ProyectoForm(instance=proyecto)
    
    return render(request, 'proyectos/mantenedor_proyectos.html', {'form':form})