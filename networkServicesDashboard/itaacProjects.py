from peewee import *

itaacProjects = PostgresqlDatabase('itaacProjects')

class UnknownFieldType(object):
    pass

class itaacModel(Model):
    class Meta:
        database = itaacProjects

class Projects(itaacModel):
    accesstype = CharField(max_length=255, null=True)
    activity = TextField(null=True)
    buildingid_a = CharField(max_length=255, null=True)
    buildingid_b = CharField(max_length=255, null=True)
    businessimpact = TextField(null=True)
    businessunit = CharField(max_length=255, null=True)
    cellnumber_a = CharField(max_length=255, null=True)
    cellnumber_b = CharField(max_length=255, null=True)
    circuitsize = CharField(max_length=255, null=True)
    city_a = CharField(max_length=255, null=True)
    city_b = CharField(max_length=255, null=True)
    company_a = CharField(max_length=255, null=True)
    company_b = CharField(max_length=255, null=True)
    contacttitle_a = CharField(max_length=255, null=True)
    contacttitle_b = CharField(max_length=255, null=True)
    contactcompany_a = CharField(max_length=255, null=True)
    contactcompany_b = CharField(max_length=255, null=True)
    contactemail_a = CharField(max_length=255, null=True)
    contactemail_b = CharField(max_length=255, null=True)
    contactname_a = CharField(max_length=255, null=True)
    contactname_b = CharField(max_length=255, null=True)
    contactnumber_a = CharField(max_length=255, null=True)
    contactnumber_b = CharField(max_length=255, null=True)
    comments = TextField(null=True)
    deliverydate = DateField(null=True)
    department = CharField(max_length=255, null=True)
    dependencies = TextField(null=True)
    diversity = BooleanField(null=True)
    documentation = BlobField(null=True)
    floor_a = CharField(max_length=255, null=True)
    floor_b = CharField(max_length=255, null=True)
    intercampus = BooleanField(null=True)
    latency = CharField(max_length=255, null=True)
    nickname = CharField(max_length=255, null=True)
    othercontacts = TextField(null=True)
    otherinfo = TextField(null=True)
    projectid = PrimaryKeyField()
    projectname = CharField(max_length=255, null=True)
    projectscope = TextField(null=True)
    protection = BooleanField(null=True)
    requestdate = DateField(null=True)
    requestorname = CharField(max_length=255, null=True)
    requirementsurl = BlobField(null=True)
    state_a = CharField(max_length=255, null=True)
    state_b = CharField(max_length=255, null=True)
    status = IntegerField(null=True)
    street_a = CharField(max_length=255, null=True)
    street_b = CharField(max_length=255, null=True)
    teammailer = CharField(max_length=255, null=True)
    tel_a = CharField(max_length=255, null=True)
    tel_b = CharField(max_length=255, null=True)
    tmsorder = CharField(max_length=255, null=True)
    zipcode_a = CharField(max_length=255, null=True)
    zipcode_b = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'projects'

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

class Colocombo(itaacModel):
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
