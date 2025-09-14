# Importamos el forms que viene de django
from django import forms

# Importamos el modelo Personal
from .models import Personal, Usuario


# Creamos la clase del formulario usando como parametros form y modelForm
class FormUsuarioView(forms.ModelForm):
    #Creamos una clase meta
    class Meta:
        model = Usuario
        # Llamamos al los campos que queremos visualizar
        fields = (
            'Nombre',
            'Apellido',
            'NumeroDoc',
            'Correo',
        )

        # Aqui podemos agregarles estilos a los inputs cuando usamos el ({{ form }}) en el html
        widgets = {
            # Nombramoa el campo al cual queremos que haga el diseño y llamamos su etiqueta
            'Nombre': forms.TextInput(
                # (attrs) significa atribitos 
                attrs= {
                    # El diseño que vamos a colocar y el mensaje
                    'placeholder': 'Ingrese su nombre'
                }
            ),
            'Apellido': forms.TextInput(
                attrs={
                    'placeholder': 'Dijita tu apellido'
                }
            ),
            'Correo': forms.TextInput(
                attrs= {
                    'placeholder': 'Dijite un correo valido'
                }
            ),
            'NumeroDoc': forms.TextInput(
                attrs={
                    'placeholder': 'Dijita tu numero de identidad'
                }
            )
        }



class FormPersonalView(forms.ModelForm):
    class Meta:
        model = Personal
        fields = (
            'Nombre',
            'numeroDoc',
            'Contraseña',
            'Habilidades',
        )
        widgets = {
            'Nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre'
                }
            ),
            'numeroDoc': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su numero de documento'
                }
            ),
            'Contraseña': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su contraseñas'
                }
            )
        }



        # ¡¡Ahora vamos al views!!