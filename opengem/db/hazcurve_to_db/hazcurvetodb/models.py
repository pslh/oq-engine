from django.contrib.gis.db import models

# Models from opengemdb
# related to hazard curve serialization:
# hazardcalculation, hazardcurve, hazardpointvalue, geopoint, 
# intensitymeasuretype, hazardinputltreemodel, hilmpath, hazardinputbasicmodel
#
# Initially generated with ogrinspect and modified manually
# author aurea moemke
# started: 29 Sep 2010

class Seismotecenvt(models.Model):
    secode = models.CharField(max_length=10, primary_key=True)
    sename = models.CharField("Name", max_length=50)
    sedesc = models.CharField("Description", max_length=100)
    seremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'seismotecenvt'
    def __unicode__(self):
        return self.sename

class Calculationgroup(models.Model):
    cgcode = models.CharField("Group Code", max_length=10, primary_key=True) 
    cgname = models.CharField("Name", max_length=50)
    cgdesc = models.CharField("Description", max_length=100)
    cgauthlevel = models.CharField("Authorization Level", max_length=1)
    cgadddate = models.DateTimeField("Addition Date")
    cgremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'calculationgroup'
    def __unicode__(self):
        return self.cgname

class Calculationowner(models.Model):
    cocode = models.CharField("Owner Code", max_length=10, primary_key=True)
    coname = models.CharField("Name", max_length=50)
    codesc = models.CharField("Description", max_length=100)
    coauthlevel = models.CharField("Authorization Level", max_length=1)
    coadddate = models.DateTimeField("Addition Date")
    coremarks = models.CharField("Remarks", max_length=255)
    cgcode = models.ForeignKey(Calculationgroup, db_column='cgcode')
    class Meta:
        db_table = u'calculationowner'
    def __unicode__(self):
        return self.coname

class Earthquakecatalog(models.Model):
    EQCATFORMATTYPE_CHOICES = (
        (1, 'GSHAPEA Format'),
        (2, 'USGS Earthquake Catalog Format'),
        (3, 'SED Format'),
        (9, 'Others'),
    )
    EQCATTYPE_CHOICES = ( 
        (u'H', u'Historical'),
        (u'I', u'Instrumental'),
        (u'HI', u'Combination Historical and Instrumental'),
        (u'S', u'Synthetic'),
        (u'O', u'Others'),
    )
    #TODO: Fix Time zone choices
    TIMEZONE_CHOICES = (
        ('UTC+10:30','Australian Central Daylight Time'),
        ('UTC+9:30','Australian Central Standard Time'),
        ('UTC+8','ASEAN Common Time'),
        ('UTC-3','Atlantic Daylight Time'),
        ('UTC+11','Australian Eastern Daylight Time'),
        ('UTC+10','Australian Eastern Standard Time'),
        ('UTC+4:30','Afghanistan Time'),
    )
    ORIGFORMATID_CHOICES = (
        (1, 'GSHAPEA Ascii Text Format'),
        (2, 'USGS Ascii Text Format'),
        (3, 'QuakeML XML Format'),
        (4, 'ESRI Shapefile Format'),
        (9, 'Others'),
    )
    ecid = models.AutoField("Id", primary_key=True)
    ecprivatetag = models.BooleanField("Private To GEM?", default=True)
    ecshortname = models.CharField("Short Name", max_length=20)
    ecname = models.CharField("Name", max_length=50)
    ecdesc = models.CharField("Description", max_length=100)
    ecformattype = models.IntegerField("Format Type", 
                                       choices=EQCATFORMATTYPE_CHOICES)
    eccattype = models.CharField("Earthquake Catalog Type",
                                 max_length=5,
                                 choices=EQCATTYPE_CHOICES)
    ecstartdate = models.DateTimeField("Start Date")
    ecenddate = models.DateTimeField("End Date")
    ectimezone = models.CharField("Time Zone", max_length=10, 
                                 choices=TIMEZONE_CHOICES)
    eccvrgcd = models.CharField("Coverage Code (country/region code)", 
                                 max_length=10)
    ecorigformatid = models.IntegerField("Original Format Id",
                                 choices=ORIGFORMATID_CHOICES)
    ecremarks = models.CharField("Remarks", max_length=255)
    ecareapolygon = models.CharField("Polygon WKT", max_length=5120)
    ecareamultipolygon = models.CharField("Polygon WKT", max_length=5120)
    #Geometry fields
    ecpgareapolygon = models.PolygonField(blank=True)
    ecpgareamultipolygon = models.MultiPolygonField(blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = u'earthquakecatalog'

    def __unicode__(self):
        return self.ecname

class Event(models.Model):
    evid = models.AutoField("Event Id", primary_key=True)
    evshortname = models.CharField("Short Name", max_length=20)
    evname = models.CharField("Name", max_length=50)
    evdesc = models.CharField("Description", max_length=100)
    evorigid = models.CharField("Name in Original Catalog", max_length=50)
    evtimestamp = models.DateTimeField()
    evyear = models.IntegerField()
    evmonth = models.IntegerField()
    evday = models.IntegerField()
    evhour = models.IntegerField()
    evmin = models.IntegerField()
    evsec = models.IntegerField()
    evnanosec = models.IntegerField()
    evlat = models.FloatField()
    evlong = models.FloatField()
    evdepth = models.FloatField()
    evmagnitude = models.FloatField()
    evremarks = models.CharField("Remarks", max_length=255)
    evothdata1 = models.CharField("Other Relevant Data 1", max_length=100)
    evothdata2 = models.CharField("Other Relevant Data 2", max_length=100)
    evref = models.CharField("Event Reference Information", max_length=100)
    everrorcode = models.IntegerField("Error Code")
    evpoint = models.CharField("Point WKT", max_length=255)
    ecid = models.ForeignKey(Earthquakecatalog, db_column='ecid')
    #Geospatial data
    evpgpoint = models.PointField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'event'
    def __unicode__(self):
        return self.evname

class Siteamplification(models.Model):
    sacode = models.CharField(max_length=10, primary_key=True)
    saname = models.CharField("Name", max_length=50)
    sadesc = models.CharField("Description", max_length=100)
    savs30min = models.IntegerField("VS 30 Minimum")
    savs30max = models.IntegerField("VS 30 Maximum")
    savs30descstring = models.CharField("VS 30 Description", max_length=50)
    sanehrp = models.CharField("NEHRP Code", max_length=4)
    saintampl = models.FloatField("Intensity Amplification")
    saremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'siteamplification'
    def __unicode__(self):
        return self.saname

class Soilclass(models.Model):
    socode = models.CharField(max_length=10, primary_key=True)
    soname = models.CharField("Name", max_length=50)
    sodesc = models.CharField("Description", max_length=100)
    sovalue = models.CharField("Value", max_length=10)
    soremarks = models.CharField("Remarks",max_length=255)
    class Meta:
        db_table = u'soilclass'
    def __unicode__(self):
        return self.soname

class Geopoint(models.Model):
    gpid = models.AutoField("Geopoint Id", primary_key=True)
    gppoint = models.CharField("Point WKT", max_length=255)
    gpname = models.CharField("Name", max_length=50)
    gpdesc = models.CharField("Description", max_length=100)
    sacode = models.ForeignKey(Siteamplification, db_column='sacode')
    socode = models.ForeignKey(Soilclass, db_column='socode')
    # Geospatial data
    gppgpoint = models.PointField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'geopoint'
    def __unicode__(self):
        return self.gpname

class Hazardsoftware(models.Model):
    hscode = models.TextField(primary_key=True) # This field type is a guess.
    hsname =  models.CharField("Name", max_length=50)
    hsdesc = models.CharField("Description", max_length=100)
    hsadddate = models.DateTimeField("Addition Date")
    hsremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'hazardsoftware'
    def __unicode__(self):
        return self.hsname

class Intensitymeasuretype(models.Model):
    imcode = models.TextField(primary_key=True) # This field type is a guess.
    imname =  models.CharField("Name", max_length=50)
    imdesc = models.CharField("Description", max_length=100)
    imvaluemin = models.FloatField("Intensity Measure Minimum Value")
    imvaluemax = models.FloatField("Intensity Measure Maximum Value")
    imunittype = models.CharField("Unit type", max_length=10) 
    imunitdescr = models.CharField("Unit Description", max_length=100)
    imremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'intensitymeasuretype'
    def __unicode__(self):
        return self.imname

class Logictreestruc(models.Model):
    ltsid = models.AutoField("Logic Tree Structure Id", primary_key=True)
    ltsshortname = models.CharField("Short Name", max_length=20)
    ltsname = models.CharField("Name",max_length=50)
    ltsdesc = models.CharField("Description", max_length=100)
    ltsremarks = models.CharField("Remarks", max_length=255)
    ltsnumlevels = models.IntegerField("Number of Levels")
    class Meta:
        db_table = u'logictreestruc'
    def __unicode__(self):
        return self.ltsname

class Sourcegeometrycatalog(models.Model):
    SOURCEGEOMCATTYPE_CHOICES = ( 
        (u'H', u'Historical'),
        (u'I', u'Instrumental'),
        (u'HI', u'Combination Historical and Instrumental'),
        (u'S', u'Synthetic'),
        (u'O', u'Others')
    )
    ORIGFORMATTYPE_CHOICES = (
        ( 1, u'Ascii Text'),
        ( 2, u'Excel File Format'),
        ( 3, u'Comma Separated Value Format'),
        ( 4, u'ESRI Shapefile'),
        ( 5, u'Others')
    )
    scid = models.AutoField("Catalog Id", primary_key=True)
    scprivatetag = models.BooleanField("Private to Opengem", default=True)
    scshortname = models.CharField("Short Name:", max_length=20)
    scname = models.CharField(max_length=50)
    scdesc = models.CharField(max_length=100,blank = True)
    sctypecode = models.CharField("Catalog Type", max_length=5, 
                      choices=SOURCEGEOMCATTYPE_CHOICES, default='I')
    scareapolygon = models.CharField("Polygon WKT", max_length=5120)
    scareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    scstartdate = models.DateTimeField("Start Date", blank=True)
    scenddate = models.DateTimeField("End Date", blank=True)
    scsources = models.CharField("Sources of data", max_length=255, blank=True) 
    scorigformatid = models.IntegerField("Original Format Type",
                     choices=ORIGFORMATTYPE_CHOICES,default=u'O')
    scremarks = models.CharField("Remarks", max_length=255, blank=True)
    #Geodjango-specific: a geometry field, 
    #and overriding the default manager with a GeoManager instance.
    scpgareapolygon = models.PolygonField(blank=True)
    scpgareamultipolygon = models.MultiPolygonField(blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = u'sourcegeometrycatalog'
    def __unicode__(self):
        return self.scname


class Hazardinputbasicmodel(models.Model):
    hibmid = models.AutoField("Hazard Basic Model", primary_key=True)
    hibmshortname = models.CharField("Short Name", max_length=20)
    hibmname = models.CharField("Name", max_length=50)
    hibmdesc = models.CharField("Description", max_length=100)
    hibmremarks = models.CharField("Remarks", max_length=255)
    hibmcvrgtypecode = models.CharField("Coverage Type Code", max_length=1) 
    hibmareapolygon = models.CharField("Polygon WKT", max_length=5120)
    hibmareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    scid = models.ForeignKey(Sourcegeometrycatalog, db_column='scid')
    #Geospatial data
    hibmpgareapolygon = models.PolygonField()
    hibmpgareamultipolygon = models.MultiPolygonField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'hazardinputbasicmodel'
    def __unicode__(self):
        return self.hibmname

class Hazardinputltreemodel(models.Model):
    hilmid = models.AutoField("Hazard Input Logic Tree Model Id", 
                              primary_key=True)
    hilmshortname = models.CharField("Short Name", max_length=20)
    hilmname = models.CharField("Name", max_length=50)
    hilmdesc = models.CharField("Description", max_length=100)
    hilmremarks = models.CharField("Remarks", max_length=255)
    hilmcvrgtypecode = models.IntegerField()
    hilmareapolygon = models.CharField("Polygon WKT", max_length=5120)
    hilmareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    ltsid = models.ForeignKey(Logictreestruc, db_column='ltsid')
    # Geospatial data
    hilmpgareapolygon = models.PolygonField()
    hilmpgareamultipolygon = models.MultiPolygonField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'hazardinputltreemodel'
    def __unicode__(self):
        return self.hilmname


class Hilmpath(models.Model):
    hilmpid = models.AutoField("Hazard Input Logic Tree Model Path Id", 
                               primary_key=True)
    hilmppathstring = models.CharField("Path String", max_length=5120)
    hilmpfinalpathtag = models.BooleanField("Endbranch?")
    hilmid = models.ForeignKey(Hazardinputltreemodel, db_column='hilmid')
    hilmpweight = models.FloatField("Endbranch Weight")
    hilmpshortname = models.CharField("Short Name", max_length=20)
    hilmpname = models.CharField("Name", max_length=50)
    hilmpdesc = models.CharField("Description", max_length=100)
    hilmpremarks = models.CharField("Remarks", max_length=255)
    scid = models.ForeignKey(Sourcegeometrycatalog, db_column='scid')
    #hilmpltree = models.CharField("Ltree")
    class Meta:
        db_table = u'hilmpath'
    def __unicode__(self):
        return self.hilmppathstring

class Hazardcalculation(models.Model):
    PROBDETTAG_CHOICES = (
        ( 'P', u'Probabilistic'),
        ( 'D', u'Deterministic')
    )
    hcid = models.AutoField("Hazard Calculation Id", primary_key=True)
    hcshortname = models.CharField("Short Name", max_length=20)
    hcname = models.CharField("Name", max_length=50)
    hcdesc = models.CharField("Description", max_length=100)
    hcstarttimestamp = models.DateTimeField()
    hcendtimestamp = models.DateTimeField()
    hcprobdettag = models.CharField("(P)robabilistic/(D)eterministic",
                    max_length=1,
                    choices=PROBDETTAG_CHOICES)
    hcgemgentag = models.BooleanField()
    hcareapolygon = models.CharField("Polygon WKT", max_length=5120)
    hcareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    hcremarks = models.CharField("Remarks", max_length=255)
    hibmid = models.ForeignKey(Hazardinputbasicmodel, db_column='hibmid')
    hilmid = models.ForeignKey(Hazardinputltreemodel, db_column='hilmid')
    hilmpid = models.ForeignKey(Hilmpath, db_column='hilmpid')
    evid = models.ForeignKey(Event, db_column='evid')
    hscode = models.ForeignKey(Hazardsoftware, db_column='hscode')
    cocode = models.ForeignKey(Calculationowner, db_column='cocode')
    # Geospatial data
    hcpgareapolygon = models.PolygonField()
    hcpgareamultipolygon = models.MultiPolygonField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'hazardcalculation'
    def __unicode__(self):
        return self.hcname

class Hazardpointvalue(models.Model):
    hpid = models.AutoField("Hazard Point Value Id", primary_key=True)
    hpvalue = models.FloatField("Ground Motion Value")
    hpexceedprob = models.FloatField("Prob'y of Exceedance")
    hpexceedyears = models.IntegerField("Years")
    hcid = models.ForeignKey(Hazardcalculation, db_column='hcid')
    gpid = models.ForeignKey(Geopoint, db_column='gpid')
    imcode = models.ForeignKey(Intensitymeasuretype, db_column='imcode')
    class Meta:
        db_table = u'hazardpointvalue'
    def __unicode__(self):
        return "Haz Pt Id "+ str(self.hpid)

class Seismicsource(models.Model):
    SEISMICSOURCETYPE_CHOICES = (
        (1, 'Simple Fault'),
        (5, 'Complex/Subduction Fault'),
        (2, 'Area Source Zone'),
        (3, 'Gridded Seismicity Point'),
        (4, 'Seismic Point')
    )
    GEOMTYPE_CHOICES = (
        (1,'Point'),
        (2,'Multilinestring'),
        (3,'Polygon'),
        (4,'Multipolygon')
    )
    scid = models.ForeignKey(Sourcegeometrycatalog, db_column = 'scid')
    ssid = models.AutoField("Seismic Source Id", primary_key=True)
    sssrctypecode = models.IntegerField("Seismic Source Type Code", 
                choices=SEISMICSOURCETYPE_CHOICES)
    ssgeomtypecode = models.IntegerField("Geometry Type Code",
                choices=GEOMTYPE_CHOICES)
    ssgrdefaulttag = models.BooleanField("Gutenberg-Richter Default?")
    ssorigid = models.CharField("Original Seismic Source Id", max_length=50)
    ssshortname = models.CharField("Short Name", max_length = 20)
    ssname = models.CharField("Name", max_length = 50)
    ssdesc = models.CharField("Description", max_length = 100)
    ssremarks = models.CharField("Remarks", max_length = 255)
    ssarea = models.FloatField("Area")
    ssanormalized = models.FloatField("Normalized a value")
    ssdepth = models.FloatField("Depth")
    ssbackgrdzonetag = models.BooleanField("Background Zone?")
    sserrorcode = models.IntegerField()
    ssmultilinestring = models.CharField(max_length=5120)
    sstopmultilinestring = models.CharField(max_length=5120)
    ssbottommultilinestring = models.CharField(max_length=5120)
    sspolygon = models.CharField(max_length=5120)
    ssmultipolygon = models.CharField(max_length=5120)
    sspoint = models.CharField(max_length=255)
    secode = models.ForeignKey(Seismotecenvt, db_column='secode')
    #Geodjango-specific:
    sspgpolygon = models.PolygonField()
    sspgmultipolygon = models.MultiPolygonField()
    sspgmultilinestring = models.MultiLineStringField()
    sspgtopmultilinestring = models.MultiLineStringField()
    sspgbottommultilinestring = models.MultiLineStringField()
    sspgpoint = models.PointField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'seismicsource'
    #Returns string representation of the model.
    def __unicode__(self):
        return self.ssname

class Hazardcurve(models.Model):
    hcrvid = models.AutoField("Hazard Curve Id", primary_key=True)
    hcrvshortname = models.CharField("Short Name", max_length=20)
    hcrvname = models.CharField("Name", max_length=50)
    hcrvdesc = models.CharField("Description", max_length=100)
    hcrvtimestamp = models.DateTimeField("Timestamp")
    hcrvmingrdmotion = models.FloatField("Minimum Ground Motion")
    hcrvmaxgrdmotion = models.FloatField("Maximum Ground Motion")
    hcrvtimeperiod = models.IntegerField("Time Period")
    hcrvsadamping = models.FloatField("SA Damping")
    hcrvsaperiod = models.IntegerField("SA Period")
    hcrvremarks = models.CharField("Remarks", max_length=255)
    hcid = models.ForeignKey(Hazardcalculation, db_column='hcid')
    gpid = models.ForeignKey(Geopoint, db_column='gpid')
    imcode = models.ForeignKey(Intensitymeasuretype, db_column='imcode')
    class Meta:
        db_table = u'hazardcurve'
    def __unicode__(self):
        return self.hcrvname

class Hazardmap(models.Model):
    hmapid = models.AutoField("Hazard Map Id", primary_key=True)
    hmapshortname = models.CharField("Short Name", max_length=20)
    hmapname = models.CharField("Name", max_length=50)
    hmapdesc = models.CharField("Description", max_length=100)
    hmaptimestamp = models.DateTimeField("Timestamp")
    hmaptimedepstartdate = models.DateTimeField("Time Dep Map Start Timestamp")
    hmaptimedependdate = models.DateTimeField("Time Dep Map End Timestamp")
    hmapexceedprob = models.IntegerField("Probability of Exceedance, i.e. 10")
    hmapexceedyears = models.IntegerField("Years, i.e. 50")
    hmapdamping = models.IntegerField("Damping")
    hmapgridsize = models.FloatField("Grid Size, i.e. 0.1")
    hmapremarks = models.CharField("Remarks",max_length=255)
    hcid = models.ForeignKey(Hazardcalculation, db_column='hcid')
    imcode = models.ForeignKey(Intensitymeasuretype, db_column='imcode')
    class Meta:
        db_table = u'hazardmap'
    def __unicode__(self):
        return self.hmapname


