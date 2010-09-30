from django.contrib.gis.db import models

# Models from opengemdb
# related to hazard curve serialization:
# hazardcalculation, hazardcurve, hazardpointvalue, geopoint, 
# intensitymeasuretype, hazardinputltreemodel, hilmpath, hazardinputbasicmodel
#
# Initially generated with ogrinspect and modified manually
# author aurea moemke
# started: 29 Sep 2010

class Calculationgroup(models.Model):
    cgcode = models.CharField("Group Code", primary_key=True) 
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
    cocode = models.CharField("Owner Code", primary_key=True)
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
    ecid = models.IntegerField("Id", primary_key=True)
    ecprivatetag = models.BooleanField("Private To GEM?", default=True)
    ecshortname = models.CharField("Short Name", max_length=20)
    ecname = models.CharField("Name", max_length=50)
    ecdesc = models.CharField("Description", max_length=100)
    ecformattype = models.IntegerField("Format Type", 
                                       choices=EQCATFORMATTYPE_CHOICES)
    eccattype = models.CharField("Earthquake Catalog Type",
                                 choices=EQCATTYPE_CHOICES)
    ecstartdate = models.DateTimeField("Start Date")
    ecenddate = models.DateTimeField("End Date")
    ectimezone = models.CharField("Time Zone", 
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

class Econstant(models.Model):
    EDATATYPE_CHOICES = ( 
        (1, 'Integer'),
        (2, 'Float'),
        (3, 'String'),
        (4, 'Boolean')
    ) 
    eccode = models.CharField("Code", max_length=10, primary_key=True)
    ectypeid = models.IntegerField("Equation Constant Data Type",
                                   choices=EDATATYPE_CHOICES)
    ecshortname = models.CharField("Short Name", max_length=20)
    ecname =  models.CharField("Name", max_length=50)
    ecdesc = models.CharField("Description", max_length=100)
    ecremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'econstant'
    def __unicode__(self):
        return self.ecname

#TODO: Multicolumn primary keys
class Ecreference(models.Model):
    rlid = models.ForeignKey(Referenceliterature, db_column='rlid')
    ecid = models.ForeignKey(Earthquakecatalog, db_column='ecid')
    eradddate = models.DateTimeField()
    class Meta:
        db_table = u'ecreference'
    def __unicode__(self):
        return "Reference"+str(self.ecrlid)+str(self.ecid)

class Eqcatcompleteness(models.Model):
    EQCATCOMPTYPE_CHOICES = ( 
        ('T', 'Time Complete'),
        ('R', 'Region Complete'),
        ('O', 'Others')
    )
    ccid = models.IntegerField(primary_key=True)
    cctype = models.CharField("Catalog Completeness Code", max_length=1,
                               choices=EQCATCOMPTYPE_CHOICES)
    ccareapolygon = models.CharField("Polygon WKT", max_length=5120)
    ccareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    ccstartdate = models.DateTimeField("Start Date")
    ccenddate = models.DateTimeField("End Date")
    ccmlevel = models.FloatField("Magnitude Completeness Level")
    ecid = models.ForeignKey(Earthquakecatalog, db_column='ecid')
    #Geometry fields
    ccpgareapolygon = models.PolygonField(blank=True)
    ccpgareamultipolygon = models.MultiPolygonField(blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = u'eqcatcompleteness'
    def __unicode__(self):
        return "EqCatCompletenessID"+str(self.ccid)

class Evariable(models.Model):
    DATATYPE_CHOICES = ( 
        (1, 'Integer'),
        (2, 'Float'),
        (3, 'String'),
        (4, 'Boolean')
    ) 
    evcode = models.CharField("Variable code", max_length=10, primary_key=True)
    evtypeid = models.IntegerField("Data Type", 
                  choices=DATATYPE_CHOICES)
    evshortname = models.CharField("Short Name", max_length=20)
    evname =  models.CharField("Name", max_length=50)    
    evdesc = models.CharField("Description", max_length=100)
    evremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'evariable'
    def __unicode__(self):
        return self.evname

class Event(models.Model):
    evid = models.IntegerField("Id", primary_key=True)
    evshortname = mmodels.CharField("Short Name", max_length=20)
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

# TODO:Change to Multicolumn primary key: gfcode+gecode
class Gefeaturevalue(models.Model):
    gfcode = models.ForeignKey(Gmpefeature, db_column='gfcode')
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    gefvalstring = models.CharField("Value String", max_length=50)
    gefremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gefeaturevalue'
    def __unicode__(self):
        return self.gfcode+self.gecode

class Geopoint(models.Model):
    gpid = models.IntegerField("Id", primary_key=True)
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

# TODO:Change to Multicolumn primary key: rlid+gecode
class Gereference(models.Model):
    rlid = models.ForeignKey(Referenceliterature, db_column='rlid')
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    gradddate = models.DateTimeField()
    class Meta:
        db_table = u'gereference'
    def __unicode__(self):
        return str(self.rlid)+self.gecode

# TODO:Change to Multicolumn primary key: gecode+eccode
class Gmeconstant(models.Model):
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    eccode = models.ForeignKey(Econstant, db_column='eccode')
    gmecvalue = models.CharField("Value of Constant", max_length=20)
    gmecremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gmeconstant'
    def __unicode__(self):
        return self.gecode+self.eccode

# TODO:Change to Multicolumn primary key: gecode+evcode
class Gmevariable(models.Model):
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    evcode = models.ForeignKey(Evariable, db_column='evcode')
    gmevremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gmevariable'
    def __unicode__(self):
        return self.gecode+self.evcode

# TODO:Change to Multicolumn primary key: gpcode+gecode
class Gmparamvalue(models.Model):
    gpcode = models.ForeignKey(Gmpeparameter, db_column='gpcode')
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    gepvalstring = models.CharField("Parameter Value String", max_length=50)
    gepremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gmparamvalue'
    def __unicode__(self):
        return self.gpcode+self.gecode

class Gmpe(models.Model):
    EQNTYPE_CHOICES = (
        ('S','Standard 3 constants'),
        ('O','Other')
    )
    gecode = models.CharField("GMPE Code", primary_key=True)
    geprivatetag = models.BooleanField("Private to GEM?")
    geshortname = mmodels.CharField("Short Name", max_length=20)
    gename = models.CharField("Name", max_length=50)
    gedesc = models.CharField("Description", max_length=100)
    geremarks = models.CharField("Remarks", max_length=255)
    geequation = models.CharField("Functional Form", max_length=5120)
    geeqndbdefntag = models.BooleanField("Equation Fcnal Form Defined in DB?")
    geeqntypecode = models.CharField("Equation Type Code", max_length=1,
                    choices=EQNTYPE_CHOICES) 
    geareapolygon = models.CharField("Polygon WKT", max_length=5120)
    geareamultipolygon = models.CharField("Multipolygon WKT", max_length=5120)
    secode = models.ForeignKey(Seismotecenvt, db_column='secode')
    # Geospatial data
    gepgareapolygon = models.PolygonField()
    gepgareamultipolygon = models.MultiPolygonField()
    objects = models.GeoManager()
    class Meta:
        db_table = u'gmpe'
    def __unicode__(self):
        return self.gename

class Gmpefeature(models.Model):
    gfcode = models.CharField(max_length=10, primary_key=True)
    gftypeid = models.IntegerField()
    gfpossvalstring = models.CharField(max_length=2048)
    gfshortname = models.CharField("Short Name", max_length=20)
    gfname = models.CharField("Name", max_length=50)
    gfdesc = models.CharField("Description", max_length=100)
    gfremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gmpefeature'
    def __unicode__(self):
        return self.gfname

class Gmpeparameter(models.Model):
    gpcode = models.TextField(max_length=10, primary_key=True)
    gptypeid = models.IntegerField()
    gppossvalstring = models.CharField("Possible Value", max_length=2048)
    gpshortname = mmodels.CharField("Short Name", max_length=20)
    gpname = models.CharField("Name", max_length=50)
    gpdesc = models.CharField("Description", max_length=100)
    gpremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'gmpeparameter'
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
    imunittype = models.CharField() 
    imunitdescr = models.CharField("Description", max_length=100)
    imremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'intensitymeasuretype'
    def __unicode__(self):
        return self.imname

class Magrupturerelation(models.Model):
    mrrcode = models.CharField(max_length=10, primary_key=True)
    mrrname = models.CharField(max_length=50)
    mrrdesc = models.CharField(max_length=100)
    mrrremarks = models.CharField(max_length=255)
    class Meta:
        db_table = u'magrupturerelation'
    def __unicode__(self):
        return self.mrrname

class Logictreestruc(models.Model):
    ltsid = models.IntegerField(primary_key=True)
    ltsshortname = mmodels.CharField("Short Name", max_length=20)
    ltsname = models.CharField("Name",max_length=50)
    ltsdesc = models.CharField("Description", max_length=100)
    ltsremarks = models.CharField("Remarks", max_length=255)
    ltsnumlevels = models.IntegerField("Number of Levels")
    class Meta:
        db_table = u'logictreestruc'
    def __unicode__(self):
        return self.ltsname

class Ltreeparamtype(models.Model):
    DATATYPE_CHOICES = ( 
        (1, 'Integer'),
        (2, 'Float'),
        (3, 'String'),
        (4, 'Boolean')
    ) 
    ltptid = models.IntegerField(primary_key=True)
    ltptshortname = mmodels.CharField("Short Name", max_length=20)
    ltptname = models.CharField("Name", max_length=50)
    ltptdesc = models.CharField("Description", max_length=100)
    ltptdatatypecode = models.IntegerField("Data Type Code",
                       choices = DATATYPE_CHOICES)
    ltptpossvalstring = models.CharField("Possible Value String")
    ltptvaluemin = models.FloatField("Minimum Value")
    ltptvaluemax = models.FloatField("Maximum Value")
    ltptmapping = models.CharField("Mapping", max_length=255)
    ltptremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'ltreeparamtype'
    def __unicode__(self):
        return self.ltptname

class Hazardpointvalue(models.Model):
    hpid = models.IntegerField(primary_key=True)
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

#TODO: Multicolumn primary keys
class Hibmge(models.Model):
    hibmid = models.ForeignKey(Hazardinputbasicmodel, db_column='hibmid')
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    hibmgeweight = models.FloatField()
    class Meta:
        db_table = u'hibmge'

class Seismicsource(models.Model):
   SEISMICSOURCETYPE_CHOICES = (
        (1, 'Simple Fault'),
        (5, 'Complex/Subduction Fault'),
        (2, 'Area Source Zone'),
        (3, 'Gridded Seismicity Point'),
        (4, 'Seismic Point'),
    )
    GEOMTYPE_CHOICES = (
        (1, 'Point'),
        (2, 'Multilinestring'),
        (3, 'Polygon'),
        (4, 'Multipolygon'),
    )
    scid = models.ForeignKey(SourceGeometryCatalog, db_column = 'scid')
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

# TODO: add support for multicolumn indexes
# Currently no support for composite/multicolumn primary keys in Django
class Ssourcemfd(models.Model):
    SLIPTYPECODE_CHOICES = (
        (1, 'Normal'),
        (2, 'Reverse'),
        (3, 'StrikeSlip'),
    )
    ssid = models.ForeignKey("Id", Seismicsource, db_column='ssid')
    mfdcode = models.ForeignKey(Magfreqdistn, db_column='mfdcode')
    ssmfdseqnum = models.IntegerField("Sequence Number")
    ssmfdmagnitudemax = models.FloatField("Maximum Magnitude")
    ssmfdmagnitudemin = models.FloatField("Minimum Magnitude")
    ssmfdvala = models.FloatField("a Value")
    ssmfdvalb = models.FloatField("b Value")
    ssmfdlambda = models.FloatField("Lambda Value")
    ssmfdbeta = models.FloatField("Beta Value")
    ssmfdvalaorig = models.FloatField("Original a value")
    ssmfdcharmagnitude = models.FloatField("Char Magnitude")
    ssmfdcharrate = models.FloatField("Char Rate")
    ssmfdcharmagsd = models.FloatField("Char Magnitude Standard Deviation")
    ssmfdtrunclevel = models.FloatField("Truncation Level")
    ssmfdmodelweight = models.FloatField("Model Weight")
    ssmfdmomentrate = models.FloatField("Moment Rate")
    ssmfdstrike = models.IntegerField("Strike (degrees)")
    ssmfddip = models.IntegerField("Dip (degrees)")
    ssmfdrake = models.IntegerField("Rake (degrees)")
    ssmfddipdirection = models.CharField("Dip Direction", max_length=5)
    ssmfddowndipwidth = models.FloatField("Downdip Width")
    ssmfdtopoffault = models.FloatField("Top of Fault")
    ssmfdfaultlength = models.FloatField("Fault Length")
    ssmfdsliptypecode = models.IntegerField("Slip Type Code",
                        choices=SLIPTYPECODE_CHOICES)
    mrrcode = models.ForeignKey(Magrupturerelation, db_column='mrrcode')
    ssmfderrorcode = models.IntegerField()
    ssmfdremarks = models.CharField("Remarks", max_length=255)
    ssmfddisctag = models.BooleanField("Discretization Tag")
    ssmfddeltamag = models.FloatField("Discretization Step")
    ssmfdnumintervals = models.IntegerField("Number of Discrete Intervals")
    ssmfddiscvalsstring = models.CharField(
            "Magnitude, Seismic Rate pairs for Discrete MFD", max_length=2048)
    class Meta:
        db_table = u'ssourcemfd'
    def __unicode__(self):
        return str(self.ssid)+mfdcode+str(self.ssmfdseqnum)

class Sourcegeometrycatalog(models.Model):
    SOURCEGEOMCATTYPE_CHOICES = ( 
        (u'H', u'Historical'),
        (u'I', u'Instrumental'),
        (u'HI', u'Combination Historical and Instrumental'),
        (u'S', u'Synthetic'),
        (u'O', u'Others'),
    )
    ORIGFORMATTYPE_CHOICES = (
        ( 1, u'Ascii Text'),
        ( 2, u'Excel File Format'),
        ( 3, u'Comma Separated Value Format'),
        ( 4, u'ESRI Shapefile'),
        ( 5, u'Others'),
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

#class GeographyColumns(models.Model):
#    f_table_catalog = models.TextField() # This field type is a guess.
#    f_table_schema = models.TextField() # This field type is a guess.
#    f_table_name = models.TextField() # This field type is a guess.
#    f_geography_column = models.TextField() # This field type is a guess.
#    coord_dimension = models.IntegerField()
#    srid = models.IntegerField()
#    type = models.TextField()
#    class Meta:
#        db_table = u'geography_columns'

class Hilmpath(models.Model):
    hilmpid = models.IntegerField(primary_key=True)
    hilmppathstring = models.CharField("Path String", max_length=5120)
    hilmpfinalpathtag = models.BooleanField("Endbranch?")
    hilmid = models.ForeignKey(Hazardinputltreemodel, db_column='hilmid')
    hilmpweight = models.FloatField("Endbranch Weight")
    hilmpshortname = mmodels.CharField("Short Name", max_length=20)
    hilmpname = models.CharField("Name", max_length=50)
    hilmpdesc = models.CharField("Description", max_length=100)
    hilmpremarks = models.CharField("Remarks", max_length=255)
    scid = models.ForeignKey(Sourcegeometrycatalog, db_column='scid')
    hilmpltree = models.CharField("Ltree")
    class Meta:
        db_table = u'hilmpath'
    def __unicode__(self):
        return self.hilmppathstring

# TODO: Multicolumn primary keys
class Hibmreference(models.Model):
    rlid = models.ForeignKey(Referenceliterature, db_column='rlid')
    hibmid = models.ForeignKey(Hazardinputbasicmodel, db_column='hibmid')
    hibmradddate = models.DateTimeField()
    class Meta:
        db_table = u'hibmreference'

#class SpatialRefSys(models.Model):
#    srid = models.IntegerField(primary_key=True)
#    auth_name = models.CharField(max_length=256)
#    auth_srid = models.IntegerField()
#    srtext = models.CharField(max_length=2048)
#    proj4text = models.CharField(max_length=2048)
#    class Meta:
#        db_table = u'spatial_ref_sys'

#class GeometryColumns(models.Model):
#    f_table_catalog = models.CharField(max_length=256)
#    f_table_schema = models.CharField(max_length=256)
#    f_table_name = models.CharField(max_length=256)
#    f_geometry_column = models.CharField(max_length=256)
#    coord_dimension = models.IntegerField()
#    srid = models.IntegerField()
#    type = models.CharField(max_length=30)
#    class Meta:
#        db_table = u'geometry_columns'

class Hazardcurve(models.Model):
    hcrvid = models.IntegerField(primary_key=True)
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

class Hazardinputbasicmodel(models.Model):
    hibmid = models.IntegerField(primary_key=True)
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
    hilmid = models.IntegerField(primary_key=True)
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


class Hazardcalculation(models.Model):
    PROBDETTAG_CHOICES = (
        ( 'P', u'Probabilistic'),
        ( 'D', u'Deterministic')
    )
    hcid = models.IntegerField(primary_key=True)
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

class Hazardmap(models.Model):
    hmapid = models.IntegerField(primary_key=True)
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

class Hilmruleset(models.Model):
    hilmrid = models.IntegerField(primary_key=True)
    hilmrcvrgtypecode = models.IntegerField()
    hilmractiontypecode = models.IntegerField()
    hilmrvalstring = models.CharField() 
    hilmrprobpctstring = models.CharField()
    ltptid = models.ForeignKey(Ltreeparamtype, db_column='ltptid')
    ltpvid = models.ForeignKey(Ltreeparamvalue, db_column='ltpvid')
    hilmid = models.ForeignKey(Hazardinputltreemodel, db_column='hilmid')
    class Meta:
        db_table = u'hilmruleset'
    def __unicode__(self):
        return self.hilmrvalstring

class Hilmreference(models.Model):
    rlid = models.ForeignKey(Referenceliterature, db_column='rlid')
    hilmid = models.ForeignKey(Hazardinputltreemodel, db_column='hilmid')
    hilmradddate = models.DateTimeField()
    class Meta:
        db_table = u'hilmreference'
    def __unicode__(self):
        return self.ecname

class Hilmpge(models.Model):
    hilmpid = models.ForeignKey(Hilmpath, db_column='hilmpid')
    gecode = models.ForeignKey(Gmpe, db_column='gecode')
    hilmpgeweight = models.FloatField()
    class Meta:
        db_table = u'hilmpge'
    def __unicode__(self):
        return self.ecname

class Ltreeparamtypelevel(models.Model):
    ltptid = models.ForeignKey(Ltreeparamtype, db_column='ltptid')
    ltsid = models.ForeignKey(Logictreestruc, db_column='ltsid')
    ltptlevel = models.IntegerField()
    ltptnumbranches = models.IntegerField()
    ltptbranchsettag = models.BooleanField()
    class Meta:
        db_table = u'ltreeparamtypelevel'
    def __unicode__(self):
        return self.ecname

class Ltreeparamvalue(models.Model):
    ltpvid = models.IntegerField(primary_key=True)
    ltpvshortname = models.CharField("Short Name", max_length=20)
    ltpvname = models.CharField(max_length=50)
    ltpvdesc = models.CharField(max_length=100)
    ltpvremarks = models.CharField(max_length=255)
    ltptid = models.ForeignKey(Ltreeparamtype, db_column='ltptid')
    class Meta:
        db_table = u'ltreeparamvalue'
    def __unicode__(self):
        return self.ecname

class Sfaultchar(models.Model):
    ssfcid = models.IntegerField(primary_key=True)
    ssfcstatus = models.TextField() # This field type is a guess.
    ssfcsliprate = models.FloatField()
    ssfcslipratesd = models.FloatField()
    ssfcfloattypeid = models.IntegerField()
    ssfcfloatingruptureflag = models.BooleanField()
    ssfcfloatoffsetalongstrike = models.IntegerField()
    ssfcfloatoffsetalongdip = models.IntegerField()
    ssfcrupturetop = models.IntegerField()
    ssfcrupturebottom = models.IntegerField()
    ssid = models.ForeignKey(Seismicsource, db_column='ssid')
    class Meta:
        db_table = u'sfaultchar'
    def __unicode__(self):
        return self.ecname

class Magfreqdistn(models.Model):
    mfdcode = models.TextField(primary_key=True) # This field type is a guess.
    mfdname = models.CharField(max_length=50)
    mfddesc = models.CharField(max_length=100)
    mfdremarks = models.CharField(max_length=255)
    mfddisctag = models.BooleanField()
    class Meta:
        db_table = u'magfreqdistn'
    def __unicode__(self):
        return self.ecname

class Screference(models.Model):
    rlid = models.ForeignKey(Referenceliterature, db_column='rlid')
    scid = models.ForeignKey(Sourcegeometrycatalog, db_column='scid')
    scradddate = models.DateTimeField()
    class Meta:
        db_table = u'screference'
    def __unicode__(self):
        return self.ecname

class Referenceliterature(models.Model):
    rlid = models.IntegerField()
    rlmajorreftag = models.BooleanField()
    rlshortname = models.CharField("Short Name", max_length=20)
    rlmainauthorfname = models.TextField() # This field type is a guess.
    rlmainauthorlname = models.TextField() # This field type is a guess.
    rlotherauthor = models.CharField(max_length=512)
    rltitle = models.CharField(max_length=512)
    rlmediatype = models.TextField() # This field type is a guess.
    rlperiodicaltitle = models.CharField(max_length=512)
    rlpublishercity = models.CharField(max_length=100)
    rlpublishername = models.CharField(max_length=512)
    rlpubnyear = models.IntegerField()
    rlvolnum = models.IntegerField()
    rlissuenum = models.IntegerField()
    rlpagenums = models.CharField(max_length=100)
    rllastaccessdate = models.DateField()
    rltype = models.TextField() # This field type is a guess.
    rlurl = models.CharField(max_length=1024)
    rlremarks = models.CharField(max_length=255)
    class Meta:
        db_table = u'referenceliterature'

class Seismotecenvt(models.Model):
    secode = models.CharField(max_length=10, primary_key=True)
    sename = models.CharField("Name", max_length=50)
    sedesc = models.CharField("Description", max_length=100)
    seremarks = models.CharField("Remarks", max_length=255)
    class Meta:
        db_table = u'seismotecenvt'
    def __unicode__(self):
        return self.sename

class Siteamplification(models.Model):
    sacode = models.CharField(primary_key=True)
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
    socode = models.CharField(primary_key=True) # This field type is a guess.
    soname = models.CharField("Name", max_length=50)
    sodesc = models.CharField("Description", max_length=100)
    sovalue = models.CharField("Value", max_length=10)
    soremarks = models.CharField("Remarks",max_length=255)
    class Meta:
        db_table = u'soilclass'
    def __unicode__(self):
        return self.soname
