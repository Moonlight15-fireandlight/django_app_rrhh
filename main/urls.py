from django.urls import path
from main import views

urlpatterns = [
    #path('login/', views.login, name='login'),
    path('registerpage/', views.registerpage, name='register'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('', views.home, name='home'),
    path('events/<event_id>', views.events, name='events'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('contratos/', views.contratos, name='contratos'),
    path('comisiones', views.comisiones, name='comisiones'),
    path('show_changes/', views.show_changes, name='show_changes'),
    path('update_event/<event_id>', views.update_event, name='update_event'),
    path('update_rrhh/<event_id>', views.update_rrhh, name='update_rrhh'),
    path('delete_event/<event_id>', views.delete_event, name='delete_event'),
    path('constancias', views.constancias, name='constancias'),
]
