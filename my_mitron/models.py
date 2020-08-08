from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

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
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField("Start date")
    end_date = models.DateTimeField("End date")
    manager_agency = models.ManyToManyField(Agency)

    def __str__(self):
        return self.name

class Form(models.Model):
    name = models.CharField(max_length=100)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    

class FormItem(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    class Meta:
        abstract = True
    
    def __str__(self):
        return name

#Specify different kinds of preset Form items
class COIIItem(FormItem):
    coii_number = models.CharField("COII number", max_length=9, validators=[MaxLengthValidator(9),MinLengthValidator(9)])

class AddressItem(FormItem):
    address_number = models.IntegerField("Address number")
    postcode = models.IntegerField(validators=[MaxLengthValidator(5),MinLengthValidator(5)])
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, null=True)
