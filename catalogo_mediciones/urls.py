from django.urls import path
from . import views as v

urlpatterns = [

    path('', v.catalogo_mediciones, name='catalogo'),

]