from peewee import *

database = PostgresqlDatabase("dbff40je858639", host="ec2-23-23-81-171.compute-1.amazonaws.com", user="innjnankcerubt", passwd="KfbMwHkzDWzzU0FmDSNsroRS0l")
psql_db.get_conn().set_client_encoding('UTF8')

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Clients(BaseModel):
    activityconducted = CharField(max_length=500, null=True, db_column='activityConducted')
    billtoid = IntegerField(null=True, db_column='billToId')
    billtoname = CharField(max_length=100, null=True, db_column='billToName')
    case = CharField(max_length=50, null=True)
    comments = CharField(max_length=500, null=True)
    connectionowner = CharField(max_length=100, null=True, db_column='connectionOwner')
    crosscharge = CharField(max_length=10, null=True, db_column='crossCharge')
    engagementid = PrimaryKeyField(db_column='engagementId')
    estimatedmaximumbandwidth = CharField(max_length=10, null=True, db_column='estimatedMaximumBandwidth')
    golivedate = DateField(null=True, db_column='goLiveDate')
    implementation = CharField(max_length=50, null=True)
    inservice = IntegerField(null=True, db_column='inService')
    labid = IntegerField(null=True, db_column='labId')
    labname = CharField(max_length=100, null=True, db_column='labName')
    labstatus = CharField(max_length=20, null=True, db_column='labStatus')
    location = CharField(max_length=100, null=True)
    othercontact = CharField(max_length=100, null=True, db_column='otherContact')
    otherservices = CharField(max_length=500, null=True, db_column='otherServices')
    plans = CharField(max_length=500, null=True)
    primarycontact = CharField(max_length=100, null=True, db_column='primaryContact')
    securityinfo = CharField(max_length=10, null=True, db_column='securityInfo')
    securityreview = CharField(max_length=50, null=True, db_column='securityReview')
    servicegateway1 = CharField(max_length=100, null=True, db_column='serviceGateway1')
    servicegateway2 = CharField(max_length=100, null=True, db_column='serviceGateway2')
    status = IntegerField(null=True)
    subscriber = CharField(max_length=100, null=True)
    targetdate = DateField(null=True, db_column='targetDate')
    teamname = CharField(max_length=100, null=True, db_column='teamName')
    updated = DateTimeField()
    vapapproval = CharField(max_length=10, null=True, db_column='vapApproval')

    class Meta:
        db_table = 'Clients'

class Notes(BaseModel):
    noteid = PrimaryKeyField(db_column='noteId', primary_key=True)
    engagementid = ForeignKeyField(db_column='engagementId', rel_model=Clients)
    content = TextField()
    posted = DateTimeField()

    class Meta:
        db_table = 'Notes'