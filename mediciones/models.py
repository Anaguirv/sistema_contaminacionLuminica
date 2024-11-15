from django.db import models
from django.utils import timezone
from .choices import cumplimiento, tipo_instrumento, tipo_medicion
from fiscalizacion.models import Fiscalizacion

class InstrumentoMedicion(models.Model):
    tipo = models.CharField(max_length=1, choices=tipo_instrumento, verbose_name='Iipo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    num_serie = models.CharField(max_length=50, verbose_name='N° de Serie')
    
    def __str__(self):
        return "{}".format(self.get_tipo_display())
        
    class Meta:
        db_table = 'instrumento_medicion'
        verbose_name = 'Instrumento de medición'
        verbose_name_plural = 'Instrumentos de medición'


class Medicion(models.Model):
    tipo = models.CharField(max_length=1, choices=tipo_medicion, verbose_name='Iipo')
    latitud = models.FloatField(verbose_name='Latitud')
    longitud = models.FloatField(verbose_name='Longitud')
    valor_medido = models.FloatField(verbose_name='Valor medido')
    cumplimiento = models.CharField(max_length=1, choices=cumplimiento, blank=True, null=True, verbose_name='Cumplimiento')
    observacion = models.CharField(max_length=500, verbose_name='Observación')
    #FK
    instrumento_medicion = models.ForeignKey(InstrumentoMedicion, null=False, on_delete=models.RESTRICT)
    fiscalizacion = models.ForeignKey(Fiscalizacion, null=False, on_delete=models.RESTRICT)
    creado = models.DateTimeField(default=timezone.now, editable=False)  
    
    def __str__(self):
        return "{} {}".format(self.tipo, self.valor_medido)
        
    class Meta:
        db_table = 'medicion'
        verbose_name = 'Medición'
        verbose_name_plural = 'Mediciones'

