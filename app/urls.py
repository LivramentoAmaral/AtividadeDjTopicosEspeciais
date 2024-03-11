
from django.contrib import admin
from django.urls import path
from app.views import MapView  # Importe a visualização MapView



urlpatterns = [

    # Include the urls from the app

    path('', MapView.as_view(), name='index'),  # Corrija a configuração da URL para usar MapView.as_view()

    # path('draw',views.Drawpage, name='draw'),  

    # path('cerrado',views.Mapa_cerrado, name='cerrado'),  



]