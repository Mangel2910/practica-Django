from .models import Personal, Habilidades, Usuario
from rest_framework import serializers

class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ['id', 'Nombre', 'numeroDoc', 'Contraseña', 'Habilidades']


class HabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidades
        fields = ['id', 'habilidad']



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('__all__')