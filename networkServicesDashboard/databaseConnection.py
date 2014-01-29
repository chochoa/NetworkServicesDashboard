from peewee import *

database = PostgresqlDatabase('dbff40je858639', **{'host': 'ec2-23-23-81-171.compute-1.amazonaws.com', 'password': 'KfbMwHkzDWzzU0FmDSNsroRS0l', 'port': 5432, 'user': 'innjnankcerubt'})

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class clients(BaseModel):
    aclreview = CharField(max_length=100, null=True)
    activityconducted = TextField(null=True)
    architecturereview = CharField(max_length=100, null=True)
    billtoid = IntegerField(null=True)
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
    vapapproval = BooleanField(null=True)
    addressspace = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'clients'

class notes(BaseModel):
    content = TextField(null=True)
    engagementid = ForeignKeyField(null=True, db_column='engagementid', rel_model=clients)
    noteid = PrimaryKeyField()
    posted = DateTimeField(null=True)

    class Meta:
        db_table = 'notes'