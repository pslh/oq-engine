from django.db import models

# Create your models here.

class Fault(models.Model): 
    name = models.CharField(max_length=255)

class FaultSection(models.Model):
    fault = models.ForeignKey(Fault)
    slip_rate = models.DecimalField(decimal_places=2, max_digits=5)
    dip_angel = models.DecimalField(decimal_places=2, max_digits=5)
    rake_angel = models.DecimalField(decimal_places=2, max_digits=5)