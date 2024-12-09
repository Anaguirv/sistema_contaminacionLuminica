from django.urls import path
from . import views as v


urlpatterns = [

    path('Api_mediciones', v.cargar_mediciones_completas, name='Api_mediciones'),
    path('Api_instrumentos_medicion', v.cargar_instrumentos_medicion, name='cargar_instrumentos_medicion'),
    path('Guardar_medicion', v.guardar_medicion, name='guardar_medicion'),
    path('Cargar_mediciones/<int:proyecto_id>/', v.cargar_mediciones, name='cargar_mediciones'),
    path('Cargar_medicion_por_id/<int:medicion_id>/', v.cargar_medicion_por_id, name='cargar_medicion_por_id'),

    path('Guardar_medicion_sensor', v.guardar_medicion_sensor, name='guardar_medicion_sensor'),
    path('Cargar_mediciones_sensor', v.cargar_mediciones_sensor, name='cargar_mediciones_sensor'),


]



