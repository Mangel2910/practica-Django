from django.shortcuts import render
from .models import Personal, Usuario
from .serializers import PersonalSerializer, HabilidadSerializer
from rest_framework import generics

# Create your views here.

class PersonalViewSet(generics.ListCreateAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer


#Usando (Filter) para buscar algo
from rest_framework.generics import ListAPIView
#Primera Forma
class PersonalListsEscritor(ListAPIView):
    queryset = Personal.objects.filter(
        Habilidades__habilidad = 'Escritor'  # Filtra para mostrar solo los que tienen habilidades
    )
    serializer_class = PersonalSerializer


#Segunda Forma Funsion (get_queryset)
class PersonalListsIngeniero(ListAPIView):
    serializer_class = PersonalSerializer
    def get_queryset(self):
        lista = Personal.objects.filter(
            Habilidades__habilidad = 'Ingeniero'  # Filtra para mostrar solo los que tienen habilidades
        )
        return lista #Para esta funsion siempre debemos rotornar un valor
    

#Tercera forma (Usando Rutas)
class PersonalListRutas(ListAPIView):
    serializer_class = PersonalSerializer
    def get_queryset(self):
        habilidad = self.kwargs['habilidad']
        lista = Personal.objects.filter(
            Habilidades__habilidad = habilidad  # Filtra para mostrar solo los que tienen habilidades
        )
        return lista #No olvides el return
        

#Lista por plabra clave

# Para esta clase deberiamos usar los templates que nos dara mejor vusalizacion en una pagina real donde lo hacemos con un buscador que al buscarlo nos dara el objeto que se esta buscando


# Si lo queremos usar con un campo que tiene (ManyToManyField) o (Foreingkey), debemos llamar al campo primero en: context_object_name y en donde se vera la lista y por ultimo debemos colocar el (palabra_clave) el id que queremos que muestre
class ListaPresonalByKword(ListAPIView):
    serializer_class = PersonalSerializer
    context_object_name = 'Nombre' #Aqui estamos llamando al campo del modulo Personal que deseemos 
    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", 'Camilo') #Aqui le decimos que de la ruta de (kword) busque el objeto que estamos solicitando, en este caso es el nombre que dijiste el usuario.
        lista = Personal.objects.filter(
            Nombre=palabra_clave #Aqui es donde se creara la lista que se encuentre con dichop objeto recibido por el usuario que se almaceno en palabra_clave
        )
        return lista

    

#Lista de personas por habilidad
class ListPeronalHabilidad(ListAPIView):
    serializer_class = HabilidadSerializer #LLamamos al serializer de habilidades que es el que queremos usar
    context_object_name = 'habilidad' #Llmamos al campo de ese serializador de Habilidades
    def get_queryset(self):
        personal = Personal.objects.get(id=1) #Asignamos todo a la variable de personas y que de ese mismo use el get() para optener el valor por id
        return personal.Habilidades.all() #Aqui se devuelve la variable que usamos y el campo de la tabla Personal y que llame a todos los relacionados


#Usando DetailView
# se utiliza para mostrar los detalles de un objeto específico
#Es ideal para mostrar la información detallada de un único elemento, como los detalles de un producto, un perfil de usuario o una entrada de blog

#Con el no es necesario colocar el (context_object_name) ya que el lo hace todo

#Usando este Es necesario usar los templates de html

#Con esta parametro es necesario que en la url se se use (<int:pk>)

from django.views.generic import DetailView

class PersonalDetailView(DetailView):
    model = Personal
    template_name = "Detailview/detail_personal.html"
    #Para activar los templates debemos crear un forlder fuera del proyecto llamado (templates) y ahi dentro creamos los html que vamos a usar, ademas debemos entrar al settings y colocar el (BASE_DIR) dentro de los TEMPLATES y en DIRS colocamos: 'DIRS': [BASE_DIR / 'templates'],


    #Esta funcion nos ayuda a enviar una variable extra hacie los templates que no se encuentre en algun modelo, puede ser usado para tutulos o diferentes variables
    def get_context_data(self, **kwargs):
        context = super(PersonalDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Empleado del mes'
        return context
    
    

#Esto nos ayudara a buscar un template normal y con ello poder usarla para que no dirija al html 
from django.views.generic import TemplateView

class SuccesView(TemplateView):
    template_name = "Succes/succesPersonal.html"




#Usando CreateView = CreateAPIView
#Genera la tabla para poder dijitar datos por el usuario
#Es bueno usarlo con los templates, para mejor visualizacion al usarlo debemos usar dentro del template los que es form = {{form}}
# Para poder usarlo debemos importarlo asi: from django.views.generic.edit import CreateView

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class PersonalCreateView(CreateView):
    template_name = "CreateApiView/form.html"
    model = Personal
    fields = ('__all__')
    success_url = reverse_lazy('Peronal_app:Pagina_Entrada')

    #Cuando usamos el (reverse_lazy) debemos colocar en parentesis a donde queremos que acceda, llamamos al (app_name de las urls) y despues de los dos puntos (:) colocamos el nombre que fue asignada la url (name='') 

    #Es el que redirecciona cuando el form ya esta echo, podemos dejarlo ('.') que envia a la misma pagina o llevandonos a otra nuevas. ( success_url = '.'  )

    #Para que nos lleve a otra pagina debemos colocar la url que le asignamos en URL del templateView ( success_url = '/succes' )

#Permite personalizar qué sucede después de que el formulario es válido y antes de guardar (o justo después de guardar) el objeto en la base de datos.
    def form_valid(self, form):
        personal = form.save()
        personal.save()
        return super(PersonalCreateView, self).form_valid(form)





# Usando UpdateView
from django.views.generic import UpdateView

class ActualizarView(TemplateView):
    template_name = 'Update/GuardarDatosNuevos.html'

class PersonaUptadeView(UpdateView):
    model = Personal
    fields = '__all__'
    template_name = 'Update/Acualizar.html'
    success_url = reverse_lazy('Peronal_app:Actualizar')

    

#Usando DeleteView
from django.views.generic import DeleteView

class PersonalDelete(TemplateView):
    template_name = 'Delete/ConfirlDelete.html'

class PersonalDeleteView(DeleteView):
    model = Personal
    template_name = 'Delete/DeletePersonal.html'
    success_url = reverse_lazy('Peronal_app:confirm_delete')
    



#Usando un formulario

# Llamamos a la clase del archivo form
from .form import FormPruebaView

# Creamso el template que se usara despues de registrarse
class PersonalWelcome(TemplateView):
    template_name = 'Formulario/Inicio.html'

# cramos la clase del formulario 
class FormPersonalView(CreateView):
    template_name = 'Formulario/form.html'
    model = Usuario
    # Podemos cambiar (fields), ya que esta se encuentra en la clase del archivo form.py.
    form_class = FormPruebaView
    success_url = reverse_lazy('Peronal_app:qr_codigo')

    




#Creacion de QR
from django.shortcuts import render
from .models import Usuario

def home_view(request):
    obj = Usuario.objects.all()
    return render(request, 'QR/qrWelcome.html', {'obj': obj})