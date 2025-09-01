import os
from django.db import models

# Para hacer un QR
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import ImageDraw, Image, ImageEnhance, ImageOps

# Create your models here.

class Personal(models.Model):
    Nombre = models.CharField(max_length=100)
    numeroDoc = models.CharField(max_length=20)
    Contraseña = models.CharField(max_length=100)
    Habilidades = models.ManyToManyField('Habilidades', blank=True)  # Relación de muchos a muchos con Habilidades
    


    class Meta:
        verbose_name = 'Personal' #Espara una visualización más amigable en el admin
        ordering = ['id'] #Ordena por el campo Nombre
        unique_together = ('numeroDoc', 'Contraseña') #Indica que un valor no se vuelva a repetir 


    def __str__(self):
        return self.Nombre
    


#Modelo de QR 
class Usuario(models.Model):
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    NumeroDoc = models.CharField(max_length=100)
    Correo = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='media/qr_codes', blank=True)# Para usar este tenemos que instalar (python -m pip install Pillow) por que vamos a usar una imagen
    
    
    #Instalamos el (pip install qrcode)
    def save(self, *args, **kwargs):

        #Aqui almacenamos este enlace en una variable 
        url = 'https://i.pinimg.com/1200x/1c/8f/b9/1c8fb9feaf1267dec6cfd42660f5e14d.jpg'

        # Combinar todos los datos en un solo string
        data = f"Nombre: {self.Nombre}\nApellido: {self.Apellido}\nDocumento: {self.NumeroDoc}\nCorreo: {self.Correo}"

        # Generar el QR con esa información
        #dentro del make colocamos lo que es la variable al cual le asiganamos los datos que queremos que se vean al escanear el codigo qr
        # Crear el código QR con alta corrección de errores
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Crear fondo con degradado azul a verde
        width, height = qr_img.size
        gradient = Image.new("RGBA", (width, height), "#00B4FF")
        for y in range(height):
            r = 0
            g = int(180 + (255 - 180) * y / height)
            b = int(255 + (0 - 255) * y / height)
            for x in range(width):
                gradient.putpixel((x, y), (r, g, b, 255))

        # Mezclar fondo con QR
        blended = Image.alpha_composite(gradient, qr_img)

        # Redondear bordes del QR
        radius = 40
        mask = Image.new("L", blended.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
        rounded_qr = ImageOps.fit(blended, blended.size)
        rounded_qr.putalpha(mask)

        # Ruta del logo
        logo_path = os.path.join('static', 'images', 'cba.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")

            # Redimensionar el logo
            logo_size = 100
            logo.thumbnail((logo_size, logo_size), Image.LANCZOS)

            # Crear círculo blanco de fondo
            circle = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)

            white_bg = Image.new("RGBA", logo.size, "white")
            white_bg.putalpha(circle)

            logo_circle = Image.composite(logo, white_bg, circle)

            # Posición centrada
            pos = (
                (rounded_qr.size[0] - logo_circle.size[0]) // 2,
                (rounded_qr.size[1] - logo_circle.size[1]) // 2
            )

            # Limpiar fondo detrás del logo
            draw_bg = ImageDraw.Draw(rounded_qr)
            draw_bg.ellipse(
                [
                    pos,
                    (pos[0] + logo_circle.size[0], pos[1] + logo_circle.size[1])
                ],
                fill="white"
            )

            # Pegar logo
            rounded_qr.paste(logo_circle, pos, logo_circle)

        # Crear lienzo y pegar el QR centrado
        canvas = Image.new('RGBA', (500, 500), 'white')
        qr_pos = (
            (canvas.size[0] - rounded_qr.size[0]) // 2,
            (canvas.size[1] - rounded_qr.size[1]) // 2
        )
        canvas.paste(rounded_qr, qr_pos, rounded_qr)

        # Guardar imagen en memoria
        fname = f'qr_code-{self.Nombre}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        buffer.seek(0)

        # Guardar en el campo ImageField
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        # Guardar el modelo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Nombre

    


class Habilidades(models.Model):
    habilidad = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Habilidad'
        ordering = ['habilidad']

    def __str__(self):
        return self.habilidad
