from django.contrib.gis.db import models
from django.contrib.auth.models import User


DATA_COMPLETENESS = ((1, 'well-constrained'), 
                     (2, 'moderately-constrained'), 
                     (3, 'poorly-constrained'), 
                     (4, 'inferred'),
)

DISPLACEMENT = (    (1, '0.1 - <0.5'),
                    (2, '0.5 - <1'),
                    (3, '1 - <5'),
                    (4, '5 - <10'),
                    (5, '10 - <30'),
)

AGE = (
        (1, '0-1000' ),
        (2, '1000-11,700' ),
        (3, '11,700-50,000' ),
        (4, '50,000-100,000' ),
        (5, '100,000-1,000,000' ),
        (6, '1,000,000-10,000,000' ),
)

INTERVAL = (
        (1, '10 - <100' ),
        (2, '100 - <1000' ),
        (3, '1000 - <2000' ),
        (4, '2000 - <5000' ),
        (5, '5000 - <10,000' ),
        (6, '10,000 - <100,000' ),
        (7, '100,000 - <500,000' ),
        (8, '500,000 - <1,000,000' ),
        (9, '1,000,000 - <10,000,000' ),
)

SLIP_RATE = (
        (1, '0.001 - <0.01' ),
        (2, '0.01 - <0.1' ),
        (3, '0.1 - <1' ),
        (4, '1 - <5' ),
        (5, '5 - <10' ),
        (6, '10 - <50' ),
        (7, '50 - <100' ),
        (8, '100 - <200' ),
)

SLIP_TYPE = (
        (1, 'Reverse' ),
        (2, 'Thrust' ),
        (3, 'Normal' ),
        (4, 'Dextral' ),
        (5, 'Sinistral' ),
        (6, 'Normal-dextral' ),
        (7, 'Normal-sinistral' ),
        (8, 'Reverse-dextral' ),
        (9, 'Reverse-sinistral' ),
        (10, 'Dextral-normal' ),
        (11, 'Dextral-reverse' ),
        (12, 'Sinistral-reverse' ),
        (13, 'Sinistral-normal' ),
)

EXPRESSION = (
        (1, 'Surface trace' ),
        (2, 'Eroded scarp' ),
        (3, 'Sharp feature' ),
        (4, 'Topographic feature' ),
        (5, 'Bedrock extension' ),
        (6, 'Subtle feature' ),
        (7, 'Concealed' ),
        (8, 'No trace' ),
)

FOLD_TYPE = (
        (1, 'Anticline' ),
        (2, 'Syncline' ),
        (3, 'Monocline' ),
)

METHOD = (
        (1, 'GPS Survey' ),
        (2, 'LiDAR' ),
        (3, 'Aerial Photographs' ),
        (4, 'Topographic Map' ),
        (5, 'Google Earth' ),
)

OCTANT = (
        ('E', 'East' ),
        ('N', 'North' ),
        ('NE', 'North-East' ),
        ('NW', 'North-West' ),
        ('S', 'South' ),
        ('SE', 'South-East' ),
        ('SW', 'South-West' ),
        ('W', 'West' ),
)

DECIMAL_FIELD = {'decimal_places' : 2, 
               'max_digits' : 5,
               'null' : True,
               'blank' : True }


class FuzzyIntegerField(models.Field): # CompositeField
    # TODO(JMC): Implement this for multi-variate fields, e.g. the 
    #    min, max, preferred fields
    pass

class Episodic(models.Model):
    is_episodic = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = models.GeoManager()
    class Meta:
        abstract = True


class Fault(models.Model):
    """A Fault is a named collection of Fault Sections"""
    name = models.CharField(max_length=255)
    compiler = models.ForeignKey(User, default=1)
    contributer = models.CharField(max_length=255, default="GEM Faulted Earth")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    completeness = models.IntegerField(
            choices=DATA_COMPLETENESS, null=False, default=4)
    notes = models.TextField(default="", blank=True)
    verified_by = models.ForeignKey(
            User, related_name='verifier', null=True, editable=False)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name


class Observation(models.Model):
    fault = models.ForeignKey(Fault)
    geometry = models.PointField(blank=True, null=True)


class FaultSection(Episodic):
    """Fault Sections are seismogenicly distinct portions of a fault trace"""
    fault = models.ForeignKey(Fault)
    method = models.IntegerField(choices=METHOD, default=5)
    expression = models.IntegerField(choices=EXPRESSION, default=1)
    accuracy = models.DecimalField(decimal_places=2, max_digits=3, default=0.10)
    aseismic_slip_factor = models.DecimalField(
            decimal_places=2, max_digits=5, default=0.00)
    slip_rate = models.IntegerField(choices=SLIP_RATE, default=3, null=True)
    slip_type = models.IntegerField(choices=SLIP_TYPE, default=3)
    dip_angle = models.DecimalField(**DECIMAL_FIELD)
    rake_angle = models.DecimalField(**DECIMAL_FIELD) # DIP DIR?
    strike_angle = models.DecimalField(**DECIMAL_FIELD)
    geometry = models.MultiLineStringField(blank=True, null=True)
    upper_depth = models.DecimalField(**DECIMAL_FIELD)
    lower_depth = models.DecimalField(**DECIMAL_FIELD)
    downthrown_side = models.CharField(max_length=2, choices=OCTANT, 
            null=False, default='E')
    notes = models.TextField(default="", blank=True)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "some section"


class Recurrence(models.Model):
    section = models.ForeignKey(FaultSection)
    dip_slip_ratio = models.IntegerField(blank=True, null=True)
    marker_age = models.IntegerField(blank=True, null=True)
    scaling = models.IntegerField(blank=True, null=True)
    interval = models.IntegerField(choices=INTERVAL, default=1)
    earthquake = models.IntegerField(blank=True, null=True)


class Fold(models.Model):
    """Folds are named collections of Fold Sections"""
    pass


class FoldSection(models.Model):
    pass