from .auth import sign_in, sign_out, step_two, register,login
from django.urls import path


urlpatterns =[
    path('auth/up/',sign_in, name="sign_in"),
    path('auth/out/', sign_out, name='logout'),
    path('auth/two/',step_two,name='step_two'),
    path('regis/',register,name='register'),

]