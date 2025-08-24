from django.contrib import admin
from .models import Personal, Habilidades, Usuario
# Register your models here.

admin.site.register(Habilidades)
admin.site.register(Usuario)


class PresonalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Nombre',
        'numeroDoc',
        'Contraseña',
    )
    search_fields = ('Nombre',)  # Permite buscar por Nombre o como deseemos
    list_filter = ('Nombre', 'Habilidades')  # Permite filtrar por Nombre


    filter_horizontal = ('Habilidades',)  # Permite seleccionar varias habilidades a la vez, es un campo de muchos a muchos

admin.site.register(Personal , PresonalAdmin)