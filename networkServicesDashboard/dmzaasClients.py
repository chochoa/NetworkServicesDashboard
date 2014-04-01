from peewee import *

dmzaasClients = PostgresqlDatabase('dmzaasClients', user = 'rilogan')

class UnknownFieldType(object):
    pass

class dmzaasModel(Model):
    class Meta:
        database = dmzaasClients

class clients(dmzaasModel):
    aclreview = CharField(max_length=100, null=True)
    activityconducted = TextField(null=True)
    architecturereview = CharField(max_length=100, null=True)
    billtoid = CharField(max_length=50, null=True)
    billtoname = CharField(max_length=100, null=True)
    comments = TextField(null=True)
    connectionowner = CharField(max_length=100, null=True)
    crosscharge = CharField(max_length=100, null=True)
    engagementid = PrimaryKeyField()
    estimatedmaximumbandwidth = CharField(max_length=100, null=True)
    golivedate = DateField(null=True)
    implementation = CharField(max_length=100, null=True)
    inservice = BooleanField(null=True)
    inservicedatetime = DateTimeField(null=True)
    labid = IntegerField(null=True)
    labname = CharField(max_length=100, null=True)
    labstatus = CharField(max_length=100, null=True)
    location = CharField(max_length=100, null=True)
    othercontact = CharField(max_length=100, null=True)
    otherservices = TextField(null=True)
    plans = TextField(null=True)
    primarycontact = CharField(max_length=100, null=True)
    remedycase = TextField(null=True)
    securityinfo = BooleanField(null=True)
    servicegateway1 = CharField(max_length=100, null=True)
    servicegateway2 = CharField(max_length=100, null=True)
    status = IntegerField(null=True)
    subscriber = CharField(max_length=100, null=True)
    targetdate = DateField(null=True)
    teamname = CharField(max_length=100, null=True)
    updated = DateTimeField(null=True)
    addressspace = CharField(max_length=100, null=True)
    statustimestart = DateTimeField(null=True)
    implementationcr = CharField(max_length=100, null=True)
    assignee = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'clients'

class notes(dmzaasModel):
    content = TextField(null=True)
    engagementid = ForeignKeyField(null=True, db_column='engagementid', rel_model=clients)
    noteid = PrimaryKeyField()
    posted = DateTimeField(null=True)

    class Meta:
        db_table = 'notes'

class gateways(dmzaasModel):
    gatewayid = PrimaryKeyField()
    location = TextField()
    name = TextField()

    class Meta:
        db_table = 'gateways'

class assignees(dmzaasModel):
    assigneeid = PrimaryKeyField()
    function = TextField()
    name = TextField()

    class Meta:
        db_table = 'assignees'
