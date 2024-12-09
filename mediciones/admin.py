from django.contrib import admin
from .models import InstrumentoMedicion, Medicion, Sensor, MedicionSensor

# Register your models here.
class InstrumentoMedicionAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'marca', 'modelo', 'num_serie']


class MedicionAdmin(admin.ModelAdmin):
    list_display = ['id','tipo', 'fiscalizacion', 'latitud', 'longitud',  'temperatura', 'humedad', 'valor_medido', 'cumplimiento', 'observacion', 'instrumento_medicion', 'creado']


class SensorAdmin(admin.ModelAdmin):
    list_display = ['id','valor','fecha','hora']

class MedicionSensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'sensor', 'temperatura', 'humedad', 'luminancia', 'iluminancia']


# Configuración para Sensor
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'latitud', 'longitud']


admin.site.register(InstrumentoMedicion, InstrumentoMedicionAdmin)
admin.site.register(Medicion, MedicionAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(MedicionSensor, MedicionSensorAdmin)
