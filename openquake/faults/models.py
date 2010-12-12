from django.db import models
from django.contrib.auth.models import User

DATA_COMPLETENESS = (   (1, 'Incomplete'), 
                        (2, 'Partial'), 
                        (3, 'Adequate'), 
                        (4, 'Complete'),
)

class Fault(models.Model):
    """Faults are a named collection of Fault Sections"""
    name = models.CharField(max_length=255)
    compiler = models.ForeignKey(User)
    contributer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    completeness = models.IntegerField(
            choices=DATA_COMPLETENESS, null=False, default=1)

class FaultSection(models.Model):
    """Fault Sections are seismogenicly distinct portions of a fault trace"""
    fault = models.ForeignKey(Fault)
    slip_rate = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    dip_angle = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    rake_angle = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    geometry = models.CharField(max_length=255) # TODO(JMC): Make this GEO
    upper_depth = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    lower_depth = models.DecimalField(decimal_places=2, max_digits=5, null=True)

