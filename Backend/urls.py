from django.urls import path, include

from . import views
app_name = "Personal_app" #Es el nombre asignado para todos los demas urls, lo usamos para especificar a que url queremos acceder.
urlpatterns = [
    path('personal/', views.PersonalViewSet.as_view()),  # Para crear y listar Personal

    #Usando Filtro de busqueda
    path('personal-Escritor/', views.PersonalListsEscritor.as_view()),

    #Usando filtro con funsion
    path('personal-Ingeniero/', views.PersonalListsIngeniero.as_view()),

    #Usando filtro con rutas
    path('personal/<habilidad>/', views.PersonalListRutas.as_view()),

    #Buscar usuario por palabra clave
    path('kword/', views.ListaPresonalByKword.as_view()),

    #Listar Personal por abilidad
    path('Habilidad/', views.ListPeronalHabilidad.as_view()),

    #Liosta de Personal con DetailView
    path('detailView/<int:pk>/', views.PersonalDetailView.as_view()),

    #Usando CreateApiView
    path('createApiview/', views.PersonalCreateView.as_view()),

    #Usando TemplateView
    path('succes/', views.SuccesView.as_view(), name='Pagina_Entrada'),
    # Template Actualizar
    path('actualizar_Personal/', views.ActualizarView.as_view(), name='Actualizar'),

    #Usando UpdateView
    path('update/<int:pk>/', views.PersonaUptadeView.as_view(), name='actualizar_personal'),

    #Usando DeleteView
    path('eliminar/<int:pk>/', views.PersonalDeleteView.as_view(), name='eliminar'),
    path('confirm_delete/', views.PersonalDelete.as_view(), name='confirm_delete'),

    #Formulario_QR
    path('form_qr/', views.FormUsuarioView.as_view(), name='Form'),
    #QR
    path('qr_code/', views.home_view, name="qr_codigo"),

    #Formulario Peronal
    path('form_personal/', views.FormPersonalView.as_view(), name='form_perso'),
    #Welcome Personal
    path('personal_inicio/', views.personal_welcome, name='personal_inicio')
]