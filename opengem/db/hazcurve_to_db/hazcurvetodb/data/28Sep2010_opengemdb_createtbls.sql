--
-- PostgreSQL database dump
--
--
-- Name: calculationgroup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE calculationgroup (
    cgcode character(10) NOT NULL,
    cgname character varying(50),
    cgdesc character varying(100),
    cgauthlevel character(1),
    cgadddate timestamp without time zone,
    cgremarks character varying(255)
);


--
-- Name: TABLE calculationgroup; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE calculationgroup IS 'Calculation Group';


--
-- Name: COLUMN calculationgroup.cgcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationgroup.cgcode IS 'Calculation Group Code';


--
-- Name: COLUMN calculationgroup.cgname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationgroup.cgname IS 'Calculation Group Name';


--
-- Name: COLUMN calculationgroup.cgdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationgroup.cgdesc IS 'Calculation Group Description';


--
-- Name: COLUMN calculationgroup.cgauthlevel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationgroup.cgauthlevel IS 'Calculation Group Authorization Level';


--
-- Name: COLUMN calculationgroup.cgremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationgroup.cgremarks IS 'Remarks';


--
-- Name: calculationowner; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE calculationowner (
    cocode character(10) NOT NULL,
    coname character varying(50),
    codesc character varying(100),
    coauthlevel character(1),
    coadddate timestamp without time zone,
    coremarks character varying(255),
    cgcode character(10) NOT NULL
);


--
-- Name: TABLE calculationowner; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE calculationowner IS 'Calculation Owner';


--
-- Name: COLUMN calculationowner.cocode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.cocode IS 'Calculation Owner Code';


--
-- Name: COLUMN calculationowner.coname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.coname IS 'Calculation Owner Name';


--
-- Name: COLUMN calculationowner.codesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.codesc IS 'Description';


--
-- Name: COLUMN calculationowner.coauthlevel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.coauthlevel IS 'Calculation Owner Authorization Level';


--
-- Name: COLUMN calculationowner.coremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.coremarks IS 'Remarks';


--
-- Name: COLUMN calculationowner.cgcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN calculationowner.cgcode IS 'Calculation Group Code';


--
-- Name: earthquakecatalog; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE earthquakecatalog (
    ecid integer NOT NULL,
    ecprivatetag boolean,
    ecshortname character(20),
    ecname character varying(50),
    ecdesc character varying(100),
    ecformattype integer,
    eccattype character(5),
    ecstartdate timestamp without time zone,
    ecenddate timestamp without time zone,
    ectimezone character(10),
    eccvrgcd character(10),
    ecorigformatid integer,
    ecareapolygon character varying(5120),
    ecareamultipolygon character varying(5120),
    ecremarks character varying(255),
    ecpgareapolygon geometry,
    ecpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_ecpgareamultipolygon CHECK ((st_ndims(ecpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_ecpgareapolygon CHECK ((st_ndims(ecpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_ecpgareamultipolygon CHECK (((geometrytype(ecpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (ecpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_ecpgareapolygon CHECK (((geometrytype(ecpgareapolygon) = 'POLYGON'::text) OR (ecpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_ecpgareamultipolygon CHECK ((st_srid(ecpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_ecpgareapolygon CHECK ((st_srid(ecpgareapolygon) = 4326))
);


--
-- Name: TABLE earthquakecatalog; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE earthquakecatalog IS 'Earthquake Catalog';


--
-- Name: COLUMN earthquakecatalog.ecshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecshortname IS 'Catalog short name for reference';


--
-- Name: COLUMN earthquakecatalog.ecname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecname IS 'Earthquake Catalog Long Name for Reference';


--
-- Name: COLUMN earthquakecatalog.ecdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecdesc IS 'Earthquake Catalog Description';


--
-- Name: COLUMN earthquakecatalog.ecformattype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecformattype IS 'Contains format type, i.e. tabular ASCII, ESRI Gis, etc.';


--
-- Name: COLUMN earthquakecatalog.eccattype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.eccattype IS 'Combinations of historical, instumental, synthetic, etc. ';


--
-- Name: COLUMN earthquakecatalog.ecstartdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecstartdate IS 'Start Date';


--
-- Name: COLUMN earthquakecatalog.ecenddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecenddate IS 'End date of Earthquake Catalog';


--
-- Name: COLUMN earthquakecatalog.ectimezone; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ectimezone IS 'Time standard, i.e. GMT, UTC';


--
-- Name: COLUMN earthquakecatalog.eccvrgcd; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.eccvrgcd IS 'If country, then country code; if regional, then region code';


--
-- Name: COLUMN earthquakecatalog.ecorigformatid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecorigformatid IS 'Earthquake Catalog Original Format Id, to refer to another table later';


--
-- Name: COLUMN earthquakecatalog.ecareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN earthquakecatalog.ecareapolygon IS 'Earthquake Catalog Area Polygon, describing area of coverage of earthquatecat';


--
-- Name: earthquakecatalog_ecid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE earthquakecatalog_ecid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: earthquakecatalog_ecid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE earthquakecatalog_ecid_seq OWNED BY earthquakecatalog.ecid;


--
-- Name: econstant; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE econstant (
    eccode character(10) NOT NULL,
    ectypeid integer,
    ecshortname character(20),
    ecname character varying(50),
    ecdesc character varying(100),
    ecremarks character varying(255)
);


--
-- Name: TABLE econstant; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE econstant IS 'Equation Constant';


--
-- Name: COLUMN econstant.eccode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN econstant.eccode IS 'i.e. R, for Distance';


--
-- Name: COLUMN econstant.ectypeid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN econstant.ectypeid IS 'I-Integer, F-float';


--
-- Name: COLUMN econstant.ecshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN econstant.ecshortname IS 'i.e. b';


--
-- Name: COLUMN econstant.ecname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN econstant.ecname IS 'i.e. beta';


--
-- Name: COLUMN econstant.ecremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN econstant.ecremarks IS 'i.e. represents distance from epicenter to ...';


--
-- Name: ecreference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ecreference (
    rlid integer NOT NULL,
    ecid integer NOT NULL,
    eradddate timestamp without time zone
);


--
-- Name: TABLE ecreference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE ecreference IS 'Earthquake Catalog to Reference Literature';


--
-- Name: COLUMN ecreference.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ecreference.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN ecreference.eradddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ecreference.eradddate IS 'Date Added';


--
-- Name: eqcatcompleteness; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE eqcatcompleteness (
    ccid integer NOT NULL,
    cctype character(1),
    ccareapolygon character varying(5120),
    ccareamultipolygon character varying(5120),
    ccstartdate timestamp without time zone,
    ccenddate timestamp without time zone,
    ccmlevel real,
    ecid integer NOT NULL,
    ccpgareapolygon geometry,
    ccpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_ccpgareamultipolygon CHECK ((st_ndims(ccpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_ccpgareapolygon CHECK ((st_ndims(ccpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_ccpgareamultipolygon CHECK (((geometrytype(ccpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (ccpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_ccpgareapolygon CHECK (((geometrytype(ccpgareapolygon) = 'POLYGON'::text) OR (ccpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_ccpgareamultipolygon CHECK ((st_srid(ccpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_ccpgareapolygon CHECK ((st_srid(ccpgareapolygon) = 4326))
);


--
-- Name: TABLE eqcatcompleteness; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE eqcatcompleteness IS 'Earthquake Catalog Completeness Level';


--
-- Name: COLUMN eqcatcompleteness.ccid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.ccid IS 'Earthquake Catalog Completeness Id';


--
-- Name: COLUMN eqcatcompleteness.cctype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.cctype IS 'Earthquake Catalog Completeness Type, i.e. T=Time,R=Region';


--
-- Name: COLUMN eqcatcompleteness.ccareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.ccareapolygon IS 'Earthquake Catalog Completeness Area';


--
-- Name: COLUMN eqcatcompleteness.ccstartdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.ccstartdate IS 'Earthquake Catalog Completeness Start Year';


--
-- Name: COLUMN eqcatcompleteness.ccenddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.ccenddate IS 'Earthquake Catalog Completeness End Year';


--
-- Name: COLUMN eqcatcompleteness.ccmlevel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN eqcatcompleteness.ccmlevel IS 'Earthquake Catalog Completeness Magnitude Level';


--
-- Name: eqcatcompleteness_ccid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE eqcatcompleteness_ccid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: eqcatcompleteness_ccid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE eqcatcompleteness_ccid_seq OWNED BY eqcatcompleteness.ccid;


--
-- Name: seismicsource; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE seismicsource (
    ssid integer NOT NULL,
    sssrctypecode integer,
    ssgeomtypecode integer,
    ssgrdefaulttag boolean,
    ssorigid character(50),
    ssshortname character(20),
    ssname character varying(50),
    ssdesc character varying(100),
    ssremarks character varying(255),
    ssarea double precision,
    ssanormalized double precision,
    ssdepth double precision,
    ssmultilinestring character varying(5120),
    sstopmultilinestring character varying(5120),
    ssbottommultilinestring character varying(5120),
    sspolygon character varying(5120),
    ssmultipolygon character varying(5120),
    sspoint character varying(255),
    ssbackgrdzonetag boolean,
    sserrorcode integer,
    scid integer NOT NULL,
    secode character(10),
    sspgpolygon geometry,
    sspgmultipolygon geometry,
    sspgmultilinestring geometry,
    sspgtopmultilinestring geometry,
    sspgbottommultilinestring geometry,
    sspgpoint geometry,
    CONSTRAINT enforce_dims_sspgbottommultilinestring CHECK ((st_ndims(sspgbottommultilinestring) = 2)),
    CONSTRAINT enforce_dims_sspgmultilinestring CHECK ((st_ndims(sspgmultilinestring) = 2)),
    CONSTRAINT enforce_dims_sspgmultipolygon CHECK ((st_ndims(sspgmultipolygon) = 2)),
    CONSTRAINT enforce_dims_sspgpoint CHECK ((st_ndims(sspgpoint) = 2)),
    CONSTRAINT enforce_dims_sspgpolygon CHECK ((st_ndims(sspgpolygon) = 2)),
    CONSTRAINT enforce_dims_sspgtopmultilinestring CHECK ((st_ndims(sspgtopmultilinestring) = 2)),
    CONSTRAINT enforce_geotype_sspgbottommultilinestring CHECK (((geometrytype(sspgbottommultilinestring) = 'MULTILINESTRING'::text) OR (sspgbottommultilinestring IS NULL))),
    CONSTRAINT enforce_geotype_sspgmultilinestring CHECK (((geometrytype(sspgmultilinestring) = 'MULTILINESTRING'::text) OR (sspgmultilinestring IS NULL))),
    CONSTRAINT enforce_geotype_sspgmultipolygon CHECK (((geometrytype(sspgmultipolygon) = 'MULTIPOLYGON'::text) OR (sspgmultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_sspgpoint CHECK (((geometrytype(sspgpoint) = 'POINT'::text) OR (sspgpoint IS NULL))),
    CONSTRAINT enforce_geotype_sspgpolygon CHECK (((geometrytype(sspgpolygon) = 'POLYGON'::text) OR (sspgpolygon IS NULL))),
    CONSTRAINT enforce_geotype_sspgtopmultilinestring CHECK (((geometrytype(sspgtopmultilinestring) = 'MULTILINESTRING'::text) OR (sspgtopmultilinestring IS NULL))),
    CONSTRAINT enforce_srid_sspgbottommultilinestring CHECK ((st_srid(sspgbottommultilinestring) = 4326)),
    CONSTRAINT enforce_srid_sspgmultilinestring CHECK ((st_srid(sspgmultilinestring) = 4326)),
    CONSTRAINT enforce_srid_sspgmultipolygon CHECK ((st_srid(sspgmultipolygon) = 4326)),
    CONSTRAINT enforce_srid_sspgpoint CHECK ((st_srid(sspgpoint) = 4326)),
    CONSTRAINT enforce_srid_sspgpolygon CHECK ((st_srid(sspgpolygon) = 4326)),
    CONSTRAINT enforce_srid_sspgtopmultilinestring CHECK ((st_srid(sspgtopmultilinestring) = 4326))
);


--
-- Name: TABLE seismicsource; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE seismicsource IS 'Contains Seismic Source Data, Faults, Zones, Gridded Seis, Points';


--
-- Name: COLUMN seismicsource.ssid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssid IS 'Seismic Source Id';


--
-- Name: COLUMN seismicsource.sssrctypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.sssrctypecode IS 'Source Type, 1-fault (usually MULTILINESTRING or multipolygon), 2-Zone (MULTIPOLYGON), 3-Gridded Seis (Point), 4-Seis Point (Point) 5-Subduction zone (top multilinestring, bottom multilinestring)';


--
-- Name: COLUMN seismicsource.ssgeomtypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssgeomtypecode IS '1- Point (grid seis or seismic point), M- multilinestring (fault), 3- multipolygon (zone)';


--
-- Name: COLUMN seismicsource.ssgrdefaulttag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssgrdefaulttag IS 'Gutenberg Richter Default tag, T if default is gutenberg richter, false otherwise';


--
-- Name: COLUMN seismicsource.ssorigid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssorigid IS 'Source Original ID';


--
-- Name: COLUMN seismicsource.ssshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssshortname IS 'Source Short Name';


--
-- Name: COLUMN seismicsource.ssname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssname IS 'Source Name';


--
-- Name: COLUMN seismicsource.ssdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssdesc IS 'Source Description';


--
-- Name: COLUMN seismicsource.ssremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssremarks IS 'Source Remarks';


--
-- Name: COLUMN seismicsource.ssarea; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssarea IS 'Source Area, if multipolygon';


--
-- Name: COLUMN seismicsource.ssanormalized; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssanormalized IS 'Source A normalized';


--
-- Name: COLUMN seismicsource.ssmultilinestring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssmultilinestring IS 'Source Fault multilinestring, if fault';


--
-- Name: COLUMN seismicsource.sstopmultilinestring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.sstopmultilinestring IS 'added 12March 2010';


--
-- Name: COLUMN seismicsource.ssbottommultilinestring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssbottommultilinestring IS 'added 12March 2010';


--
-- Name: COLUMN seismicsource.sspolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.sspolygon IS 'Source Zone Polygon, if source zone';


--
-- Name: COLUMN seismicsource.ssmultipolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssmultipolygon IS 'added 12 Mar 2010, in case there are multipolygons';


--
-- Name: COLUMN seismicsource.sspoint; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.sspoint IS 'Seismic Point, if seismic point or gridded seis, in EWKT';


--
-- Name: COLUMN seismicsource.ssbackgrdzonetag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.ssbackgrdzonetag IS 'Seismic Zone Background tag, if seismic zone';


--
-- Name: COLUMN seismicsource.sserrorcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.sserrorcode IS 'source error code, error encountered during processing of original source catalog';


--
-- Name: COLUMN seismicsource.scid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.scid IS 'Source Geometry Catalog Id';


--
-- Name: COLUMN seismicsource.secode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismicsource.secode IS 'Seismotectonic Environment Id';


--
-- Name: ssourcemfd; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ssourcemfd (
    ssid integer NOT NULL,
    mfdcode character(15) NOT NULL,
    ssmfdseqnum integer NOT NULL,
    ssmfdmagnitudemax double precision,
    ssmfdmagnitudemin double precision,
    ssmfdvala double precision,
    ssmfdvalb double precision,
    ssmfdlambda double precision,
    ssmfdbeta double precision,
    ssmfdvalaorig double precision,
    ssmfdcharmagnitude double precision,
    ssmfdcharrate double precision,
    ssmfdcharmagsd double precision,
    ssmfdtrunclevel double precision,
    ssmfdmodelweight double precision,
    ssmfdmomentrate double precision,
    ssmfdstrike integer,
    ssmfddip integer,
    ssmfdrake integer,
    ssmfddipdirection character(5),
    ssmfddowndipwidth double precision,
    ssmfdtopoffault double precision,
    ssmfdfaultlength double precision,
    ssmfdsliptypecode integer,
    mrrcode character(15),
    ssmfderrorcode integer,
    ssmfdremarks character varying(255),
    ssmfddisctag boolean,
    ssmfddeltamag double precision,
    ssmfdnumintervals integer,
    ssmfddiscvalsstring character varying(2048)
);


--
-- Name: TABLE ssourcemfd; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE ssourcemfd IS 'Seismic Source to MFD';


--
-- Name: COLUMN ssourcemfd.ssid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssid IS 'Seismic Source Id';


--
-- Name: COLUMN ssourcemfd.mfdcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.mfdcode IS 'Magnitude Freq Distn Code';


--
-- Name: COLUMN ssourcemfd.ssmfdseqnum; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdseqnum IS '1= predominant fault, 2 to n= others';


--
-- Name: COLUMN ssourcemfd.ssmfdcharmagnitude; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdcharmagnitude IS 'Seismic source char magnitude for given MFD';


--
-- Name: COLUMN ssourcemfd.ssmfdcharrate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdcharrate IS 'Seismic source char rate for given MFD';


--
-- Name: COLUMN ssourcemfd.ssmfdmodelweight; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdmodelweight IS 'Model Weight, as in USGS NSHM hasfxnga7c.f';


--
-- Name: COLUMN ssourcemfd.ssmfdmomentrate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdmomentrate IS 'Moment Rate, as in USGS NSHM 2008 hazfxnga7c.f';


--
-- Name: COLUMN ssourcemfd.ssmfdstrike; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdstrike IS 'Seismic source strike for given MFD, in degrees';


--
-- Name: COLUMN ssourcemfd.ssmfddip; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfddip IS 'Seismic source dip for given MFD, in degrees';


--
-- Name: COLUMN ssourcemfd.ssmfdrake; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdrake IS 'Seismic source rake for given MFD, in degrees';


--
-- Name: COLUMN ssourcemfd.ssmfddipdirection; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfddipdirection IS 'Seismic source dip direction for given MFD';


--
-- Name: COLUMN ssourcemfd.ssmfddowndipwidth; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfddowndipwidth IS 'Down dip width as in USGS NSHM 2008 hazfxnga7c.f';


--
-- Name: COLUMN ssourcemfd.ssmfdtopoffault; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdtopoffault IS 'Top of Fault as in USGS NSHM 2008 hazfxnga7c.f';


--
-- Name: COLUMN ssourcemfd.ssmfdfaultlength; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdfaultlength IS 'Fault length as in USGS NSHM 2008 hazfxnga7c.f';


--
-- Name: COLUMN ssourcemfd.ssmfdsliptypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfdsliptypecode IS 'Seismic source slip type code for given MFD, 1 - normal, 2-reverse, 3 -strikeslip';


--
-- Name: COLUMN ssourcemfd.mrrcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.mrrcode IS 'Magnitude Rupture Relation Code';


--
-- Name: COLUMN ssourcemfd.ssmfderrorcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfderrorcode IS '1-gr data in a char input, 2-char data in a gr input, 3-new generated mag max < orig mag min';


--
-- Name: COLUMN ssourcemfd.ssmfddeltamag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfddeltamag IS 'Delta/discretization step of magnitude for Gutenberg Richter, USGS NSHM 2008';


--
-- Name: COLUMN ssourcemfd.ssmfddiscvalsstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ssourcemfd.ssmfddiscvalsstring IS 'contains Magnitude, Seis Rate pairs for discrete MFD';


--
-- Name: eugsmodelhan; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW eugsmodelhan AS
    SELECT ss.ssid, ss.ssshortname, ss.sspgpoint, s1.ssmfddeltamag, s1.ssmfdnumintervals, s1.ssmfddiscvalsstring FROM ssourcemfd s1, seismicsource ss WHERE ((ss.ssid = s1.ssid) AND (ss.scid = 3));


--
-- Name: evariable; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE evariable (
    evcode character(10) NOT NULL,
    evtypeid integer,
    evshortname character(20),
    evname character varying(50),
    evdesc character varying(100),
    evremarks character varying(255)
);


--
-- Name: TABLE evariable; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE evariable IS 'Equation Variable';


--
-- Name: COLUMN evariable.evcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN evariable.evcode IS 'i.e. R, for Distance';


--
-- Name: COLUMN evariable.evshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN evariable.evshortname IS 'i.e. r';


--
-- Name: COLUMN evariable.evname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN evariable.evname IS 'i.e. Distance';


--
-- Name: COLUMN evariable.evremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN evariable.evremarks IS 'i.e. represents distance from epicenter to ...';


--
-- Name: event; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE event (
    evid integer NOT NULL,
    evshortname character(20),
    evname character varying(50),
    evdesc character varying(100),
    evorigid character(50),
    evtimestamp timestamp without time zone,
    evyear integer,
    evmonth integer,
    evday integer,
    evhour integer,
    evmin integer,
    evsec integer,
    evnanosec integer,
    evlat double precision,
    evlong double precision,
    evdepth double precision,
    evmagnitude double precision,
    evremarks character varying(255),
    evothdata1 character varying(100),
    evothdata2 character varying(100),
    evref character varying(100),
    everrorcode integer DEFAULT 0,
    evpoint character varying(255),
    ecid integer NOT NULL,
    evpgpoint geometry,
    CONSTRAINT enforce_dims_evpgpoint CHECK ((st_ndims(evpgpoint) = 2)),
    CONSTRAINT enforce_geotype_evpgpoint CHECK (((geometrytype(evpgpoint) = 'POINT'::text) OR (evpgpoint IS NULL))),
    CONSTRAINT enforce_srid_evpgpoint CHECK ((st_srid(evpgpoint) = 4326))
);


--
-- Name: TABLE event; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE event IS 'Contains earthquake events as defined in catalogs';


--
-- Name: COLUMN event.evid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evid IS 'Event id given by system, auto generate?';


--
-- Name: COLUMN event.evshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evshortname IS 'Event Short Name';


--
-- Name: COLUMN event.evname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evname IS 'Event Name';


--
-- Name: COLUMN event.evdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evdesc IS 'Event Description';


--
-- Name: COLUMN event.evorigid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evorigid IS 'Event original id in source catalog';


--
-- Name: COLUMN event.evtimestamp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evtimestamp IS 'Event Date and Time in UTC Standard Time';


--
-- Name: COLUMN event.evhour; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evhour IS '24 hour time';


--
-- Name: COLUMN event.evlat; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evlat IS 'Event Latitude';


--
-- Name: COLUMN event.evlong; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evlong IS 'Event Longitude';


--
-- Name: COLUMN event.evdepth; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evdepth IS 'Depth of Given Event';


--
-- Name: COLUMN event.evmagnitude; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evmagnitude IS 'Magnitude of the Event';


--
-- Name: COLUMN event.evremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evremarks IS 'Remarks regarding event, i.e. other info ';


--
-- Name: COLUMN event.evothdata1; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evothdata1 IS 'Data relating to event';


--
-- Name: COLUMN event.evothdata2; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evothdata2 IS 'Other data relating to event';


--
-- Name: COLUMN event.evref; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.evref IS 'Other event reference info';


--
-- Name: COLUMN event.everrorcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN event.everrorcode IS 'Event possible error code, 0- no error, 1-incomplete date, 2-incomplete time';


--
-- Name: event_evid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE event_evid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: event_evid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE event_evid_seq OWNED BY event.evid;


--
-- Name: gefeaturevalue; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gefeaturevalue (
    gfcode character(10) NOT NULL,
    gecode character(10) NOT NULL,
    gefvalstring character(50),
    gefremarks character varying(255)
);


--
-- Name: TABLE gefeaturevalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gefeaturevalue IS 'GMPE Feature Value';


--
-- Name: COLUMN gefeaturevalue.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gefeaturevalue.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gefeaturevalue.gefvalstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gefeaturevalue.gefvalstring IS 'GMPE Feature Value String';


--
-- Name: gemsesame; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gemsesame (
    gid integer NOT NULL,
    title character varying(10),
    the_geom geometry,
    CONSTRAINT enforce_dims_the_geom CHECK ((st_ndims(the_geom) = 2)),
    CONSTRAINT enforce_geotype_the_geom CHECK (((geometrytype(the_geom) = 'MULTIPOLYGON'::text) OR (the_geom IS NULL))),
    CONSTRAINT enforce_srid_the_geom CHECK ((st_srid(the_geom) = 4326))
);


--
-- Name: gemsesame_gid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE gemsesame_gid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: gemsesame_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE gemsesame_gid_seq OWNED BY gemsesame.gid;


--
-- Name: geography_columns; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW geography_columns AS
    SELECT current_database() AS f_table_catalog, n.nspname AS f_table_schema, c.relname AS f_table_name, a.attname AS f_geography_column, geography_typmod_dims(a.atttypmod) AS coord_dimension, geography_typmod_srid(a.atttypmod) AS srid, geography_typmod_type(a.atttypmod) AS type FROM pg_class c, pg_attribute a, pg_type t, pg_namespace n WHERE ((((((c.relkind = ANY (ARRAY['r'::"char", 'v'::"char"])) AND (t.typname = 'geography'::name)) AND (a.attisdropped = false)) AND (a.atttypid = t.oid)) AND (a.attrelid = c.oid)) AND (c.relnamespace = n.oid));


SET default_with_oids = true;

--
-- Name: geometry_columns; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE geometry_columns (
    f_table_catalog character varying(256) NOT NULL,
    f_table_schema character varying(256) NOT NULL,
    f_table_name character varying(256) NOT NULL,
    f_geometry_column character varying(256) NOT NULL,
    coord_dimension integer NOT NULL,
    srid integer NOT NULL,
    type character varying(30) NOT NULL
);


SET default_with_oids = false;

--
-- Name: geopoint; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE geopoint (
    gpid integer NOT NULL,
    gppoint character(255),
    gpname character varying(50),
    gpdesc character varying(100),
    sacode character(10),
    socode character(10),
    gppgpoint geometry,
    CONSTRAINT enforce_dims_gppgpoint CHECK ((st_ndims(gppgpoint) = 2)),
    CONSTRAINT enforce_geotype_gppgpoint CHECK (((geometrytype(gppgpoint) = 'POINT'::text) OR (gppgpoint IS NULL))),
    CONSTRAINT enforce_srid_gppgpoint CHECK ((st_srid(gppgpoint) = 4326))
);


--
-- Name: TABLE geopoint; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE geopoint IS 'Geographic Point Object';


--
-- Name: COLUMN geopoint.gppoint; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN geopoint.gppoint IS 'Geographic Point, longitude, latitude';


--
-- Name: COLUMN geopoint.gpname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN geopoint.gpname IS 'Geographic Point Name';


--
-- Name: COLUMN geopoint.gpdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN geopoint.gpdesc IS 'GeographicPoint Description';


--
-- Name: COLUMN geopoint.sacode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN geopoint.sacode IS 'Site Amplification Id, i.e. SOFTROCK';


--
-- Name: COLUMN geopoint.socode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN geopoint.socode IS 'SIA 261 classification values, A to E, F1, F2';


--
-- Name: geopoint_gpid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE geopoint_gpid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: geopoint_gpid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE geopoint_gpid_seq OWNED BY geopoint.gpid;


--
-- Name: gereference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gereference (
    rlid integer NOT NULL,
    gecode character(10) NOT NULL,
    gradddate timestamp without time zone
);


--
-- Name: TABLE gereference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gereference IS 'GMPE to Reference Literature';


--
-- Name: COLUMN gereference.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gereference.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN gereference.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gereference.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gereference.gradddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gereference.gradddate IS 'GMPE-Reference Lit Date Added';


--
-- Name: gfz_europe_sourcemodel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW gfz_europe_sourcemodel AS
    SELECT ss.ssid, ss.ssshortname, sm.ssmfdvalb, ss.ssdepth, sm.ssmfdlambda, sm.ssmfdmagnitudemax AS magmax, sm.ssmfdmagnitudemin AS magmin, ss.sspgmultipolygon, ss.ssmultipolygon FROM seismicsource ss, ssourcemfd sm WHERE ((ss.ssid = sm.ssid) AND (ss.scid = 2));


--
-- Name: gfzeuropesrcmodel; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW gfzeuropesrcmodel AS
    SELECT ss.ssid, ss.ssshortname, sm.ssmfdvalb, ss.ssdepth, sm.ssmfdlambda, sm.ssmfdmagnitudemax AS magmax, sm.ssmfdmagnitudemin AS magmin, ss.sspgmultipolygon, ss.ssmultipolygon FROM seismicsource ss, ssourcemfd sm WHERE ((ss.ssid = sm.ssid) AND (ss.scid = 2));


--
-- Name: gmeconstant; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmeconstant (
    gecode character(10) NOT NULL,
    eccode character(10) NOT NULL,
    gmecvalue character(20),
    gmecremarks character varying(255)
);


--
-- Name: TABLE gmeconstant; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmeconstant IS 'GMPE Constant';


--
-- Name: COLUMN gmeconstant.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmeconstant.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gmeconstant.eccode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmeconstant.eccode IS 'i.e. R, for Distance';


--
-- Name: COLUMN gmeconstant.gmecvalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmeconstant.gmecvalue IS 'Value of constant, i.e. 1.0';


--
-- Name: gmevariable; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmevariable (
    gecode character(10) NOT NULL,
    evcode character(10) NOT NULL,
    gmevremarks character varying(255)
);


--
-- Name: TABLE gmevariable; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmevariable IS 'GMPE Variable';


--
-- Name: COLUMN gmevariable.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmevariable.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gmevariable.evcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmevariable.evcode IS 'i.e. R, for Distance';


--
-- Name: gmparamvalue; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmparamvalue (
    gpcode character(10) NOT NULL,
    gecode character(10) NOT NULL,
    gepvalstring character(50),
    gepremarks character varying(255)
);


--
-- Name: TABLE gmparamvalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmparamvalue IS 'GMPE Parameter Value';


--
-- Name: COLUMN gmparamvalue.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmparamvalue.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gmparamvalue.gepvalstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmparamvalue.gepvalstring IS 'GMPE Parameter Value String';


--
-- Name: gmpe; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmpe (
    gecode character(10) NOT NULL,
    geprivatetag boolean,
    geshortname character(20),
    gename character varying(50),
    gedesc character varying(100),
    geremarks character varying(255),
    geequation character varying(5120),
    geeqndbdefntag boolean,
    geeqntypecode character(1),
    geareapolygon character varying(5120),
    geareamultipolygon character varying(5120),
    secode character(10) NOT NULL,
    gepgareapolygon geometry,
    gepgareamultipolygon geometry,
    CONSTRAINT enforce_dims_gepgareamultipolygon CHECK ((st_ndims(gepgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_gepgareapolygon CHECK ((st_ndims(gepgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_gepgareamultipolygon CHECK (((geometrytype(gepgareamultipolygon) = 'MULTIPOLYGON'::text) OR (gepgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_gepgareapolygon CHECK (((geometrytype(gepgareapolygon) = 'POLYGON'::text) OR (gepgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_gepgareamultipolygon CHECK ((st_srid(gepgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_gepgareapolygon CHECK ((st_srid(gepgareapolygon) = 4326))
);


--
-- Name: TABLE gmpe; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmpe IS 'Ground Motion Prediction Equation';


--
-- Name: COLUMN gmpe.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.gecode IS 'ex. AT08, etc';


--
-- Name: COLUMN gmpe.gename; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.gename IS 'GMPE Short Name';


--
-- Name: COLUMN gmpe.gedesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.gedesc IS 'GMPE Description';


--
-- Name: COLUMN gmpe.geremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.geremarks IS 'GMPE Remarks';


--
-- Name: COLUMN gmpe.geequation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.geequation IS 'GMPE Equation in functional format';


--
-- Name: COLUMN gmpe.geeqndbdefntag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.geeqndbdefntag IS 'True, if defined in db (standard format), False - not defined';


--
-- Name: COLUMN gmpe.geeqntypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.geeqntypecode IS 'Ground Motion Prediction Equation  Type, i.e. Standard=3 constants, 3 vars; other=see vars, const';


--
-- Name: COLUMN gmpe.geareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.geareapolygon IS 'Describes area of polygon okay for GMPE';


--
-- Name: COLUMN gmpe.secode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpe.secode IS 'Seismotectonic Environment Id';


--
-- Name: gmpefeature; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmpefeature (
    gfcode character(10) NOT NULL,
    gftypeid integer,
    gfpossvalstring character varying(2048),
    gfshortname character(20),
    gfname character varying(50),
    gfdesc character varying(100),
    gfremarks character varying(255)
);


--
-- Name: TABLE gmpefeature; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmpefeature IS 'Features of particular GMPEs (for info only)';


--
-- Name: COLUMN gmpefeature.gfshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpefeature.gfshortname IS 'ex. H = number of Horiz records (refer: selection of GMPEs for GEM1)';


--
-- Name: gmpeparameter; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gmpeparameter (
    gpcode character(10) NOT NULL,
    gptypeid integer,
    gppossvalstring character varying(2048),
    gpshortname character(20),
    gpname character varying(50),
    gpdesc character varying(100),
    gpremarks character varying(255)
);


--
-- Name: TABLE gmpeparameter; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE gmpeparameter IS 'Parameters of particular GMPEs (for setting defaults)';


--
-- Name: COLUMN gmpeparameter.gpshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN gmpeparameter.gpshortname IS 'ex. GAUSSTRUNC';


--
-- Name: hazardpointvalue; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardpointvalue (
    hpid integer NOT NULL,
    hpvalue double precision,
    hpexceedprob double precision,
    hpexceedyears integer,
    hcid integer NOT NULL,
    gpid integer NOT NULL,
    imcode character(10) NOT NULL
);


--
-- Name: TABLE hazardpointvalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardpointvalue IS 'Hazard Point Values contained in Hazard Map';


--
-- Name: COLUMN hazardpointvalue.hpid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardpointvalue.hpid IS 'Hazard Point Sequence Id, just a sequence number for reference, order unimportant';


--
-- Name: COLUMN hazardpointvalue.hpexceedprob; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardpointvalue.hpexceedprob IS 'Exceedance Proby Pct, the 2 in "2% in 50 years" or the annual proby of exceedance for hazard curves (.133544 in 1 year)';


--
-- Name: COLUMN hazardpointvalue.hcid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardpointvalue.hcid IS 'Hazard Calculation Id';


--
-- Name: COLUMN hazardpointvalue.imcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardpointvalue.imcode IS 'Intensity Measure TType Id';


--
-- Name: hanhazmap; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW hanhazmap AS
    SELECT h.hpid, h.gpid, g.gppgpoint, g.gppoint, h.hpvalue, h.hpexceedprob AS hpexceedprobpct, h.hpexceedyears, h.hcid FROM hazardpointvalue h, geopoint g WHERE ((h.hcid = 27) AND (h.gpid = g.gpid));


--
-- Name: hazardcalculation; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardcalculation (
    hcid integer NOT NULL,
    hcshortname character(20),
    hcname character varying(50),
    hcdesc character varying(100),
    hcstarttimestamp timestamp without time zone,
    hcendtimestamp timestamp without time zone,
    hcprobdettag character(1),
    hcgemgentag boolean,
    hcareapolygon character varying(5120),
    hcareamultipolygon character varying(5120),
    hcremarks character varying(255),
    hibmid integer,
    hilmid integer,
    hilmpid integer,
    evid integer,
    hscode character(10) NOT NULL,
    cocode character(10) NOT NULL,
    hcpgareapolygon geometry,
    hcpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_hcpgareamultipolygon CHECK ((st_ndims(hcpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_hcpgareapolygon CHECK ((st_ndims(hcpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_hcpgareamultipolygon CHECK (((geometrytype(hcpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (hcpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_hcpgareapolygon CHECK (((geometrytype(hcpgareapolygon) = 'POLYGON'::text) OR (hcpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_hcpgareamultipolygon CHECK ((st_srid(hcpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_hcpgareapolygon CHECK ((st_srid(hcpgareapolygon) = 4326))
);


--
-- Name: TABLE hazardcalculation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardcalculation IS 'Hazard Calculation';


--
-- Name: COLUMN hazardcalculation.hcid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcid IS 'Hazard Calculation Id';


--
-- Name: COLUMN hazardcalculation.hcshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcshortname IS 'Hazard Calc Short Name';


--
-- Name: COLUMN hazardcalculation.hcname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcname IS 'Hazard Calc Short Name';


--
-- Name: COLUMN hazardcalculation.hcdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcdesc IS 'Hazard Calc Description';


--
-- Name: COLUMN hazardcalculation.hcstarttimestamp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcstarttimestamp IS 'Date when Hazard Calculation made, TimeStamp without TimeZone';


--
-- Name: COLUMN hazardcalculation.hcprobdettag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcprobdettag IS 'Hazard Calculation Probabilistic Deterministic Tag, ''P'' or ''T''';


--
-- Name: COLUMN hazardcalculation.hcgemgentag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcgemgentag IS 'Hazard Calculation GEM Generated Tag, true (generated by GEM) or false (previously generated)';


--
-- Name: COLUMN hazardcalculation.hcareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcareapolygon IS 'Hazard Calculation Area Polygon';


--
-- Name: COLUMN hazardcalculation.hcareamultipolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcareamultipolygon IS 'Added 12 Mar 2010';


--
-- Name: COLUMN hazardcalculation.hcremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hcremarks IS 'Hazard Calculation Remarks';


--
-- Name: COLUMN hazardcalculation.evid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.evid IS 'Event id given by system, auto generate?';


--
-- Name: COLUMN hazardcalculation.hscode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.hscode IS 'Hazard Software Code';


--
-- Name: COLUMN hazardcalculation.cocode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcalculation.cocode IS 'Calculation Owner Code';


--
-- Name: hazardcalculation_hcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardcalculation_hcid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardcalculation_hcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardcalculation_hcid_seq OWNED BY hazardcalculation.hcid;


--
-- Name: hazardcurve; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardcurve (
    hcrvid integer NOT NULL,
    hcrvshortname character(20),
    hcrvname character varying(50),
    hcrvdesc character varying(100),
    hcrvtimestamp timestamp without time zone,
    hcrvmingrdmotion double precision,
    hcrvmaxgrdmotion double precision,
    hcrvtimeperiod integer,
    hcrvsadamping double precision,
    hcrvsaperiod integer,
    hcrvremarks character varying(255),
    hcid integer,
    gpid integer NOT NULL,
    imcode character(10) NOT NULL
);


--
-- Name: TABLE hazardcurve; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardcurve IS 'Hazard Curve, may be generated by Hazard Calc or from other source';


--
-- Name: COLUMN hazardcurve.hcrvid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvid IS 'Hazard Curve Id';


--
-- Name: COLUMN hazardcurve.hcrvshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvshortname IS 'Hazard Curve shortname';


--
-- Name: COLUMN hazardcurve.hcrvname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvname IS 'Hazard curve Name';


--
-- Name: COLUMN hazardcurve.hcrvdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvdesc IS 'Hazard Curve Description';


--
-- Name: COLUMN hazardcurve.hcrvtimestamp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvtimestamp IS 'Hazard Curve Time Stamp';


--
-- Name: COLUMN hazardcurve.hcrvsadamping; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvsadamping IS 'Hazard Curve Spectral Acceleration Damping Value';


--
-- Name: COLUMN hazardcurve.hcrvsaperiod; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvsaperiod IS 'Hazard Curve Spectral Acceleration Period';


--
-- Name: COLUMN hazardcurve.hcrvremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcrvremarks IS 'Hazard curve Remarks';


--
-- Name: COLUMN hazardcurve.hcid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.hcid IS 'Hazard Calculation Id, the corresponding HCID if system generated';


--
-- Name: COLUMN hazardcurve.imcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardcurve.imcode IS 'Intensity Measure TType Id';


--
-- Name: hazardcurve_hcrvid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardcurve_hcrvid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardcurve_hcrvid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardcurve_hcrvid_seq OWNED BY hazardcurve.hcrvid;


--
-- Name: hazardinputbasicmodel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardinputbasicmodel (
    hibmid integer NOT NULL,
    hibmshortname character(20),
    hibmname character varying(50),
    hibmdesc character varying(100),
    hibmremarks character varying(255),
    hibmcvrgtypecode character(1),
    hibmareapolygon character varying(5120),
    hibmareamultipolygon character varying(5120),
    scid integer,
    hibmpgareapolygon geometry,
    hibmpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_hibmpgareamultipolygon CHECK ((st_ndims(hibmpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_hibmpgareapolygon CHECK ((st_ndims(hibmpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_hibmpgareamultipolygon CHECK (((geometrytype(hibmpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (hibmpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_hibmpgareapolygon CHECK (((geometrytype(hibmpgareapolygon) = 'POLYGON'::text) OR (hibmpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_hibmpgareamultipolygon CHECK ((st_srid(hibmpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_hibmpgareapolygon CHECK ((st_srid(hibmpgareapolygon) = 4326))
);


--
-- Name: TABLE hazardinputbasicmodel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardinputbasicmodel IS 'Hazard Input Model/ Earthquake Rupture Forecast Input Model';


--
-- Name: COLUMN hazardinputbasicmodel.hibmname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.hibmname IS 'i.e. Abrahamson etc';


--
-- Name: COLUMN hazardinputbasicmodel.hibmdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.hibmdesc IS 'Hazard Input Model Description';


--
-- Name: COLUMN hazardinputbasicmodel.hibmremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.hibmremarks IS 'Hazard Input Basic Model Remarks';


--
-- Name: COLUMN hazardinputbasicmodel.hibmcvrgtypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.hibmcvrgtypecode IS 'Hazard Input Basic Coverage Type, 1- all, 2- area, 3-chosen sources';


--
-- Name: COLUMN hazardinputbasicmodel.hibmareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.hibmareapolygon IS 'area polygon for computation';


--
-- Name: COLUMN hazardinputbasicmodel.scid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputbasicmodel.scid IS 'Source Geometry Catalog Id';


--
-- Name: hazardinputbasicmodel_hibmid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardinputbasicmodel_hibmid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardinputbasicmodel_hibmid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardinputbasicmodel_hibmid_seq OWNED BY hazardinputbasicmodel.hibmid;


--
-- Name: hazardinputltreemodel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardinputltreemodel (
    hilmid integer NOT NULL,
    hilmshortname character(20),
    hilmname character varying(50),
    hilmdesc character varying(100),
    hilmremarks character varying(255),
    hilmcvrgtypecode integer,
    hilmareapolygon character varying(5120),
    hilmareamultipolygon character varying(5120),
    ltsid integer NOT NULL,
    hilmpgareapolygon geometry,
    hilmpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_hilmpgareamultipolygon CHECK ((st_ndims(hilmpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_hilmpgareapolygon CHECK ((st_ndims(hilmpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_hilmpgareamultipolygon CHECK (((geometrytype(hilmpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (hilmpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_hilmpgareapolygon CHECK (((geometrytype(hilmpgareapolygon) = 'POLYGON'::text) OR (hilmpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_hilmpgareamultipolygon CHECK ((st_srid(hilmpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_hilmpgareapolygon CHECK ((st_srid(hilmpgareapolygon) = 4326))
);


--
-- Name: TABLE hazardinputltreemodel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardinputltreemodel IS 'Hazard Input Model/ Earthquake Rupture Forecast Input with Logic Tree Model';


--
-- Name: COLUMN hazardinputltreemodel.hilmshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputltreemodel.hilmshortname IS 'Hazard Input Logic Tree Short Name';


--
-- Name: COLUMN hazardinputltreemodel.hilmdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputltreemodel.hilmdesc IS 'Hazard Input Model Description';


--
-- Name: COLUMN hazardinputltreemodel.hilmremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputltreemodel.hilmremarks IS 'Hazard Input Logic Tree Model Remarks';


--
-- Name: COLUMN hazardinputltreemodel.hilmcvrgtypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputltreemodel.hilmcvrgtypecode IS '1- all sources, 2-area of sources, 3 - chosen sources';


--
-- Name: COLUMN hazardinputltreemodel.hilmareamultipolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardinputltreemodel.hilmareamultipolygon IS 'Added 12 Mar 2010';


--
-- Name: hazardinputltreemodel_hilmid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardinputltreemodel_hilmid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardinputltreemodel_hilmid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardinputltreemodel_hilmid_seq OWNED BY hazardinputltreemodel.hilmid;


--
-- Name: hazardmap; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardmap (
    hmapid integer NOT NULL,
    hmapshortname character(20),
    hmapname character varying(50),
    hmapdesc character varying(100),
    hmaptimestamp timestamp without time zone,
    hmaptimedepstartdate timestamp without time zone,
    hmaptimedependdate timestamp without time zone,
    hmapexceedprob double precision,
    hmapexceedyears integer,
    hmapdamping integer,
    hmapgridsize real,
    hmapremarks character varying(255),
    hmapwms character varying(256),
    hcid integer,
    imcode character(10) NOT NULL
);


--
-- Name: TABLE hazardmap; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardmap IS 'Hazard Map, may be generated by Hazard Calc or from other source';


--
-- Name: COLUMN hazardmap.hmapid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapid IS 'Hazard Map Id';


--
-- Name: COLUMN hazardmap.hmapshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapshortname IS 'Hazard Map shortname';


--
-- Name: COLUMN hazardmap.hmapname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapname IS 'Hazard Map Name';


--
-- Name: COLUMN hazardmap.hmapdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapdesc IS 'Hazard Map Description';


--
-- Name: COLUMN hazardmap.hmaptimestamp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmaptimestamp IS 'Hazard Map Time Stamp- - for Time Dependent Hazard Map Tag';


--
-- Name: COLUMN hazardmap.hmaptimedepstartdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmaptimedepstartdate IS 'Hazard Map Time-dependent Start Date';


--
-- Name: COLUMN hazardmap.hmaptimedependdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmaptimedependdate IS 'Hazard Map Time-dependent End Date';


--
-- Name: COLUMN hazardmap.hmapexceedprob; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapexceedprob IS 'Hazard Map Exceedance Probability, i.e. the 10% in "10% in 50 years"';


--
-- Name: COLUMN hazardmap.hmapexceedyears; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapexceedyears IS 'Hazard Map Exceedance Years Value, i.e. the 50 years in "10% in 50 years"';


--
-- Name: COLUMN hazardmap.hmapdamping; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapdamping IS 'Hazard Map Damping Value, , i.e. 5% damping';


--
-- Name: COLUMN hazardmap.hmapgridsize; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapgridsize IS 'Hazard Map Grid Size Longitude/Latitude, i.e. 0.1';


--
-- Name: COLUMN hazardmap.hmapremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapremarks IS 'Hazard Map Remarks';


--
-- Name: COLUMN hazardmap.hmapwms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hmapwms IS 'Hazard Map WMS for storing WMS URL';


--
-- Name: COLUMN hazardmap.hcid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.hcid IS 'Hazard Calculation Id, the corresponding HCID if system generated';


--
-- Name: COLUMN hazardmap.imcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardmap.imcode IS 'Intensity Measure TType Id';


--
-- Name: hazardmap_hmapid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardmap_hmapid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardmap_hmapid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardmap_hmapid_seq OWNED BY hazardmap.hmapid;


--
-- Name: hazardpointvalue_hpid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hazardpointvalue_hpid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hazardpointvalue_hpid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hazardpointvalue_hpid_seq OWNED BY hazardpointvalue.hpid;


--
-- Name: hazardsoftware; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hazardsoftware (
    hscode character(10) NOT NULL,
    hsname character varying(50),
    hsdesc character varying(100),
    hsadddate timestamp without time zone,
    hsremarks character varying(255)
);


--
-- Name: TABLE hazardsoftware; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hazardsoftware IS 'Hazard Calculation Software';


--
-- Name: COLUMN hazardsoftware.hscode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardsoftware.hscode IS 'Hazard Software Code';


--
-- Name: COLUMN hazardsoftware.hsname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hazardsoftware.hsname IS 'Hazard Calculation Software Name';


--
-- Name: hibmge; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hibmge (
    hibmid integer NOT NULL,
    gecode character(10) NOT NULL,
    hibmgeweight double precision
);


--
-- Name: TABLE hibmge; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hibmge IS 'Hazard Input Basic Model to GMPE';


--
-- Name: COLUMN hibmge.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hibmge.gecode IS 'ex. AT08, etc';


--
-- Name: hibmreference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hibmreference (
    rlid integer NOT NULL,
    hibmid integer NOT NULL,
    hibmradddate timestamp without time zone
);


--
-- Name: TABLE hibmreference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hibmreference IS 'Hazard Input Model  to Reference Literature';


--
-- Name: COLUMN hibmreference.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hibmreference.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN hibmreference.hibmradddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hibmreference.hibmradddate IS 'Hazard Input Model - Ref Lit Date Added';


--
-- Name: hilmpath; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hilmpath (
    hilmpid integer NOT NULL,
    hilmppathstring character varying(5120),
    hilmpfinalpathtag boolean,
    hilmid integer NOT NULL,
    hilmpweight double precision,
    hilmpshortname character(20),
    hilmpname character varying(50),
    hilmpdesc character varying(100),
    hilmpremarks character varying(255),
    scid integer,
    hilmpltree ltree
);


--
-- Name: TABLE hilmpath; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hilmpath IS 'Paths corresponding to Ltree';


--
-- Name: COLUMN hilmpath.hilmppathstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmpath.hilmppathstring IS 'format paramtype_paramval_probval.paramtype_paramval_probval, for parsing';


--
-- Name: COLUMN hilmpath.hilmpfinalpathtag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmpath.hilmpfinalpathtag IS 'Tags the final logic tree tag, t-if final logic tree, ready for calc, f - if not';


--
-- Name: COLUMN hilmpath.scid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmpath.scid IS 'Source Geometry Catalog Id';


--
-- Name: hilmpath_hilmpid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hilmpath_hilmpid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hilmpath_hilmpid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hilmpath_hilmpid_seq OWNED BY hilmpath.hilmpid;


--
-- Name: hilmpge; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hilmpge (
    hilmpid integer NOT NULL,
    gecode character(10) NOT NULL,
    hilmpgeweight double precision
);


--
-- Name: TABLE hilmpge; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hilmpge IS 'Hazard Input Logic Tree Model to GMPE';


--
-- Name: COLUMN hilmpge.gecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmpge.gecode IS 'ex. AT08, etc';


--
-- Name: hilmreference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hilmreference (
    rlid integer NOT NULL,
    hilmid integer NOT NULL,
    hilmradddate timestamp without time zone
);


--
-- Name: TABLE hilmreference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hilmreference IS 'Hazard Input Logic Tree Model  to Reference Literature';


--
-- Name: COLUMN hilmreference.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmreference.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN hilmreference.hilmradddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmreference.hilmradddate IS 'Hazard Input Model - Ref Lit Date Added';


--
-- Name: hilmruleset; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hilmruleset (
    hilmrid integer NOT NULL,
    hilmrcvrgtypecode integer,
    hilmractiontypecode integer,
    hilmrvalstring character(100),
    hilmrprobpctstring character(10),
    ltptid integer NOT NULL,
    ltpvid integer NOT NULL,
    hilmid integer NOT NULL
);


--
-- Name: TABLE hilmruleset; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE hilmruleset IS 'Hazard Input Logic Tree Model Ruleset';


--
-- Name: COLUMN hilmruleset.hilmrcvrgtypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmruleset.hilmrcvrgtypecode IS '1-all sources, 2-area, 3-some sources';


--
-- Name: COLUMN hilmruleset.hilmractiontypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmruleset.hilmractiontypecode IS '0- do nothing, 1-Replace, 2- Add';


--
-- Name: COLUMN hilmruleset.hilmrvalstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmruleset.hilmrvalstring IS 'the value that will replace orig value or be added to orig value';


--
-- Name: COLUMN hilmruleset.hilmrprobpctstring; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmruleset.hilmrprobpctstring IS 'write 02 for 0.2, 0333 for 0.333';


--
-- Name: COLUMN hilmruleset.ltpvid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN hilmruleset.ltpvid IS 'Logic Tree Parameter Type Id';


--
-- Name: hilmruleset_hilmrid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE hilmruleset_hilmrid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: hilmruleset_hilmrid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE hilmruleset_hilmrid_seq OWNED BY hilmruleset.hilmrid;


--
-- Name: intensitymeasuretype; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE intensitymeasuretype (
    imcode character(10) NOT NULL,
    imname character varying(50),
    imdesc character varying(100),
    imvaluemin double precision,
    imvaluemax double precision,
    imunittype character(10),
    imunitdescr character varying(100),
    imremarks character varying(255)
);


--
-- Name: TABLE intensitymeasuretype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE intensitymeasuretype IS 'Intensity Measure Type';


--
-- Name: COLUMN intensitymeasuretype.imcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imcode IS 'Intensity Measure TType Id';


--
-- Name: COLUMN intensitymeasuretype.imname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imname IS 'Intensity MeasureType Name, i.e. PGA, PGV, SA1HZ, SA3HZ, SA5HZ (Spectral Acceleration at:  5hz, 0.2secs; 3.33hz,0.3sec;1hz,1 sec), MMI';


--
-- Name: COLUMN intensitymeasuretype.imdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imdesc IS 'Intensity Measure Type Description, i.e. PGA, PGV, Spectral Acceleration at:  5hz, 0.2secs; 3.33hz,0.3sec;1hz,1 sec)';


--
-- Name: COLUMN intensitymeasuretype.imvaluemin; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imvaluemin IS 'Intensity Measure Type Minimum Value';


--
-- Name: COLUMN intensitymeasuretype.imvaluemax; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imvaluemax IS 'Intensity Measure Type Maximum Value';


--
-- Name: COLUMN intensitymeasuretype.imunittype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN intensitymeasuretype.imunittype IS 'Intensity Measure Type Units';


--
-- Name: logictreestruc; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE logictreestruc (
    ltsid integer NOT NULL,
    ltsshortname character(20),
    ltsname character varying(50),
    ltsdesc character varying(100),
    ltsremarks character varying(255),
    ltsnumlevels integer
);


--
-- Name: TABLE logictreestruc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE logictreestruc IS 'Logic Tree Structure';


--
-- Name: COLUMN logictreestruc.ltsdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN logictreestruc.ltsdesc IS 'Logic Tree Structure Description';


--
-- Name: logictreestruc_ltsid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE logictreestruc_ltsid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: logictreestruc_ltsid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE logictreestruc_ltsid_seq OWNED BY logictreestruc.ltsid;


--
-- Name: ltreeparamtype; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ltreeparamtype (
    ltptid integer NOT NULL,
    ltptshortname character(20),
    ltptname character varying(50),
    ltptdesc character varying(100),
    ltptdatatypecode integer,
    ltptpossvalstring character(2048),
    ltptvaluemin double precision,
    ltptvaluemax double precision,
    ltptmapping character varying(255),
    ltptremarks character varying(255)
);


--
-- Name: TABLE ltreeparamtype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE ltreeparamtype IS 'Logic Tree Parameter Type';


--
-- Name: COLUMN ltreeparamtype.ltptdatatypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtype.ltptdatatypecode IS 'for info only, to do value replacement/computation if needed';


--
-- Name: COLUMN ltreeparamtype.ltptvaluemin; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtype.ltptvaluemin IS 'for range checking';


--
-- Name: COLUMN ltreeparamtype.ltptvaluemax; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtype.ltptvaluemax IS 'for range checking';


--
-- Name: COLUMN ltreeparamtype.ltptmapping; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtype.ltptmapping IS 'for implementation later';


--
-- Name: ltreeparamtype_ltptid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE ltreeparamtype_ltptid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: ltreeparamtype_ltptid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE ltreeparamtype_ltptid_seq OWNED BY ltreeparamtype.ltptid;


--
-- Name: ltreeparamtypelevel; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ltreeparamtypelevel (
    ltptid integer NOT NULL,
    ltsid integer NOT NULL,
    ltptlevel integer,
    ltptnumbranches integer,
    ltptbranchsettag boolean
);


--
-- Name: TABLE ltreeparamtypelevel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE ltreeparamtypelevel IS 'Logic Tree Parameter Type Level';


--
-- Name: COLUMN ltreeparamtypelevel.ltptlevel; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtypelevel.ltptlevel IS 'Logic Tree Parameter Type Level';


--
-- Name: COLUMN ltreeparamtypelevel.ltptbranchsettag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamtypelevel.ltptbranchsettag IS 'True-default all param values set in level, false-otherwise';


--
-- Name: ltreeparamvalue; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE ltreeparamvalue (
    ltpvid integer NOT NULL,
    ltpvshortname character(15),
    ltpvname character varying(50),
    ltpvdesc character varying(100),
    ltpvremarks character varying(255),
    ltptid integer NOT NULL
);


--
-- Name: TABLE ltreeparamvalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE ltreeparamvalue IS 'Logic Tree Parameter Value';


--
-- Name: COLUMN ltreeparamvalue.ltpvid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamvalue.ltpvid IS 'Logic Tree Parameter Type Id';


--
-- Name: COLUMN ltreeparamvalue.ltpvname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN ltreeparamvalue.ltpvname IS 'Logic Tree Parameter Value Name';


--
-- Name: ltreeparamvalue_ltpvid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE ltreeparamvalue_ltpvid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: ltreeparamvalue_ltpvid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE ltreeparamvalue_ltpvid_seq OWNED BY ltreeparamvalue.ltpvid;


--
-- Name: magfreqdistn; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE magfreqdistn (
    mfdcode character(15) NOT NULL,
    mfdname character varying(50),
    mfddesc character varying(100),
    mfdremarks character varying(255),
    mfddisctag boolean
);


--
-- Name: TABLE magfreqdistn; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE magfreqdistn IS 'Magnitude Frequency Distn';


--
-- Name: COLUMN magfreqdistn.mfdcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magfreqdistn.mfdcode IS 'Magnitude Freq Distn Code';


--
-- Name: COLUMN magfreqdistn.mfdname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magfreqdistn.mfdname IS 'Magnitude Freq Distn Name';


--
-- Name: COLUMN magfreqdistn.mfddesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magfreqdistn.mfddesc IS 'Magnitude Freq Distn Description';


--
-- Name: COLUMN magfreqdistn.mfdremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magfreqdistn.mfdremarks IS 'Magnitude Freq Distn Remarks';


--
-- Name: COLUMN magfreqdistn.mfddisctag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magfreqdistn.mfddisctag IS 'default is false';


--
-- Name: magrupturerelation; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE magrupturerelation (
    mrrcode character(15) NOT NULL,
    mrrname character varying(50),
    mrrdesc character varying(100),
    mrrremarks character varying(255)
);


--
-- Name: TABLE magrupturerelation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE magrupturerelation IS 'Magnitude Rupture Relation';


--
-- Name: COLUMN magrupturerelation.mrrcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magrupturerelation.mrrcode IS 'Magnitude Rupture Relation Code';


--
-- Name: COLUMN magrupturerelation.mrrname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magrupturerelation.mrrname IS 'Magnitude Rupture Relation Name, ex. Wells and Coppersmith, 1994';


--
-- Name: COLUMN magrupturerelation.mrrdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magrupturerelation.mrrdesc IS 'Magnitude Rupture Relation Description';


--
-- Name: COLUMN magrupturerelation.mrrremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN magrupturerelation.mrrremarks IS 'Magnitude Rupture Relation Remarks';


--
-- Name: pg_stat_user_indexes; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW pg_stat_user_indexes AS
    SELECT pg_stat_all_indexes.relid, pg_stat_all_indexes.indexrelid, pg_stat_all_indexes.schemaname, pg_stat_all_indexes.relname, pg_stat_all_indexes.indexrelname, pg_stat_all_indexes.idx_scan, pg_stat_all_indexes.idx_tup_read, pg_stat_all_indexes.idx_tup_fetch FROM pg_stat_all_indexes WHERE (pg_stat_all_indexes.schemaname <> ALL (ARRAY['pg_catalog'::name, 'pg_toast'::name, 'information_schema'::name]));


--
-- Name: pg_stat_user_indexes_view; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW pg_stat_user_indexes_view AS
    SELECT pg_stat_all_indexes.relid, pg_stat_all_indexes.indexrelid, pg_stat_all_indexes.schemaname, pg_stat_all_indexes.relname, pg_stat_all_indexes.indexrelname, pg_stat_all_indexes.idx_scan, pg_stat_all_indexes.idx_tup_read, pg_stat_all_indexes.idx_tup_fetch FROM pg_stat_all_indexes WHERE (pg_stat_all_indexes.schemaname <> ALL (ARRAY['pg_catalog'::name, 'pg_toast'::name, 'information_schema'::name]));


--
-- Name: pg_stat_user_tables; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW pg_stat_user_tables AS
    SELECT pg_stat_all_tables.relid, pg_stat_all_tables.schemaname, pg_stat_all_tables.relname, pg_stat_all_tables.seq_scan, pg_stat_all_tables.seq_tup_read, pg_stat_all_tables.idx_scan, pg_stat_all_tables.idx_tup_fetch, pg_stat_all_tables.n_tup_ins, pg_stat_all_tables.n_tup_upd, pg_stat_all_tables.n_tup_del, pg_stat_all_tables.last_vacuum, pg_stat_all_tables.last_autovacuum, pg_stat_all_tables.last_analyze, pg_stat_all_tables.last_autoanalyze FROM pg_stat_all_tables WHERE (pg_stat_all_tables.schemaname <> ALL (ARRAY['pg_catalog'::name, 'pg_toast'::name, 'information_schema'::name]));


--
-- Name: pg_stat_user_tables_view; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW pg_stat_user_tables_view AS
    SELECT pg_stat_all_tables.relid, pg_stat_all_tables.schemaname, pg_stat_all_tables.relname, pg_stat_all_tables.seq_scan, pg_stat_all_tables.seq_tup_read, pg_stat_all_tables.idx_scan, pg_stat_all_tables.idx_tup_fetch, pg_stat_all_tables.n_tup_ins, pg_stat_all_tables.n_tup_upd, pg_stat_all_tables.n_tup_del, pg_stat_all_tables.last_vacuum, pg_stat_all_tables.last_autovacuum, pg_stat_all_tables.last_analyze, pg_stat_all_tables.last_autoanalyze FROM pg_stat_all_tables WHERE (pg_stat_all_tables.schemaname <> ALL (ARRAY['pg_catalog'::name, 'pg_toast'::name, 'information_schema'::name]));


--
-- Name: referenceliterature; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE referenceliterature (
    rlid integer NOT NULL,
    rlmajorreftag boolean,
    rlshortname character(20),
    rlmainauthorfname character(25),
    rlmainauthorlname character(25),
    rlotherauthor character varying(512),
    rltitle character varying(512),
    rlmediatype character(1),
    rlperiodicaltitle character varying(512),
    rlpublishercity character varying(100),
    rlpublishername character varying(512),
    rlpubnyear integer,
    rlvolnum integer,
    rlissuenum integer,
    rlpagenums character varying(100),
    rllastaccessdate date,
    rltype character(2),
    rlurl character varying(1024),
    rlremarks character varying(255)
);


--
-- Name: TABLE referenceliterature; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE referenceliterature IS 'Reference Literature';


--
-- Name: COLUMN referenceliterature.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN referenceliterature.rlmajorreftag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlmajorreftag IS 'Reference Literature Major Reference Tag';


--
-- Name: COLUMN referenceliterature.rlshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlshortname IS 'Reference Literature short name';


--
-- Name: COLUMN referenceliterature.rlmainauthorfname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlmainauthorfname IS 'Reference Literature Main Author First Name';


--
-- Name: COLUMN referenceliterature.rlmainauthorlname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlmainauthorlname IS 'Reference Literature Main Author Last Name';


--
-- Name: COLUMN referenceliterature.rlotherauthor; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlotherauthor IS 'Reference Literature Other Authors';


--
-- Name: COLUMN referenceliterature.rltitle; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rltitle IS 'Reference Literature Title';


--
-- Name: COLUMN referenceliterature.rlpublishercity; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlpublishercity IS 'Reference Lit Publisher City';


--
-- Name: COLUMN referenceliterature.rlpublishername; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlpublishername IS 'Reference Lit Publisher Name';


--
-- Name: COLUMN referenceliterature.rlpubnyear; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlpubnyear IS 'Reference Lit Publication Year';


--
-- Name: COLUMN referenceliterature.rlvolnum; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlvolnum IS 'Reference Lit Volume Number';


--
-- Name: COLUMN referenceliterature.rlissuenum; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlissuenum IS 'Reference Lit Issue Number';


--
-- Name: COLUMN referenceliterature.rlpagenums; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlpagenums IS 'Reference Lit Page Numbers';


--
-- Name: COLUMN referenceliterature.rllastaccessdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rllastaccessdate IS 'Reference Lit Last Access Date';


--
-- Name: COLUMN referenceliterature.rltype; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rltype IS 'Reference Literature Type';


--
-- Name: COLUMN referenceliterature.rlurl; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlurl IS 'Reference Literature URL';


--
-- Name: COLUMN referenceliterature.rlremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN referenceliterature.rlremarks IS 'Reference Lit Remarks';


--
-- Name: referenceliterature_rlid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE referenceliterature_rlid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: referenceliterature_rlid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE referenceliterature_rlid_seq OWNED BY referenceliterature.rlid;


--
-- Name: screference; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE screference (
    rlid integer NOT NULL,
    scid integer NOT NULL,
    scradddate timestamp without time zone
);


--
-- Name: TABLE screference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE screference IS 'Source Geometry Catalog to Reference Literature';


--
-- Name: COLUMN screference.rlid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN screference.rlid IS 'Reference Literature Id';


--
-- Name: COLUMN screference.scid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN screference.scid IS 'Source Geometry Catalog Id';


--
-- Name: COLUMN screference.scradddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN screference.scradddate IS 'Source Geom-Ref Lit Date Added';


--
-- Name: seismicsource_ssid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE seismicsource_ssid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: seismicsource_ssid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE seismicsource_ssid_seq OWNED BY seismicsource.ssid;


--
-- Name: seismotecenvt; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE seismotecenvt (
    secode character(10) NOT NULL,
    sename character varying(50),
    sedesc character varying(100),
    seremarks character varying(255)
);


--
-- Name: TABLE seismotecenvt; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE seismotecenvt IS 'Seismotectonic Environment';


--
-- Name: COLUMN seismotecenvt.secode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismotecenvt.secode IS 'Seismotectonic Environment Id';


--
-- Name: COLUMN seismotecenvt.sename; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismotecenvt.sename IS 'Seismotectonic Environment Name, e. continental collission, subduction, interplate seismicity';


--
-- Name: COLUMN seismotecenvt.sedesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismotecenvt.sedesc IS 'Seismotectonic Environment Description';


--
-- Name: COLUMN seismotecenvt.seremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN seismotecenvt.seremarks IS 'Seismotectonic Environment Remarks';


--
-- Name: sfaultchar; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE sfaultchar (
    ssfcid integer NOT NULL,
    ssfcstatus character(2),
    ssfcsliprate double precision,
    ssfcslipratesd double precision,
    ssfcfloattypeid integer,
    ssfcfloatingruptureflag boolean,
    ssfcfloatoffsetalongstrike integer,
    ssfcfloatoffsetalongdip integer,
    ssfcrupturetop integer,
    ssfcrupturebottom integer,
    ssid integer NOT NULL
);


--
-- Name: TABLE sfaultchar; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE sfaultchar IS 'Seismic Source Fault Characteristization, char only for fault';


--
-- Name: COLUMN sfaultchar.ssfcid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcid IS 'Seismic Src characterization Id';


--
-- Name: COLUMN sfaultchar.ssfcstatus; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcstatus IS 'Seismic Src characterization Status, i.e A-Active, I-Inactive, O-Other';


--
-- Name: COLUMN sfaultchar.ssfcsliprate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcsliprate IS 'Seismic Src characterization Slip Rate, Vertical or Horizontal in mm/year, ex. 6, refer USGS NSHM Fault Parameters';


--
-- Name: COLUMN sfaultchar.ssfcslipratesd; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcslipratesd IS 'Seismic Src characterization slip Rate Standard Deviation, 1 sigma, refer USGS NSHM Fault Parameters';


--
-- Name: COLUMN sfaultchar.ssfcfloattypeid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcfloattypeid IS 'fault Float Type Id, i.e. 1-Stirling';


--
-- Name: COLUMN sfaultchar.ssfcfloatingruptureflag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcfloatingruptureflag IS 'fault Floating Rupture Flag';


--
-- Name: COLUMN sfaultchar.ssfcfloatoffsetalongstrike; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcfloatoffsetalongstrike IS 'Fault Float offset along strike, in degrees';


--
-- Name: COLUMN sfaultchar.ssfcfloatoffsetalongdip; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcfloatoffsetalongdip IS 'Fault Float offset along dip, in degrees';


--
-- Name: COLUMN sfaultchar.ssfcrupturetop; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcrupturetop IS 'In kms, i.e 0';


--
-- Name: COLUMN sfaultchar.ssfcrupturebottom; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssfcrupturebottom IS 'In kms, i.e. 15';


--
-- Name: COLUMN sfaultchar.ssid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sfaultchar.ssid IS 'Seismic Source Id';


--
-- Name: sfaultchar_ssfcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE sfaultchar_ssfcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: sfaultchar_ssfcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE sfaultchar_ssfcid_seq OWNED BY sfaultchar.ssfcid;


--
-- Name: share310510; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE share310510 (
    gid integer NOT NULL,
    id integer,
    the_geom geometry,
    CONSTRAINT enforce_dims_the_geom CHECK ((st_ndims(the_geom) = 2)),
    CONSTRAINT enforce_geotype_the_geom CHECK (((geometrytype(the_geom) = 'MULTIPOLYGON'::text) OR (the_geom IS NULL))),
    CONSTRAINT enforce_srid_the_geom CHECK ((st_srid(the_geom) = 4326))
);


--
-- Name: share310510_gid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE share310510_gid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: share310510_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE share310510_gid_seq OWNED BY share310510.gid;


--
-- Name: siteamplification; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE siteamplification (
    sacode character(10) NOT NULL,
    saname character varying(50),
    sadesc character varying(100),
    savs30min integer,
    savs30max integer,
    savs30descstring character varying(50),
    sanehrp character(4),
    saintampl real,
    saremarks character varying(255)
);


--
-- Name: TABLE siteamplification; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE siteamplification IS 'Site Amplification';


--
-- Name: COLUMN siteamplification.sacode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.sacode IS 'Site Amplification Id, i.e. SOFTROCK';


--
-- Name: COLUMN siteamplification.saname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.saname IS 'Site Amplification Name, i.e Soft Rock';


--
-- Name: COLUMN siteamplification.sadesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.sadesc IS 'Site Amplification Description';


--
-- Name: COLUMN siteamplification.savs30min; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.savs30min IS 'Site Amplification VS 30 Value, i.e. 800 m/sec (values 0 to 3000)';


--
-- Name: COLUMN siteamplification.savs30max; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.savs30max IS ' i.e. 800 m/sec (values 0 to 3000)';


--
-- Name: COLUMN siteamplification.sanehrp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.sanehrp IS 'NEHRP Classification - values A, AB, B, BC, C, CD, D, DE, E';


--
-- Name: COLUMN siteamplification.saintampl; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN siteamplification.saintampl IS 'values <0 to 1.5 ...';


--
-- Name: soilclass; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE soilclass (
    socode character(10) NOT NULL,
    soname character varying(50),
    sodesc character varying(100),
    sovalue character(10),
    soremarks character varying(255)
);


--
-- Name: TABLE soilclass; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE soilclass IS 'Soil Class';


--
-- Name: COLUMN soilclass.socode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN soilclass.socode IS 'SIA 261 classification values, A to E, F1, F2';


--
-- Name: COLUMN soilclass.soname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN soilclass.soname IS 'Site Amplification Name, i.e Soft Rock';


--
-- Name: COLUMN soilclass.sodesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN soilclass.sodesc IS 'Soil Class Description';


--
-- Name: COLUMN soilclass.sovalue; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN soilclass.sovalue IS 'SIA 261 classification values, A to E, F1, F2';


--
-- Name: sourcegeometrycatalog; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE sourcegeometrycatalog (
    scid integer NOT NULL,
    scprivatetag boolean,
    scshortname character(20),
    scname character varying(50),
    scdesc character varying(100),
    sctypecode character(5),
    scareapolygon character varying(5120),
    scareamultipolygon character varying(5120),
    scstartdate timestamp without time zone,
    scenddate timestamp without time zone,
    scsources character varying(255),
    scorigformatid integer,
    scremarks character varying(255),
    scpgareapolygon geometry,
    scpgareamultipolygon geometry,
    CONSTRAINT enforce_dims_scpgareamultipolygon CHECK ((st_ndims(scpgareamultipolygon) = 2)),
    CONSTRAINT enforce_dims_scpgareapolygon CHECK ((st_ndims(scpgareapolygon) = 2)),
    CONSTRAINT enforce_geotype_scpgareamultipolygon CHECK (((geometrytype(scpgareamultipolygon) = 'MULTIPOLYGON'::text) OR (scpgareamultipolygon IS NULL))),
    CONSTRAINT enforce_geotype_scpgareapolygon CHECK (((geometrytype(scpgareapolygon) = 'POLYGON'::text) OR (scpgareapolygon IS NULL))),
    CONSTRAINT enforce_srid_scpgareamultipolygon CHECK ((st_srid(scpgareamultipolygon) = 4326)),
    CONSTRAINT enforce_srid_scpgareapolygon CHECK ((st_srid(scpgareapolygon) = 4326))
);


--
-- Name: TABLE sourcegeometrycatalog; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE sourcegeometrycatalog IS 'Catalog of Sources of Geometry, either Seismic Source Zone or Fault information';


--
-- Name: COLUMN sourcegeometrycatalog.scid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scid IS 'Source Geometry Catalog Id';


--
-- Name: COLUMN sourcegeometrycatalog.scshortname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scshortname IS 'Source Geometry catalog short name';


--
-- Name: COLUMN sourcegeometrycatalog.scname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scname IS 'Source geometry Catalog Name';


--
-- Name: COLUMN sourcegeometrycatalog.scdesc; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scdesc IS 'Source Geometry Description';


--
-- Name: COLUMN sourcegeometrycatalog.sctypecode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.sctypecode IS 'Either H-Historic, I-Instrumental, S-synthetic, L-for logictree input srcmodel or combination of all';


--
-- Name: COLUMN sourcegeometrycatalog.scareapolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scareapolygon IS 'Describes area of source geometry catalog';


--
-- Name: COLUMN sourcegeometrycatalog.scareamultipolygon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scareamultipolygon IS 'added 12 Mar 2010';


--
-- Name: COLUMN sourcegeometrycatalog.scstartdate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scstartdate IS 'Source Geometry Start Date';


--
-- Name: COLUMN sourcegeometrycatalog.scenddate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scenddate IS 'Source Geometry Catalog End Date';


--
-- Name: COLUMN sourcegeometrycatalog.scsources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scsources IS 'Source Geometry Catalog Sources';


--
-- Name: COLUMN sourcegeometrycatalog.scorigformatid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scorigformatid IS 'Source Geometry Catalog Format ID';


--
-- Name: COLUMN sourcegeometrycatalog.scremarks; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sourcegeometrycatalog.scremarks IS 'Source Geometry Catalog Remarks';


--
-- Name: sourcegeometrycatalog_scid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE sourcegeometrycatalog_scid_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: sourcegeometrycatalog_scid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE sourcegeometrycatalog_scid_seq OWNED BY sourcegeometrycatalog.scid;


--
-- Name: spatial_ref_sys; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE spatial_ref_sys (
    srid integer NOT NULL,
    auth_name character varying(256),
    auth_srid integer,
    srtext character varying(2048),
    proj4text character varying(2048)
);


--
-- Name: ecid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE earthquakecatalog ALTER COLUMN ecid SET DEFAULT nextval('earthquakecatalog_ecid_seq'::regclass);


--
-- Name: ccid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE eqcatcompleteness ALTER COLUMN ccid SET DEFAULT nextval('eqcatcompleteness_ccid_seq'::regclass);


--
-- Name: evid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE event ALTER COLUMN evid SET DEFAULT nextval('event_evid_seq'::regclass);


--
-- Name: gid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE gemsesame ALTER COLUMN gid SET DEFAULT nextval('gemsesame_gid_seq'::regclass);


--
-- Name: gpid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE geopoint ALTER COLUMN gpid SET DEFAULT nextval('geopoint_gpid_seq'::regclass);


--
-- Name: hcid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardcalculation ALTER COLUMN hcid SET DEFAULT nextval('hazardcalculation_hcid_seq'::regclass);


--
-- Name: hcrvid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardcurve ALTER COLUMN hcrvid SET DEFAULT nextval('hazardcurve_hcrvid_seq'::regclass);


--
-- Name: hibmid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardinputbasicmodel ALTER COLUMN hibmid SET DEFAULT nextval('hazardinputbasicmodel_hibmid_seq'::regclass);


--
-- Name: hilmid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardinputltreemodel ALTER COLUMN hilmid SET DEFAULT nextval('hazardinputltreemodel_hilmid_seq'::regclass);


--
-- Name: hmapid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardmap ALTER COLUMN hmapid SET DEFAULT nextval('hazardmap_hmapid_seq'::regclass);


--
-- Name: hpid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hazardpointvalue ALTER COLUMN hpid SET DEFAULT nextval('hazardpointvalue_hpid_seq'::regclass);


--
-- Name: hilmpid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hilmpath ALTER COLUMN hilmpid SET DEFAULT nextval('hilmpath_hilmpid_seq'::regclass);


--
-- Name: hilmrid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE hilmruleset ALTER COLUMN hilmrid SET DEFAULT nextval('hilmruleset_hilmrid_seq'::regclass);


--
-- Name: ltsid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE logictreestruc ALTER COLUMN ltsid SET DEFAULT nextval('logictreestruc_ltsid_seq'::regclass);


--
-- Name: ltptid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ltreeparamtype ALTER COLUMN ltptid SET DEFAULT nextval('ltreeparamtype_ltptid_seq'::regclass);


--
-- Name: ltpvid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ltreeparamvalue ALTER COLUMN ltpvid SET DEFAULT nextval('ltreeparamvalue_ltpvid_seq'::regclass);


--
-- Name: rlid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE referenceliterature ALTER COLUMN rlid SET DEFAULT nextval('referenceliterature_rlid_seq'::regclass);


--
-- Name: ssid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE seismicsource ALTER COLUMN ssid SET DEFAULT nextval('seismicsource_ssid_seq'::regclass);


--
-- Name: ssfcid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE sfaultchar ALTER COLUMN ssfcid SET DEFAULT nextval('sfaultchar_ssfcid_seq'::regclass);


--
-- Name: gid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE share310510 ALTER COLUMN gid SET DEFAULT nextval('share310510_gid_seq'::regclass);


--
-- Name: scid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE sourcegeometrycatalog ALTER COLUMN scid SET DEFAULT nextval('sourcegeometrycatalog_scid_seq'::regclass);


--
-- Name: calculationgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY calculationgroup
    ADD CONSTRAINT calculationgroup_pkey PRIMARY KEY (cgcode);


--
-- Name: calculationowner_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY calculationowner
    ADD CONSTRAINT calculationowner_pkey PRIMARY KEY (cocode);


--
-- Name: earthquakecatalog_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY earthquakecatalog
    ADD CONSTRAINT earthquakecatalog_pkey PRIMARY KEY (ecid);


--
-- Name: econstant_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY econstant
    ADD CONSTRAINT econstant_pkey PRIMARY KEY (eccode);


--
-- Name: ecreference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ecreference
    ADD CONSTRAINT ecreference_pkey PRIMARY KEY (rlid, ecid);


--
-- Name: eqcatcompleteness_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY eqcatcompleteness
    ADD CONSTRAINT eqcatcompleteness_pkey PRIMARY KEY (ccid);


--
-- Name: evariable_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY evariable
    ADD CONSTRAINT evariable_pkey PRIMARY KEY (evcode);


--
-- Name: event_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY event
    ADD CONSTRAINT event_pkey PRIMARY KEY (evid);


--
-- Name: gefeaturevalue_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gefeaturevalue
    ADD CONSTRAINT gefeaturevalue_pkey PRIMARY KEY (gfcode, gecode);


--
-- Name: gemsesame_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gemsesame
    ADD CONSTRAINT gemsesame_pkey PRIMARY KEY (gid);


--
-- Name: geometry_columns_pk; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY geometry_columns
    ADD CONSTRAINT geometry_columns_pk PRIMARY KEY (f_table_catalog, f_table_schema, f_table_name, f_geometry_column);


--
-- Name: geopoint_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY geopoint
    ADD CONSTRAINT geopoint_pkey PRIMARY KEY (gpid);


--
-- Name: gereference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gereference
    ADD CONSTRAINT gereference_pkey PRIMARY KEY (rlid, gecode);


--
-- Name: gmeconstant_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmeconstant
    ADD CONSTRAINT gmeconstant_pkey PRIMARY KEY (gecode, eccode);


--
-- Name: gmevariable_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmevariable
    ADD CONSTRAINT gmevariable_pkey PRIMARY KEY (gecode, evcode);


--
-- Name: gmparamvalue_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmparamvalue
    ADD CONSTRAINT gmparamvalue_pkey PRIMARY KEY (gpcode, gecode);


--
-- Name: gmpe_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmpe
    ADD CONSTRAINT gmpe_pkey PRIMARY KEY (gecode);


--
-- Name: gmpefeature_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmpefeature
    ADD CONSTRAINT gmpefeature_pkey PRIMARY KEY (gfcode);


--
-- Name: gmpeparameter_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY gmpeparameter
    ADD CONSTRAINT gmpeparameter_pkey PRIMARY KEY (gpcode);


--
-- Name: hazardcalculation_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT hazardcalculation_pkey PRIMARY KEY (hcid);


--
-- Name: hazardcurve_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardcurve
    ADD CONSTRAINT hazardcurve_pkey PRIMARY KEY (hcrvid);


--
-- Name: hazardinputbasicmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardinputbasicmodel
    ADD CONSTRAINT hazardinputbasicmodel_pkey PRIMARY KEY (hibmid);


--
-- Name: hazardinputltreemodel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardinputltreemodel
    ADD CONSTRAINT hazardinputltreemodel_pkey PRIMARY KEY (hilmid);


--
-- Name: hazardmap_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardmap
    ADD CONSTRAINT hazardmap_pkey PRIMARY KEY (hmapid);


--
-- Name: hazardpointvalue_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardpointvalue
    ADD CONSTRAINT hazardpointvalue_pkey PRIMARY KEY (hpid);


--
-- Name: hazardsoftware_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hazardsoftware
    ADD CONSTRAINT hazardsoftware_pkey PRIMARY KEY (hscode);


--
-- Name: hibmge_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hibmge
    ADD CONSTRAINT hibmge_pkey PRIMARY KEY (hibmid, gecode);


--
-- Name: hibmreference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hibmreference
    ADD CONSTRAINT hibmreference_pkey PRIMARY KEY (rlid, hibmid);


--
-- Name: hilmpath_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hilmpath
    ADD CONSTRAINT hilmpath_pkey PRIMARY KEY (hilmpid);


--
-- Name: hilmpge_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hilmpge
    ADD CONSTRAINT hilmpge_pkey PRIMARY KEY (hilmpid, gecode);


--
-- Name: hilmreference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hilmreference
    ADD CONSTRAINT hilmreference_pkey PRIMARY KEY (rlid, hilmid);


--
-- Name: hilmruleset_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hilmruleset
    ADD CONSTRAINT hilmruleset_pkey PRIMARY KEY (hilmrid);


--
-- Name: intensitymeasuretype_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY intensitymeasuretype
    ADD CONSTRAINT intensitymeasuretype_pkey PRIMARY KEY (imcode);


--
-- Name: logictreestruc_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY logictreestruc
    ADD CONSTRAINT logictreestruc_pkey PRIMARY KEY (ltsid);


--
-- Name: ltreeparamtype_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ltreeparamtype
    ADD CONSTRAINT ltreeparamtype_pkey PRIMARY KEY (ltptid);


--
-- Name: ltreeparamtypelevel_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ltreeparamtypelevel
    ADD CONSTRAINT ltreeparamtypelevel_pkey PRIMARY KEY (ltptid, ltsid);


--
-- Name: ltreeparamvalue_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ltreeparamvalue
    ADD CONSTRAINT ltreeparamvalue_pkey PRIMARY KEY (ltpvid);


--
-- Name: magfreqdistn_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY magfreqdistn
    ADD CONSTRAINT magfreqdistn_pkey PRIMARY KEY (mfdcode);


--
-- Name: magrupturerelation_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY magrupturerelation
    ADD CONSTRAINT magrupturerelation_pkey PRIMARY KEY (mrrcode);


--
-- Name: referenceliterature_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY referenceliterature
    ADD CONSTRAINT referenceliterature_pkey PRIMARY KEY (rlid);


--
-- Name: screference_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY screference
    ADD CONSTRAINT screference_pkey PRIMARY KEY (rlid, scid);


--
-- Name: seismicsource_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY seismicsource
    ADD CONSTRAINT seismicsource_pkey PRIMARY KEY (ssid);


--
-- Name: seismotecenvt_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY seismotecenvt
    ADD CONSTRAINT seismotecenvt_pkey PRIMARY KEY (secode);


--
-- Name: sfaultchar_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY sfaultchar
    ADD CONSTRAINT sfaultchar_pkey PRIMARY KEY (ssfcid);


--
-- Name: share310510_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY share310510
    ADD CONSTRAINT share310510_pkey PRIMARY KEY (gid);


--
-- Name: siteamplification_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY siteamplification
    ADD CONSTRAINT siteamplification_pkey PRIMARY KEY (sacode);


--
-- Name: soilclass_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY soilclass
    ADD CONSTRAINT soilclass_pkey PRIMARY KEY (socode);


--
-- Name: sourcegeometrycatalog_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY sourcegeometrycatalog
    ADD CONSTRAINT sourcegeometrycatalog_pkey PRIMARY KEY (scid);


--
-- Name: spatial_ref_sys_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY spatial_ref_sys
    ADD CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid);


--
-- Name: ssourcemfd_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY ssourcemfd
    ADD CONSTRAINT ssourcemfd_pkey PRIMARY KEY (ssid, mfdcode, ssmfdseqnum);


--
-- Name: geopoint_gppgpoint_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX geopoint_gppgpoint_idx ON geopoint USING gist (gppgpoint);

ALTER TABLE geopoint CLUSTER ON geopoint_gppgpoint_idx;


--
-- Name: gmpe_gecode_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX gmpe_gecode_idx ON gmpe USING btree (gecode);


--
-- Name: hazardcalculation_hcpgareapolygon_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardcalculation_hcpgareapolygon_idx ON hazardcalculation USING gist (hcpgareapolygon);


--
-- Name: hazardcalculation_hibmid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardcalculation_hibmid_idx ON hazardcalculation USING btree (hibmid);


--
-- Name: hazardcalculation_hilmid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardcalculation_hilmid_idx ON hazardcalculation USING btree (hilmid);


--
-- Name: hazardcalculation_hilmpid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardcalculation_hilmpid_idx ON hazardcalculation USING btree (hilmpid);


--
-- Name: hazardcurve_hcid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardcurve_hcid_idx ON hazardcurve USING btree (hcid);


--
-- Name: hazardinputbasicmodel_hibmid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardinputbasicmodel_hibmid_idx ON hazardinputbasicmodel USING btree (hibmid);


--
-- Name: hazardinputltreemodel_hilmpgareapolygon_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardinputltreemodel_hilmpgareapolygon_idx ON hazardinputltreemodel USING gist (hilmpgareapolygon);


--
-- Name: hazardmap_hcid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardmap_hcid_idx ON hazardmap USING btree (hcid);


--
-- Name: hazardpointvalue_gpid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardpointvalue_gpid_idx ON hazardpointvalue USING btree (gpid);


--
-- Name: hazardpointvalue_hcid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardpointvalue_hcid_idx ON hazardpointvalue USING btree (hcid);


--
-- Name: hazardpointvalue_hpvalue_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardpointvalue_hpvalue_idx ON hazardpointvalue USING btree (hpvalue);


--
-- Name: hazardpointvalue_imcode_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX hazardpointvalue_imcode_idx ON hazardpointvalue USING btree (imcode);


--
-- Name: magrupturerelation_mrrcode_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX magrupturerelation_mrrcode_idx ON magrupturerelation USING btree (mrrcode);


--
-- Name: referenceliterature_rlid_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX referenceliterature_rlid_idx ON referenceliterature USING btree (rlid);


--
-- Name: siteamplification_sacode_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX siteamplification_sacode_idx ON siteamplification USING btree (sacode);


--
-- Name: soilclass_socode_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX soilclass_socode_idx ON soilclass USING btree (socode);


--
-- Name: ssourcemfd_scmfdseq_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX ssourcemfd_scmfdseq_idx ON ssourcemfd USING btree (ssid, mfdcode, ssmfdseqnum);


--
-- Name: fk_calculationowner_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY calculationowner
    ADD CONSTRAINT fk_calculationowner_1 FOREIGN KEY (cgcode) REFERENCES calculationgroup(cgcode);


--
-- Name: fk_eqcatcompleteness_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY eqcatcompleteness
    ADD CONSTRAINT fk_eqcatcompleteness_1 FOREIGN KEY (ecid) REFERENCES earthquakecatalog(ecid);


--
-- Name: fk_eqcatreference_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ecreference
    ADD CONSTRAINT fk_eqcatreference_2 FOREIGN KEY (rlid) REFERENCES referenceliterature(rlid);


--
-- Name: fk_eqcatreference_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ecreference
    ADD CONSTRAINT fk_eqcatreference_3 FOREIGN KEY (ecid) REFERENCES earthquakecatalog(ecid);


--
-- Name: fk_event_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY event
    ADD CONSTRAINT fk_event_1 FOREIGN KEY (ecid) REFERENCES earthquakecatalog(ecid);


--
-- Name: fk_geopoint_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY geopoint
    ADD CONSTRAINT fk_geopoint_2 FOREIGN KEY (socode) REFERENCES soilclass(socode);


--
-- Name: fk_geopoint_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY geopoint
    ADD CONSTRAINT fk_geopoint_3 FOREIGN KEY (sacode) REFERENCES siteamplification(sacode);


--
-- Name: fk_gfvalue_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gefeaturevalue
    ADD CONSTRAINT fk_gfvalue_2 FOREIGN KEY (gfcode) REFERENCES gmpefeature(gfcode);


--
-- Name: fk_gmeconstant_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmeconstant
    ADD CONSTRAINT fk_gmeconstant_2 FOREIGN KEY (eccode) REFERENCES econstant(eccode);


--
-- Name: fk_gmeconstant_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmeconstant
    ADD CONSTRAINT fk_gmeconstant_3 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_gmevariable_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmevariable
    ADD CONSTRAINT fk_gmevariable_2 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_gmevariable_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmevariable
    ADD CONSTRAINT fk_gmevariable_3 FOREIGN KEY (evcode) REFERENCES evariable(evcode);


--
-- Name: fk_gmfeaturevalue_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gefeaturevalue
    ADD CONSTRAINT fk_gmfeaturevalue_2 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_gmparamvalue_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmparamvalue
    ADD CONSTRAINT fk_gmparamvalue_1 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_gmparamvalue_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmparamvalue
    ADD CONSTRAINT fk_gmparamvalue_2 FOREIGN KEY (gpcode) REFERENCES gmpeparameter(gpcode);


--
-- Name: fk_gmpe_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gmpe
    ADD CONSTRAINT fk_gmpe_1 FOREIGN KEY (secode) REFERENCES seismotecenvt(secode);


--
-- Name: fk_gmpereference_1_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gereference
    ADD CONSTRAINT fk_gmpereference_1_2 FOREIGN KEY (rlid) REFERENCES referenceliterature(rlid);


--
-- Name: fk_gmpereference_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY gereference
    ADD CONSTRAINT fk_gmpereference_2 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_hazardcalculation_4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_4 FOREIGN KEY (hilmpid) REFERENCES hilmpath(hilmpid);


--
-- Name: fk_hazardcalculation_5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_5 FOREIGN KEY (cocode) REFERENCES calculationowner(cocode);


--
-- Name: fk_hazardcalculation_6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_6 FOREIGN KEY (hscode) REFERENCES hazardsoftware(hscode);


--
-- Name: fk_hazardcalculation_7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_7 FOREIGN KEY (hibmid) REFERENCES hazardinputbasicmodel(hibmid);


--
-- Name: fk_hazardcalculation_8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_8 FOREIGN KEY (evid) REFERENCES event(evid);


--
-- Name: fk_hazardcalculation_9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcalculation
    ADD CONSTRAINT fk_hazardcalculation_9 FOREIGN KEY (hilmid) REFERENCES hazardinputltreemodel(hilmid);


--
-- Name: fk_hazardcurve_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcurve
    ADD CONSTRAINT fk_hazardcurve_1 FOREIGN KEY (hcid) REFERENCES hazardcalculation(hcid);


--
-- Name: fk_hazardcurve_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcurve
    ADD CONSTRAINT fk_hazardcurve_2 FOREIGN KEY (gpid) REFERENCES geopoint(gpid);


--
-- Name: fk_hazardcurve_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardcurve
    ADD CONSTRAINT fk_hazardcurve_3 FOREIGN KEY (imcode) REFERENCES intensitymeasuretype(imcode);


--
-- Name: fk_hazardinputltreemodel_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardinputltreemodel
    ADD CONSTRAINT fk_hazardinputltreemodel_1 FOREIGN KEY (ltsid) REFERENCES logictreestruc(ltsid);


--
-- Name: fk_hazardinputmodel_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardinputbasicmodel
    ADD CONSTRAINT fk_hazardinputmodel_1 FOREIGN KEY (scid) REFERENCES sourcegeometrycatalog(scid);


--
-- Name: fk_hazardmap_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardmap
    ADD CONSTRAINT fk_hazardmap_1 FOREIGN KEY (hcid) REFERENCES hazardcalculation(hcid);


--
-- Name: fk_hazardmap_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardmap
    ADD CONSTRAINT fk_hazardmap_2 FOREIGN KEY (imcode) REFERENCES intensitymeasuretype(imcode);


--
-- Name: fk_hazardpoint_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardpointvalue
    ADD CONSTRAINT fk_hazardpoint_2 FOREIGN KEY (gpid) REFERENCES geopoint(gpid);


--
-- Name: fk_hazardpointvalue_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardpointvalue
    ADD CONSTRAINT fk_hazardpointvalue_3 FOREIGN KEY (imcode) REFERENCES intensitymeasuretype(imcode);


--
-- Name: fk_hazardpointvalue_4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hazardpointvalue
    ADD CONSTRAINT fk_hazardpointvalue_4 FOREIGN KEY (hcid) REFERENCES hazardcalculation(hcid);


--
-- Name: fk_hibmge_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hibmge
    ADD CONSTRAINT fk_hibmge_1 FOREIGN KEY (hibmid) REFERENCES hazardinputbasicmodel(hibmid);


--
-- Name: fk_hibmge_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hibmge
    ADD CONSTRAINT fk_hibmge_2 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_hibmreference_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hibmreference
    ADD CONSTRAINT fk_hibmreference_2 FOREIGN KEY (hibmid) REFERENCES hazardinputbasicmodel(hibmid);


--
-- Name: fk_hilmge_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmpge
    ADD CONSTRAINT fk_hilmge_1 FOREIGN KEY (hilmpid) REFERENCES hilmpath(hilmpid);


--
-- Name: fk_hilmge_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmpge
    ADD CONSTRAINT fk_hilmge_2 FOREIGN KEY (gecode) REFERENCES gmpe(gecode);


--
-- Name: fk_hilmpath_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmpath
    ADD CONSTRAINT fk_hilmpath_1 FOREIGN KEY (hilmid) REFERENCES hazardinputltreemodel(hilmid);


--
-- Name: fk_hilmpath_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmpath
    ADD CONSTRAINT fk_hilmpath_2 FOREIGN KEY (scid) REFERENCES sourcegeometrycatalog(scid);


--
-- Name: fk_hilmreference_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmreference
    ADD CONSTRAINT fk_hilmreference_1 FOREIGN KEY (hilmid) REFERENCES hazardinputltreemodel(hilmid);


--
-- Name: fk_hilmreference_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmreference
    ADD CONSTRAINT fk_hilmreference_2 FOREIGN KEY (rlid) REFERENCES referenceliterature(rlid);


--
-- Name: fk_hilmruleset_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmruleset
    ADD CONSTRAINT fk_hilmruleset_1 FOREIGN KEY (hilmid) REFERENCES hazardinputltreemodel(hilmid);


--
-- Name: fk_hilmruleset_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmruleset
    ADD CONSTRAINT fk_hilmruleset_2 FOREIGN KEY (ltptid) REFERENCES ltreeparamtype(ltptid);


--
-- Name: fk_hilmruleset_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hilmruleset
    ADD CONSTRAINT fk_hilmruleset_3 FOREIGN KEY (ltpvid) REFERENCES ltreeparamvalue(ltpvid);


--
-- Name: fk_hmreference_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hibmreference
    ADD CONSTRAINT fk_hmreference_1 FOREIGN KEY (rlid) REFERENCES referenceliterature(rlid);


--
-- Name: fk_ltreeparamtypelevel_1_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ltreeparamtypelevel
    ADD CONSTRAINT fk_ltreeparamtypelevel_1_2 FOREIGN KEY (ltptid) REFERENCES ltreeparamtype(ltptid);


--
-- Name: fk_ltreeparamtypelevel_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ltreeparamtypelevel
    ADD CONSTRAINT fk_ltreeparamtypelevel_2 FOREIGN KEY (ltsid) REFERENCES logictreestruc(ltsid);


--
-- Name: fk_ltreeparamvalue_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ltreeparamvalue
    ADD CONSTRAINT fk_ltreeparamvalue_2 FOREIGN KEY (ltptid) REFERENCES ltreeparamtype(ltptid);


--
-- Name: fk_seismicsource_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY seismicsource
    ADD CONSTRAINT fk_seismicsource_1 FOREIGN KEY (scid) REFERENCES sourcegeometrycatalog(scid);


--
-- Name: fk_seismicsource_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY seismicsource
    ADD CONSTRAINT fk_seismicsource_2 FOREIGN KEY (secode) REFERENCES seismotecenvt(secode);


--
-- Name: fk_sfaultchar_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY sfaultchar
    ADD CONSTRAINT fk_sfaultchar_3 FOREIGN KEY (ssid) REFERENCES seismicsource(ssid);


--
-- Name: fk_sourcegeomreference_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY screference
    ADD CONSTRAINT fk_sourcegeomreference_2 FOREIGN KEY (rlid) REFERENCES referenceliterature(rlid);


--
-- Name: fk_sourcegeomreference_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY screference
    ADD CONSTRAINT fk_sourcegeomreference_3 FOREIGN KEY (scid) REFERENCES sourcegeometrycatalog(scid);


--
-- Name: fk_ssourcemfd_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ssourcemfd
    ADD CONSTRAINT fk_ssourcemfd_1 FOREIGN KEY (ssid) REFERENCES seismicsource(ssid);


--
-- Name: fk_ssourcemfd_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ssourcemfd
    ADD CONSTRAINT fk_ssourcemfd_2 FOREIGN KEY (mfdcode) REFERENCES magfreqdistn(mfdcode);


--
-- Name: fk_ssourcemfd_3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY ssourcemfd
    ADD CONSTRAINT fk_ssourcemfd_3 FOREIGN KEY (mrrcode) REFERENCES magrupturerelation(mrrcode);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: calculationgroup; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE calculationgroup FROM PUBLIC;
REVOKE ALL ON TABLE calculationgroup FROM postgres;
GRANT ALL ON TABLE calculationgroup TO postgres;
GRANT SELECT ON TABLE calculationgroup TO gemuser;


--
-- Name: calculationowner; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE calculationowner FROM PUBLIC;
REVOKE ALL ON TABLE calculationowner FROM postgres;
GRANT ALL ON TABLE calculationowner TO postgres;
GRANT SELECT ON TABLE calculationowner TO gemuser;


--
-- Name: earthquakecatalog; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE earthquakecatalog FROM PUBLIC;
REVOKE ALL ON TABLE earthquakecatalog FROM postgres;
GRANT ALL ON TABLE earthquakecatalog TO postgres;
GRANT SELECT ON TABLE earthquakecatalog TO gemuser;


--
-- Name: econstant; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE econstant FROM PUBLIC;
REVOKE ALL ON TABLE econstant FROM postgres;
GRANT ALL ON TABLE econstant TO postgres;
GRANT SELECT ON TABLE econstant TO gemuser;


--
-- Name: ecreference; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE ecreference FROM PUBLIC;
REVOKE ALL ON TABLE ecreference FROM postgres;
GRANT ALL ON TABLE ecreference TO postgres;
GRANT SELECT ON TABLE ecreference TO gemuser;


--
-- Name: eqcatcompleteness; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE eqcatcompleteness FROM PUBLIC;
REVOKE ALL ON TABLE eqcatcompleteness FROM postgres;
GRANT ALL ON TABLE eqcatcompleteness TO postgres;
GRANT SELECT ON TABLE eqcatcompleteness TO gemuser;


--
-- Name: seismicsource; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE seismicsource FROM PUBLIC;
REVOKE ALL ON TABLE seismicsource FROM postgres;
GRANT ALL ON TABLE seismicsource TO postgres;
GRANT SELECT ON TABLE seismicsource TO gemuser;


--
-- Name: ssourcemfd; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE ssourcemfd FROM PUBLIC;
REVOKE ALL ON TABLE ssourcemfd FROM postgres;
GRANT ALL ON TABLE ssourcemfd TO postgres;
GRANT SELECT ON TABLE ssourcemfd TO gemuser;


--
-- Name: evariable; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE evariable FROM PUBLIC;
REVOKE ALL ON TABLE evariable FROM postgres;
GRANT ALL ON TABLE evariable TO postgres;
GRANT SELECT ON TABLE evariable TO gemuser;


--
-- Name: event; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE event FROM PUBLIC;
REVOKE ALL ON TABLE event FROM postgres;
GRANT ALL ON TABLE event TO postgres;
GRANT SELECT ON TABLE event TO gemuser;


--
-- Name: gefeaturevalue; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gefeaturevalue FROM PUBLIC;
REVOKE ALL ON TABLE gefeaturevalue FROM postgres;
GRANT ALL ON TABLE gefeaturevalue TO postgres;
GRANT SELECT ON TABLE gefeaturevalue TO gemuser;


--
-- Name: geometry_columns; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE geometry_columns FROM PUBLIC;
REVOKE ALL ON TABLE geometry_columns FROM postgres;
GRANT ALL ON TABLE geometry_columns TO postgres;
GRANT SELECT ON TABLE geometry_columns TO gemuser;


--
-- Name: geopoint; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE geopoint FROM PUBLIC;
REVOKE ALL ON TABLE geopoint FROM postgres;
GRANT ALL ON TABLE geopoint TO postgres;
GRANT SELECT ON TABLE geopoint TO gemuser;


--
-- Name: gereference; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gereference FROM PUBLIC;
REVOKE ALL ON TABLE gereference FROM postgres;
GRANT ALL ON TABLE gereference TO postgres;
GRANT SELECT ON TABLE gereference TO gemuser;


--
-- Name: gmeconstant; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmeconstant FROM PUBLIC;
REVOKE ALL ON TABLE gmeconstant FROM postgres;
GRANT ALL ON TABLE gmeconstant TO postgres;
GRANT SELECT ON TABLE gmeconstant TO gemuser;


--
-- Name: gmevariable; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmevariable FROM PUBLIC;
REVOKE ALL ON TABLE gmevariable FROM postgres;
GRANT ALL ON TABLE gmevariable TO postgres;
GRANT SELECT ON TABLE gmevariable TO gemuser;


--
-- Name: gmparamvalue; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmparamvalue FROM PUBLIC;
REVOKE ALL ON TABLE gmparamvalue FROM postgres;
GRANT ALL ON TABLE gmparamvalue TO postgres;
GRANT SELECT ON TABLE gmparamvalue TO gemuser;


--
-- Name: gmpe; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmpe FROM PUBLIC;
REVOKE ALL ON TABLE gmpe FROM postgres;
GRANT ALL ON TABLE gmpe TO postgres;
GRANT SELECT ON TABLE gmpe TO gemuser;


--
-- Name: gmpefeature; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmpefeature FROM PUBLIC;
REVOKE ALL ON TABLE gmpefeature FROM postgres;
GRANT ALL ON TABLE gmpefeature TO postgres;
GRANT SELECT ON TABLE gmpefeature TO gemuser;


--
-- Name: gmpeparameter; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE gmpeparameter FROM PUBLIC;
REVOKE ALL ON TABLE gmpeparameter FROM postgres;
GRANT ALL ON TABLE gmpeparameter TO postgres;
GRANT SELECT ON TABLE gmpeparameter TO gemuser;


--
-- Name: hazardpointvalue; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardpointvalue FROM PUBLIC;
REVOKE ALL ON TABLE hazardpointvalue FROM postgres;
GRANT ALL ON TABLE hazardpointvalue TO postgres;
GRANT SELECT ON TABLE hazardpointvalue TO gemuser;


--
-- Name: hazardcalculation; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardcalculation FROM PUBLIC;
REVOKE ALL ON TABLE hazardcalculation FROM postgres;
GRANT ALL ON TABLE hazardcalculation TO postgres;
GRANT SELECT ON TABLE hazardcalculation TO gemuser;


--
-- Name: hazardcurve; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardcurve FROM PUBLIC;
REVOKE ALL ON TABLE hazardcurve FROM postgres;
GRANT ALL ON TABLE hazardcurve TO postgres;
GRANT SELECT ON TABLE hazardcurve TO gemuser;


--
-- Name: hazardinputbasicmodel; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardinputbasicmodel FROM PUBLIC;
REVOKE ALL ON TABLE hazardinputbasicmodel FROM postgres;
GRANT ALL ON TABLE hazardinputbasicmodel TO postgres;
GRANT SELECT ON TABLE hazardinputbasicmodel TO gemuser;


--
-- Name: hazardinputltreemodel; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardinputltreemodel FROM PUBLIC;
REVOKE ALL ON TABLE hazardinputltreemodel FROM postgres;
GRANT ALL ON TABLE hazardinputltreemodel TO postgres;
GRANT SELECT ON TABLE hazardinputltreemodel TO gemuser;


--
-- Name: hazardmap; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardmap FROM PUBLIC;
REVOKE ALL ON TABLE hazardmap FROM postgres;
GRANT ALL ON TABLE hazardmap TO postgres;
GRANT SELECT ON TABLE hazardmap TO gemuser;


--
-- Name: hazardsoftware; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hazardsoftware FROM PUBLIC;
REVOKE ALL ON TABLE hazardsoftware FROM postgres;
GRANT ALL ON TABLE hazardsoftware TO postgres;
GRANT SELECT ON TABLE hazardsoftware TO gemuser;


--
-- Name: hibmge; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hibmge FROM PUBLIC;
REVOKE ALL ON TABLE hibmge FROM postgres;
GRANT ALL ON TABLE hibmge TO postgres;
GRANT SELECT ON TABLE hibmge TO gemuser;


--
-- Name: hibmreference; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hibmreference FROM PUBLIC;
REVOKE ALL ON TABLE hibmreference FROM postgres;
GRANT ALL ON TABLE hibmreference TO postgres;
GRANT SELECT ON TABLE hibmreference TO gemuser;


--
-- Name: hilmpath; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hilmpath FROM PUBLIC;
REVOKE ALL ON TABLE hilmpath FROM postgres;
GRANT ALL ON TABLE hilmpath TO postgres;
GRANT SELECT ON TABLE hilmpath TO gemuser;


--
-- Name: hilmpge; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hilmpge FROM PUBLIC;
REVOKE ALL ON TABLE hilmpge FROM postgres;
GRANT ALL ON TABLE hilmpge TO postgres;
GRANT SELECT ON TABLE hilmpge TO gemuser;


--
-- Name: hilmreference; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hilmreference FROM PUBLIC;
REVOKE ALL ON TABLE hilmreference FROM postgres;
GRANT ALL ON TABLE hilmreference TO postgres;
GRANT SELECT ON TABLE hilmreference TO gemuser;


--
-- Name: hilmruleset; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE hilmruleset FROM PUBLIC;
REVOKE ALL ON TABLE hilmruleset FROM postgres;
GRANT ALL ON TABLE hilmruleset TO postgres;
GRANT SELECT ON TABLE hilmruleset TO gemuser;


--
-- Name: intensitymeasuretype; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE intensitymeasuretype FROM PUBLIC;
REVOKE ALL ON TABLE intensitymeasuretype FROM postgres;
GRANT ALL ON TABLE intensitymeasuretype TO postgres;
GRANT SELECT ON TABLE intensitymeasuretype TO gemuser;


--
-- Name: logictreestruc; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE logictreestruc FROM PUBLIC;
REVOKE ALL ON TABLE logictreestruc FROM postgres;
GRANT ALL ON TABLE logictreestruc TO postgres;
GRANT SELECT ON TABLE logictreestruc TO gemuser;


--
-- Name: ltreeparamtype; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE ltreeparamtype FROM PUBLIC;
REVOKE ALL ON TABLE ltreeparamtype FROM postgres;
GRANT ALL ON TABLE ltreeparamtype TO postgres;
GRANT SELECT ON TABLE ltreeparamtype TO gemuser;


--
-- Name: ltreeparamtypelevel; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE ltreeparamtypelevel FROM PUBLIC;
REVOKE ALL ON TABLE ltreeparamtypelevel FROM postgres;
GRANT ALL ON TABLE ltreeparamtypelevel TO postgres;
GRANT SELECT ON TABLE ltreeparamtypelevel TO gemuser;


--
-- Name: ltreeparamvalue; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE ltreeparamvalue FROM PUBLIC;
REVOKE ALL ON TABLE ltreeparamvalue FROM postgres;
GRANT ALL ON TABLE ltreeparamvalue TO postgres;
GRANT SELECT ON TABLE ltreeparamvalue TO gemuser;


--
-- Name: magfreqdistn; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE magfreqdistn FROM PUBLIC;
REVOKE ALL ON TABLE magfreqdistn FROM postgres;
GRANT ALL ON TABLE magfreqdistn TO postgres;
GRANT SELECT ON TABLE magfreqdistn TO gemuser;


--
-- Name: magrupturerelation; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE magrupturerelation FROM PUBLIC;
REVOKE ALL ON TABLE magrupturerelation FROM postgres;
GRANT ALL ON TABLE magrupturerelation TO postgres;
GRANT SELECT ON TABLE magrupturerelation TO gemuser;


--
-- Name: referenceliterature; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE referenceliterature FROM PUBLIC;
REVOKE ALL ON TABLE referenceliterature FROM postgres;
GRANT ALL ON TABLE referenceliterature TO postgres;
GRANT SELECT ON TABLE referenceliterature TO gemuser;


--
-- Name: screference; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE screference FROM PUBLIC;
REVOKE ALL ON TABLE screference FROM postgres;
GRANT ALL ON TABLE screference TO postgres;
GRANT SELECT ON TABLE screference TO gemuser;


--
-- Name: seismotecenvt; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE seismotecenvt FROM PUBLIC;
REVOKE ALL ON TABLE seismotecenvt FROM postgres;
GRANT ALL ON TABLE seismotecenvt TO postgres;
GRANT SELECT ON TABLE seismotecenvt TO gemuser;


--
-- Name: sfaultchar; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE sfaultchar FROM PUBLIC;
REVOKE ALL ON TABLE sfaultchar FROM postgres;
GRANT ALL ON TABLE sfaultchar TO postgres;
GRANT SELECT ON TABLE sfaultchar TO gemuser;


--
-- Name: siteamplification; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE siteamplification FROM PUBLIC;
REVOKE ALL ON TABLE siteamplification FROM postgres;
GRANT ALL ON TABLE siteamplification TO postgres;
GRANT SELECT ON TABLE siteamplification TO gemuser;


--
-- Name: soilclass; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE soilclass FROM PUBLIC;
REVOKE ALL ON TABLE soilclass FROM postgres;
GRANT ALL ON TABLE soilclass TO postgres;
GRANT SELECT ON TABLE soilclass TO gemuser;


--
-- Name: sourcegeometrycatalog; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE sourcegeometrycatalog FROM PUBLIC;
REVOKE ALL ON TABLE sourcegeometrycatalog FROM postgres;
GRANT ALL ON TABLE sourcegeometrycatalog TO postgres;
GRANT SELECT ON TABLE sourcegeometrycatalog TO gemuser;


--
-- Name: spatial_ref_sys; Type: ACL; Schema: public; Owner: -
--

REVOKE ALL ON TABLE spatial_ref_sys FROM PUBLIC;
REVOKE ALL ON TABLE spatial_ref_sys FROM postgres;
GRANT ALL ON TABLE spatial_ref_sys TO postgres;
GRANT SELECT ON TABLE spatial_ref_sys TO gemuser;


--
-- PostgreSQL database dump complete
--

