from django.db import models

# Create your models here.
class Agency(models.Model): #Represents a government body
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name

class Procedure(models.Model): #Represents a procedure, e.g., a tax form
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    fecha_inicio = models.DateTimeField("Fecha de inicio")
    fecha_fin = models.DateTimeField("Fecha de fin")
    organo_convocante = models.ManyToManyField(Agency)

    def __str__(self):
        return self.name