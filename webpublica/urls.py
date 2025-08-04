from django.urls import path
from . import views
from webpublica.views import landing_view, inicio_view

app_name = 'webpublica'

urlpatterns = [
    
    path('landing',landing_view, name='landing'),
    path('',inicio_view, name='inicio'),


]