from django.db import models
from django.utils import timezone
from .choices import cumplimiento, tipo_instrumento, tipo_medicion
from fiscalizacion.models import Fiscalizacion
from services.utils.GenerarNombre import GenerarNombre


class InstrumentoMedicion(models.Model):
    tipo = models.CharField(max_length=1, choices=tipo_instrumento, verbose_name='Iipo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    num_serie = models.CharField(max_length=50, verbose_name='N° de Serie')
    
    def __str__(self):
        return "{}".format(self.get_tipo_display())
        
    class Meta:
        db_table = 'instrumentoMedicion'
        verbose_name = 'Instrumento de medición'
        verbose_name_plural = 'Instrumentos de medición'


class Medicion(models.Model):
    tipo = models.CharField(max_length=1, choices=tipo_medicion, verbose_name='Tipo')
    latitud = models.FloatField(verbose_name='Latitud')
    longitud = models.FloatField(verbose_name='Longitud')
    temperatura = models.FloatField(blank=True, null=True, verbose_name='Temperatura (°C)')
    humedad = models.FloatField(blank=True, null=True, verbose_name='Humedad (%)')
    valor_medido = models.FloatField(verbose_name='Valor medido')
    cumplimiento = models.CharField(max_length=1, choices=cumplimiento, blank=True, null=True, verbose_name='Cumplimiento')
    observacion = models.CharField(max_length=500, verbose_name='Observación')
    foto = models.ImageField(upload_to=GenerarNombre.generar_nombre_medicion, null=True, default='medicion/medicion.png')
    #FK
    instrumento_medicion = models.ForeignKey(InstrumentoMedicion, null=False, on_delete=models.RESTRICT)
    fiscalizacion = models.ForeignKey(Fiscalizacion, null=False, on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now, editable=False)  
    
    def __str__(self):
        return "{} {}".format(self.tipo, self.valor_medido)
        
    class Meta:
        db_table = 'medicion'
        verbose_name = 'Medición'
        verbose_name_plural = 'Mediciones'



class Sensor(models.Model):
    latitud = models.FloatField(verbose_name='Latitud')               # Latitud del sensor
    longitud = models.FloatField(verbose_name='Longitud')              # Longitud del sensor
    creado = models.DateTimeField(default=timezone.now, editable=False)  # Fecha y hora de creación

    def __str__(self):
        return f"Sensor {self.id} registrado en ({self.latitud}, {self.longitud})"
    



class MedicionSensor(models.Model):
    temperatura = models.FloatField(blank=True, null=True, verbose_name='Temperatura (°C)')
    humedad = models.FloatField(blank=True, null=True, verbose_name='Humedad (%)')
    luminancia = models.FloatField(verbose_name='Valor Luminancia')  # Luminancia, requerido
    iluminancia = models.FloatField(verbose_name='Valor Iluminancia')  # Iluminancia, requerido
    creado = models.DateTimeField(default=timezone.now, editable=False)  
    sensor = models.ForeignKey(
        'Sensor', on_delete=models.CASCADE, related_name='mediciones'
    )  # Relación con el modelo Sensor

    class Meta:
        db_table = 'medicionsensor'  # Nombre de la tabla en la base de datos
        verbose_name = 'Medición de Sensor'
        verbose_name_plural = 'Mediciones de Sensores'

    def __str__(self):
        return f"Medición {self.id} del sensor {self.sensor.id} registrada el {self.creado}"

