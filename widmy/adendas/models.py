from django.db import models
from historias.models import Historia

# Create your models here.

class Adenda(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    identificador = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return '{}'.format(self.identificador)

class Palabra(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    frase1 = models.TextField()
    frase2 = models.TextField()
    frase3 = models.TextField()

    class Meta:
        using = 'palabras'

    def __str__(self):
        return self.nombre