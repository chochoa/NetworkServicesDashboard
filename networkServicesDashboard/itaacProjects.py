from peewee import *

itaacProjects = PostgresqlDatabase('itaacProjects')

class UnknownFieldType(object):
    pass

class itaacModel(Model):
    class Meta:
        database = itaacProjects

class NewProject(itaacModel):
    timeupdated = CharField(max_length=255, null=True)
    alocation = CharField(max_length=255, null=True)
    alocationcisco = CharField(max_length=255, null=True)
    archdocumentation = CharField(max_length=255, null=True)
    assignee = CharField(max_length=255, null=True)
    billingauth = CharField(max_length=255, null=True)
    billingdept = CharField(max_length=255, null=True)
    businessunit = CharField(max_length=255, null=True)
    circuitdiagram = CharField(max_length=255, null=True)
    circuitid = CharField(max_length=255, null=True)
    circuittype = CharField(max_length=255, null=True)
    cost = CharField(max_length=255, null=True)
    crdate = CharField(max_length=255, null=True)
    crnumber = TextField(null=True)
    currentstatus = CharField(max_length=255,null=True)
    designclientapproval = CharField(max_length=255, null=True)
    designdocumentation = CharField(max_length=255, null=True)
    designstatus = CharField(max_length=255, null=True)
    discoveryauthyes = CharField(max_length=255, null=True)
    discoverystatus = CharField(max_length=255, null=True)
    hardwareassessment = CharField(max_length=255, null=True)
    hardwareneeded = CharField(max_length=255, null=True)
    hardwareorderno = CharField(max_length=255, null=True)
    i2ocaseaccepted = CharField(max_length=255, null=True)
    i2ocaseacceptedtimestamp = CharField(max_length=255, null=True)
    i2ocasecompleted = CharField(max_length=255, null=True)
    i2ocasecompletedtimestamp = CharField(max_length=255, null=True)
    i2ocasecreated = CharField(max_length=255, null=True)
    i2ocasecreatedtimestamp = CharField(max_length=255, null=True)
    i2ocasenumber = CharField(max_length=255, null=True)
    i2ocasereleased = CharField(max_length=255, null=True)
    i2ocasereleasedtimestamp = CharField(max_length=255, null=True)
    implementationstatus = CharField(max_length=255, null=True)
    impother = CharField(max_length=255, null=True)
    labid = TextField(null=True)
    linecard = CharField(max_length=255, null=True)
    litcase = CharField(max_length=255, null=True)
    mailer = CharField(max_length=255, null=True)
    opsstatus = CharField(max_length=255, null=True)
    projectid = PrimaryKeyField()
    projectname = CharField(max_length=255, null=True)
    requestor = CharField(max_length=255, null=True)
    securityfinalreview = CharField(max_length=255, null=True)
    securitystatus = CharField(max_length=255, null=True)
    securitycase = TextField(null=True)
    servicestatus = IntegerField(null=True)
    serviceteamcomments = CharField(max_length=255, null=True)
    targetdate = CharField(max_length=255, null=True)
    teamreview = CharField(max_length=255, null=True)
    thirdparty = CharField(max_length=255, null=True)
    zlocation = CharField(max_length=255, null=True)
    zlocationcisco = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'newproject'

class Assignees(itaacModel):
    assigneeid = PrimaryKeyField()
    function = TextField(null=True)
    name = TextField(null=True)

    class Meta:
        db_table = 'assignees'

class Circuits(itaacModel):
    a_bldg = CharField(max_length=255, null=True)
    a_node = CharField(max_length=255, null=True)
    business_use = CharField(max_length=255, null=True)
    circuit = CharField(max_length=255, null=True, db_column='circuit_id')
    circuit_id_no = IntegerField(null=True)
    circuitid = PrimaryKeyField()
    ckt_cnt_in_service = CharField(max_length=255, null=True)
    cross_connect = CharField(max_length=255, null=True, db_column='cross_connect_id')
    customer = CharField(max_length=255, null=True)
    description = CharField(max_length=255, null=True)
    long_haul_circuit = CharField(max_length=255, null=True, db_column='long_haul_circuit_id')
    mailers = CharField(max_length=255, null=True)
    notes = CharField(max_length=255, null=True)
    poc = CharField(max_length=255, null=True)
    poc_email = CharField(max_length=255, null=True)
    poc_phone = CharField(max_length=255, null=True)
    protected = CharField(max_length=255, null=True)
    protocol = CharField(max_length=255, null=True)
    qrtr = CharField(max_length=255, null=True)
    sec_poc = CharField(max_length=255, null=True)
    sec_poc_email = CharField(max_length=255, null=True)
    sec_poc_phone = CharField(max_length=255, null=True)
    z_bldg = CharField(max_length=255, null=True)
    z_node = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'circuits'

class ColoCombo(itaacModel):
    address = CharField(max_length=255, null=True)
    cabino_no = IntegerField(null=True)
    combination = IntegerField(null=True)
    comboid = PrimaryKeyField()
    infoprovider = CharField(null=True)
    notes = TextField(null=True)
    ownder = CharField(max_length=255, null=True)
    site = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'colocombo'

class ProjectTypes(itaacModel):
    monthlycost = IntegerField(null=True)
    size = CharField(max_length=255, null=True)
    circuittype = CharField(max_length=255, null=True)
    typeid = PrimaryKeyField()

    class Meta:
        db_table = 'projecttypes'

class ITaaCResources(itaacModel):
    resourceid = PrimaryKeyField()
    resourcelogin = CharField(max_length=255, null=True)
    resourcename = CharField(max_length=255, null=True)
    resourcetype = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'itaacresources'

class LineCards(itaacModel):
    cardid = PrimaryKeyField()
    cardname = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'linecards'

class Location(itaacModel):
    locationid = PrimaryKeyField()
    locationname = CharField(max_length=255, null=True)
    locationtype = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'location'
