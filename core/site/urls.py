from .main import index
from django.urls import path



urlpatterns = [
    path('',index,name='home')
]