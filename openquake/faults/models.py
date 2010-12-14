from django.contrib.gis.db import models
from django.contrib.auth.models import User


DATA_COMPLETENESS = ((1, 'Incomplete'), 
                     (2, 'Partial'), 
                     (3, 'Adequate'), 
                     (4, 'Complete'),
)


DECIMAL_FIELD = {'decimal_places' : 2, 
               'max_digits' : 5,
               'null' : True,
               'blank' : True }

class Episodic(models.Model):
    is_episodic = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # objects = models.GeoManager()
    class Meta:
        abstract = True

class Fault(models.Model):
    """A Fault is a named collection of Fault Sections"""
    name = models.CharField(max_length=255)
    compiler = models.ForeignKey(User)
    contributer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    completeness = models.IntegerField(
            choices=DATA_COMPLETENESS, null=False, default=1)
    notes = models.TextField(default="", blank=True)
    # objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name


class FaultSection(models.Model):
    """Fault Sections are seismogenicly distinct portions of a fault trace"""
    fault = models.ForeignKey(Fault)
    slip_rate = models.DecimalField(**DECIMAL_FIELD)
    dip_angle = models.DecimalField(**DECIMAL_FIELD)
    rake_angle = models.DecimalField(**DECIMAL_FIELD)
    geometry = models.MultiLineStringField(blank=True)
    upper_depth = models.DecimalField(**DECIMAL_FIELD)
    lower_depth = models.DecimalField(**DECIMAL_FIELD)
    objects = models.GeoManager()


class Fold(models.Model):
    """Folds are named collections of Fold Sections"""
    pass


class FoldSection(models.Model):
    pass