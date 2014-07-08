CREATE TABLE newProject(
	assignee VARCHAR(255),
	currentstatus VARCHAR(255),
	projectid SERIAL PRIMARY KEY,
	projectname VARCHAR(255),
	requestor VARCHAR(255),
	mailer VARCHAR(255),
	businessunit VARCHAR(255),
	targetdate VARCHAR(255),
	alocation VARCHAR(255),
	alocationcisco VARCHAR(255),
	zlocation VARCHAR(255),
	zlocationcisco VARCHAR(255),
	circuittype VARCHAR(255),
	cost VARCHAR(255),
	billingdept VARCHAR(255),
	billingauth VARCHAR(255),
	discoveryauthyes VARCHAR(255),
	discoverystatus VARCHAR(255) DEFAULT 'Not Started',
	serviceteamcomments VARCHAR(255),
	hardwareassessment VARCHAR(255),
	securitystatus VARCHAR(255) DEFAULT 'Not Started',
	labid TEXT,
	archdocumentation VARCHAR(255),
	securityfinalreview VARCHAR(255),
	securitycase TEXT,
	designstatus VARCHAR(255) DEFAULT 'Not Started',
	circuitid VARCHAR(255),
	designdocumentation VARCHAR(255),
	linecard VARCHAR(255),
	teamreview VARCHAR(255),
	thirdparty VARCHAR(255),
	designclientapproval VARCHAR(255),
	implementationstatus VARCHAR(255) DEFAULT 'Not Started',
	crnumber TEXT,
	crdate VARCHAR(255),
	hardwareneeded VARCHAR(255),
	hardwareorderno VARCHAR(255),
	litcase VARCHAR(255),
	circuitdiagram VARCHAR(255),
	impother VARCHAR(255),
	i2ocasenumber VARCHAR(255),
	i2ocasecreated VARCHAR(255),
	i2ocasecreatedtimestamp VARCHAR(255),
	opsstatus VARCHAR(255) DEFAULT 'Not Started',
	i2ocasereleased VARCHAR(255),
	i2ocasereleasedtimestamp VARCHAR(255),
	i2ocaseaccepted VARCHAR(255),
	i2ocaseacceptedtimestamp VARCHAR(255),
	i2ocasecompleted VARCHAR(255),
	i2ocasecompletedtimestamp VARCHAR(255),
	servicestatus INTEGER
);

CREATE TABLE projectTypes (
	typeid SERIAL PRIMARY KEY,
	size VARCHAR(255),
	circuittype VARCHAR(255),
	monthlycost INTEGER
);

CREATE TABLE itaacResources (
	resourceid SERIAL PRIMARY KEY,
	resourcename VARCHAR(255),
	resourcelogin VARCHAR(255),
	resourcetype VARCHAR(255)
);

CREATE TABLE lineCards (
	cardid SERIAL PRIMARY KEY,
	cardname VARCHAR(255)
);

CREATE TABLE location (
	locationid SERIAL PRIMARY KEY,
	locationname VARCHAR(255),
	locationtype VARCHAR(255)
);