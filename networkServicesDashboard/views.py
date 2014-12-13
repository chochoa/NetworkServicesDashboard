from networkServicesDashboard import *
from flask import render_template, redirect, make_response, request, Response, send_from_directory
from datetime import datetime, timedelta
from functools import wraps
import calendar
import time
import smtplib
import re

#Databases
from dmzaasClients import *
from itaacProjects import *

###Note: Project Status is as follows:
	#1: In Service
	#2: In Progress
	#3: Widthdrawn/Declined

#############################
#	   General functions	#
#############################

def check_auth(username, password):
    return username == 'admin' and password == 'NetworkServices'

def authenticate():
    return Response('Incorrect Username + Password :(', 401,{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#############################
# General Application Views #
#############################


# Logic to create a note
@app.route('/corporateNetwork/itaac/newNote', methods=['POST'])
def newItaacNote():
	project = request.form['projectid']
	noteContent = request.form['noteContent']
	newNote = itaacNotes.insert(projectid = project, content = noteContent)
	updateProject = NewProject.update(timeupdated = datetime.now()).where(NewProject.projectid == project)
	newNote.execute()
	updateProject.execute()
	return redirect('/corporateNetwork/itaac/project?id=' + project)

@app.route('/corporateNetwork/itaac/deleteNote', methods = ['POST'])
@requires_auth
def deleteItaacNote():
	noteid = request.form['noteid']
	delete = itaacNotes.delete().where(itaacNotes.noteid == int(request.form['noteid']))
	updateProject = NewProject.update(timeupdated = datetime.now()).where(NewProject.projectid == request.form['project'])
	delete.execute()
	updateProject.execute()
	return redirect('/corporateNetwork/itaac/project?id=' + str(request.form['project']))

@app.route('/corporateNetwork/itaac/pocs')
def itaacPocs():
	return render_template('corporateNetwork/itaac/pocs.html', projects = NewProject.select().where(NewProject.servicestatus == 1))

@app.route('/corporateNetwork/itaac/billing')
def itaacBilling():
	return render_template('corporateNetwork/itaac/billing.html', projects = NewProject.select().where(NewProject.servicestatus == 1))

@app.route('/corporateNetwork/itaac/billing/download')
def downloaditaacBillingReport():
	csv = 'ProjectID, Project Name, Requestor, A Location, Z Location, Target Date, Current Status, Authoriser, Department, Cost\r\n'
	for project in NewProject.select().where(NewProject.servicestatus == 1):
		csv += '"' + str(project.projectid) + '","' + str(project.projectname.strip()) + '","' + str(project.requestor) + '","' + str(project.alocation.strip()) + '","' + str(project.zlocation.strip()) + '","' + str(project.targetdate.strip()) + '","' + str(project.currentstatus.strip()) + '","' + str(project.billingauth.strip()) + '","' + str(project.billingdept.strip()) + '","' + str(project.cost.strip()) + '"\r\n'
	response = make_response(csv)
	response.headers["Content-Disposition"] = "attatchment; filename=" + time.strftime("%d/%m/%Y") + "_itaacBilling.csv"
	return response

@app.route('/corporateNetwork/itaac/project')
def itaacProject():
	projectid = request.args.get('id', '')
	project = NewProject.get(NewProject.projectid == projectid)

	try:
		latestNote = itaacNotes.select().where(itaacNotes.projectid == projectid).order_by(itaacNotes.updated.desc()).limit(1).get()
		latestNote.updated = (latestNote.updated).strftime("%Y-%m-%d %H:%M:%S")
	except itaacNotes.DoesNotExist:
		latestNote = {}
		latestNote['content'] = "No notes found"

	allNotes = itaacNotes.select().where(itaacNotes.projectid == projectid).order_by(itaacNotes.updated.desc())
	for note in allNotes:
		note.updated = (note.updated).strftime("%Y-%m-%d %H:%M:%S")

	resourceList = {}
	resourcetypes = []
	for resource in ITaaCResources.select():
		resourcetypes.append(resource.resourcetype)
	resourcetypes = list(set(resourcetypes))
	for resourcetype in resourcetypes:
		resourceList[resourcetype] = ITaaCResources.select().where(ITaaCResources.resourcetype == resourcetype)

	locationList = {}
	locationtypes = []
	for location in Location.select():
		locationtypes.append(location.locationtype)
	locationtypes = list(set(locationtypes))
	for locationtype in locationtypes:
		locationList[locationtype] = Location.select().where(Location.locationtype == locationtype)

	projectTypesList = {}
	circuitTypesList = []
	for projectType in ProjectTypes.select():
		circuitTypesList.append(projectType.circuittype)
	circuitTypesList = list(set(circuitTypesList))
	for circuittype in circuitTypesList:
		projectTypesList[circuittype] = ProjectTypes.select().where(ProjectTypes.circuittype == circuittype)

	if ((project.crnumber != None) and (project.crnumber != '')):
		cases = project.crnumber.split(';')
		crnumbers = ''
		for case in cases:
			if case[:3] == "INC":
				crnumbers += "<a href='http://case/" + case + "' target='_blank'>" + case + "</a><br />"
			elif case[:3] == "CRQ" or case[:3] == "RFC":
				crnumbers += "<a href='http://rfc/" + case + "' target='_blank'>" + case + "</a><br />"
			else:
				crnumbers += case + "<br />"
	else:
		crnumbers = ''

	if ((project.securitycase != None) and (project.securitycase != '')):
		cases = project.securitycase.split(';')
		securitycases = ''
		for case in cases:
			if case[:3] == "INC":
				securitycases += "<a href='http://case/" + case + "' target='_blank'>" + case + "</a><br />"
			elif case[:3] == "CRQ" or case[:3] == "RFC":
				securitycases += "<a href='http://rfc/" + case + "' target='_blank'>" + case + "</a><br />"
			else:
				securitycases += case + "<br />"
	else:
		securitycases = ''

	if ((project.labid != None) and (project.labid != '')):
		cases = project.labid.split(';')
		labids = ''
		for case in cases:
			labids += "<a href='http://eman-core.cisco.com/infosec/labreg/view.pcgi?lab_id=" + case + "' target='_blank'>" + case + "</a><br />"
	else:
		labids = ''

	return render_template('/corporateNetwork/itaac/project.html', project=project, resources = resourceList, resourcetypes = resourcetypes, projectTypes = projectTypesList, circuitTypes = circuitTypesList, lineCards = LineCards.select(), locations = locationList, locationtypes = locationtypes, splitcrnumbers = crnumbers, splitsecuritycases = securitycases, splitlabids = labids, lastNote = latestNote, notes = allNotes)

@app.route('/corporateNetwork/itaac/addProject')
def itaacAddNewProject():
	locationList = {}
	locationtypes = []
	for location in Location.select():
		locationtypes.append(location.locationtype)
	locationtypes = list(set(locationtypes))
	for locationtype in locationtypes:
		locationList[locationtype] = Location.select().where(Location.locationtype == locationtype)


	projectTypesList = {}
	circuitTypesList = []
	for projectType in ProjectTypes.select():
		circuitTypesList.append(projectType.circuittype)
	circuitTypesList = list(set(circuitTypesList))
	for circuittype in circuitTypesList:
		projectTypesList[circuittype] = ProjectTypes.select().where(ProjectTypes.circuittype == circuittype)
	return render_template('/corporateNetwork/itaac/addProject.html', projectTypes = projectTypesList, circuitTypes = circuitTypesList, locations = locationList, locationtypes = locationtypes)

@app.route('/corporateNetwork/itaac/addingProject', methods=['POST'])
def itaacAddingNewProject():
	newProject = NewProject.insert(
		timeupdated = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M"),
		servicestatus = 2,
		currentstatus = "New Request",
		projectname =  request.form['projectname'],
		requestor =  request.form['requestor'],
		mailer =  request.form['mailer'],
		businessunit =  request.form['businessunit'],
		targetdate =  request.form['targetdate'],
		alocation = request.form['alocation'],
		alocationcisco = request.form['alocationcisco'],
		zlocation = request.form['zlocation'],
		zlocationcisco = request.form['zlocationcisco'],
		circuittype =  request.form['circuittype'],
		cost =  request.form['cost'],
		billingdept =  request.form['billingdept'],
		billingauth =  request.form['billingauth'],
		discoveryauthyes = request.form['discoveryauthyes'])
	newProject.execute()
	return redirect('/corporateNetwork/itaac')

@app.route('/corporateNetwork/itaac/editingProject', methods=['POST'])
def itaacEditingProject():
	# Need to handle empty checkboxes
	hardwareneededCheck = ''
	try:
		hardwareneededCheck = request.form['hardwareneeded']
	except KeyError, e:
		hardwareneededCheck = 'off'

	i2ocasecreatedCheck = ''
	try:
		i2ocasecreatedCheck = request.form['i2ocasecreated']
	except KeyError, e:
		i2ocasecreated = 'off'

	i2ocasereleasedCheck = ''
	try:
		i2ocasereleasedCheck = request.form['i2ocasereleased']
	except KeyError, e:
		i2ocasereleased = 'off'

	i2ocaseacceptedCheck = ''
	try:
		i2ocaseacceptedCheck = request.form['i2ocaseaccepted']
	except KeyError, e:
		i2ocaseaccepted = 'off'

	i2ocasecompletedCheck = ''
	try:
		i2ocasecompletedCheck = request.form['i2ocasecompleted']
	except KeyError, e:
		i2ocasecompleted = 'off'

	newservicestatus = 2
	finalStatus = ""
	if request.form['opsstatus'] == "Completed":
		finalStatus = "Operations: Completed"
	elif request.form['opsstatus'] == "In Progress":
		finalStatus = "Operations: In Progress"
	elif request.form['implementationstatus'] == "Completed":
		finalStatus = "Implementation: Completed"
	elif request.form['implementationstatus'] == "In Progress":
		finalStatus = "Implementation: In Progress"
	elif request.form['designstatus'] == "Completed":
		finalStatus = "Design: Completed"
	elif request.form['designstatus'] == "In Progress":
		finalStatus = "Design: In Progress"
	elif request.form['securitystatus'] == "Completed" or request.form['securitystatus'] == "Not Needed":
		finalStatus = "Security Review: Completed"
	elif request.form['securitystatus'] == "In Progress":
		finalStatus = "Security Review: In Progress"
	elif request.form['discoverystatus'] == "Completed":
		finalStatus = "Discovery: Completed"
	elif request.form['discoverystatus'] == "In Progress":
		finalStatus = "Discovery: In Progress"
	else:
		finalStatus = "New Request"

	statuses = ['discoverystatus', 'securitystatus', 'designstatus', 'implementationstatus', 'opsstatus']
	ticker = 0
	for status in statuses:
		if request.form[status] == "Completed" or request.form[status] == "Not Needed":
			ticker += 1
	if ticker == 5:
			finalStatus = "In Service"
			newservicestatus = 1
	if request.form['discoverystatus'] == "Project Declined":
		finalStatus = "Project Declined"
		newservicestatus = 3

	updatedProject = NewProject.update(
		timeupdated = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M"),
		servicestatus = newservicestatus,
		assignee = request.form['assignee'],
		projectname = request.form['projectname'],
		requestor = request.form['requestor'],
		mailer = request.form['mailer'],
		businessunit = request.form['businessunit'],
		targetdate = request.form['targetdate'],
		alocation = request.form['alocation'],
		alocationcisco = request.form['alocationcisco'],
		zlocation = request.form['zlocation'],
		zlocationcisco = request.form['zlocationcisco'],
		circuittype = request.form['circuittype'],
		cost = request.form['cost'],
		currentstatus = finalStatus,
		billingdept = request.form['billingdept'],
		billingauth = request.form['billingauth'],
		discoveryauthyes = request.form['discoveryauthyes'],
		discoverystatus = request.form['discoverystatus'],
		serviceteamcomments = request.form['serviceteamcomments'],
		hardwareassessment = request.form['hardwareassessment'],
		securitystatus = request.form['securitystatus'],
		labid = request.form['labid'],
		archdocumentation = request.form['archdocumentation'],
		securityfinalreview = request.form['securityfinalreview'],
		securitycase = request.form['securitycase'],
		designstatus = request.form['designstatus'],
		circuitid = request.form['circuitid'],
		designdocumentation = request.form['designdocumentation'],
		linecard = request.form['linecard'],
		teamreview = request.form['teamreview'],
		thirdparty = request.form['thirdparty'],
		designclientapproval = request.form['designclientapproval'],
		implementationstatus = request.form['implementationstatus'],
		crnumber = request.form['crnumber'],
		crdate = request.form['crdate'],
		hardwareneeded = hardwareneededCheck,
		hardwareorderno = request.form['hardwareorderno'],
		litcase = request.form['litcase'],
		circuitdiagram = request.form['circuitdiagram'],
		impother = request.form['impother'],
		i2ocasenumber = request.form['i2ocasenumber'],
		i2ocasecreated = i2ocasecreatedCheck,
		i2ocasecreatedtimestamp = request.form['i2ocasecreatedtimestamp'],
		i2ocasereleased = i2ocasereleasedCheck,
		i2ocasereleasedtimestamp = request.form['i2ocasereleasedtimestamp'],
		opsstatus = request.form['opsstatus'],
		i2ocaseaccepted = i2ocaseacceptedCheck,
		i2ocaseacceptedtimestamp = request.form['i2ocaseacceptedtimestamp'],
		i2ocasecompleted = i2ocasecompletedCheck,
		i2ocasecompletedtimestamp = request.form['i2ocasecompletedtimestamp']).where(NewProject.projectid == request.form['projectid'])
	updatedProject.execute()

	return redirect('/corporateNetwork/itaac/project?id=' + request.form['projectid'])

@app.route('/corporateNetwork/itaac/deleteProject', methods=['POST'])
def deletingItaacProject():
	deletedProject = NewProject.delete().where(NewProject.projectid == request.form['projectid'])
	deletedProject.execute()
	return redirect('/corporateNetwork/itaac')

@app.route('/corporateNetwork/itaac/addingProjectType', methods=['POST'])
def itaacAddingProjectType():
	newProjectType = ProjectTypes.insert(
		monthlycost = request.form['projectTypeCost'],
		size = request.form['projectTypeSize'],
		circuittype = request.form['projectTypeType'])
	newProjectType.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/deletingProjectType', methods=['POST'])
def itaacDeletingProjectType():
	deleteProjectType = ProjectTypes.delete().where(ProjectTypes.typeid == request.form['typeid'])
	deleteProjectType.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/addingLineCard', methods=['POST'])
def itaacAddingLineCard():
	newLineCard = LineCards.insert(
		cardname = request.form['cardname'])
	newLineCard.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/deletingLineCard', methods=['POST'])
def itaacDeletingLineCard():
	deleteLineCard = LineCards.delete().where(LineCards.cardid == request.form['cardid'])
	deleteLineCard.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/addingLocation', methods=['POST'])
def itaacAddingLocation():
	newLocation = Location.insert(
		locationname = request.form['locationname'],
		locationtype = request.form['locationtype'])
	newLocation.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/deletingLocation', methods=['POST'])
def itaacDeletingLocation():
	deleteLocation = Location.delete().where(Location.locationid == request.form['locationid'])
	deleteLocation.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/addingResource', methods=['POST'])
def itaacAddingResource():
	newItaacResource = ITaaCResources.insert(
		resourcelogin = request.form['resourcelogin'],
		resourcename = request.form['resourcename'],
		resourcetype = request.form['resourcetype'])
	newItaacResource.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/deletingResource', methods=['POST'])
def itaacDeletingResource():
	deleteResource = ITaaCResources.delete().where(ITaaCResources.resourceid == request.form['resourceid'])
	deleteResource.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/itaac/circuitList')
def circuitList():
	return render_template('corporateNetwork/itaac/circuitList.html', circuits = Circuits.select())

@app.route('/corporateNetwork/itaac/coloInfo')
def coloInfo():
	return render_template('corporateNetwork/itaac/coloInfo.html', coloInfo = ColoCombo.select())

# In Progress ITaaC Projects
@app.route('/corporateNetwork/itaac')
def itaac():
	return render_template('corporateNetwork/itaac/inProgress.html', projects = NewProject.select().where(NewProject.servicestatus == 2))

# Completed Projects
@app.route('/corporateNetwork/itaac/completed')
def itaacCompletedProjects():
	return render_template('corporateNetwork/itaac/completed.html', projects = NewProject.select().where(NewProject.servicestatus == 1))

##################################################################################################################################################

#Index Page
@app.route('/')
def index():
	return redirect('/corporateNetwork/dmz')

#Admin Interface
@app.route('/admin')
@requires_auth
def adminInterface():
	locations = []
	for gateway in gateways.select():
		locations.append(gateway.location)
	locations = list(set(locations))
	return render_template('/admin.html', assignees = assignees.select(), gateways = gateways.select(), locations = locations, projectTypes = ProjectTypes.select(), itaacResources = ITaaCResources.select(), lineCards = LineCards.select(), itaacLocations = Location.select())

@app.route('/corporateNetwork/dmz/addingAssignee', methods=['POST'])
def addingAssignee():
	newAssignee = assignees.insert(name = request.form['assigneeName'], function = request.form['assigneeFunction'])
	newAssignee.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/dmz/deletingAssignee', methods=['POST'])
def deletingAssingee():
	deleteAssignee = assignees.delete().where(assignees.assigneeid == request.form['assigneeid'])
	deleteAssignee.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/dmz/addingGateway', methods=['POST'])
def addingGateway():
	newGateway = gateways.insert(name = request.form['gatewayName'], location = request.form['gatewayLocation'])
	newGateway.execute()
	return redirect('/admin')

@app.route('/corporateNetwork/dmz/deletingGateway', methods=['POST'])
def deletingGateway():
	deleteGateway = gateways.delete().where(gateways.gatewayid == request.form['gatewayid'])
	deleteGateway.execute()
	return redirect('/admin')

@app.route('/help')
def help():
	return render_template('/help/functionality.html')

@app.route('/help/technical')
def helpTechnical():
	return render_template('/help/technical.html')

@app.route('/help/develop')
def helpDevelop():
	return render_template('/help/developing.html')

@app.route('/tutorial')
def tutorial():
	return render_template('/tutorial.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

################
# DMZaaS Views #
################

# In Progress Clients Summary Table
@app.route('/corporateNetwork/dmz')
def dmzInProgress():
	html = ''
	for client in clients.select():
		if client.status == 2:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M")

			timeInStatus = (datetime.fromtimestamp(time.time()) - client.statustimestart).days
			if timeInStatus <= 14:
				colorClass = "success"
			elif timeInStatus <= 60:
				colorClass = "warning"
			else:
				colorClass = "danger"

			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + str(client.location) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.assignee) + '''</td>
							<td>''' + str(client.updated) + '''</td>
							<td class="''' + colorClass + '''">''' + str(timeInStatus) + ''' days</td>
						</tr>
					'''

	return render_template('corporateNetwork/dmz/inProgress.html', inProgressClients = html)

@app.route('/corporateNetwork/dmz/smo')
def dmzInProgressSMO():
	inProgressClients = clients.select().where(clients.status == 2)
	return render_template('corporateNetwork/dmz/smo.html', clients = inProgressClients)

# In Service Clients Summary Table
@app.route('/corporateNetwork/dmz/inService')
def dmzInService():
	html = ''
	totalCrossCharge = 0
	for client in clients.select():
		if client.status == 1:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M")
			if client.crosscharge == "" or client.crosscharge == None:
				client.crosscharge = 0
			totalCrossCharge += int(client.crosscharge)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + str(client.location) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.crosscharge) + '''</td>
							<td>''' + str(client.golivedate) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmz/inService.html', inServiceClients = html, totalCrossCharge = totalCrossCharge)

# Withdrawn Clients Summary Table
@app.route('/corporateNetwork/dmz/withdrawn')
def dmzWithdrawn():
	html = ''
	for client in clients.select():
		if client.status == 3:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M")
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmz/withdrawn.html', withdrawnClients = html)

# Individual Client Profiles
@app.route('/corporateNetwork/dmz/client')
def client():
	clientId = request.args.get('id', '')
	client = clients.get(clients.engagementid == clientId)

	result = getProgress(client)
	status = result['status']
	bar = result['bar']

	notesHtml = getNotes(client)
	lastNote = getLatestNote(client)

	if lastNote == None:
		lastNoteDate = ''
		lastNoteContent = "N/A"
	else:
		lastNote.posted = (lastNote.posted).strftime("%Y-%m-%d %H:%M")
		lastNoteDate = str(lastNote.posted)
		lastNoteContent = str(lastNote.content)

	if ((client.remedycase != None) and (client.remedycase != '')):
		cases = client.remedycase.split(';')
		remedycases = ''
		for case in cases:
			if case[:3] == "INC":
				remedycases += "<a href='http://case/" + case + "' target='_blank'>" + case + "</a><br />"
			elif case[:3] == "CRQ" or case[:3] == "RFC":
				remedycases += "<a href='http://rfc/" + case + "' target='_blank'>" + case + "</a><br />"
			else:
				remedycases += case + "<br />"
	else:
		remedycases = ''

	if ((client.implementationcr != None) and (client.implementationcr != '')):
		crs = client.implementationcr.split(';')
		remedycrs = ''
		for cr in crs:
			if cr[:3]== "INC":
				remedycrs += "<a href='http://case/" + cr + "' target='_blank'>" + cr + "</a><br />"
			elif cr[:3] == "CRQ" or cr[:3] == "RFC":
				remedycrs += "<a href='http://rfc/" + cr + "' target='_blank'>" + cr + "</a><br />"
			else:
				remedycrs += cr + "<br />"
	else:
		remedycrs = ''

	timeInStatus = (datetime.fromtimestamp(time.time()) - client.statustimestart).days

	gatewayList = {}
	locations = []
	for gateway in gateways.select():
		locations.append(gateway.location)
	locations = list(set(locations))
	for location in locations:
		gatewayList[location] = gateways.select().where(gateways.location == location)

	assigneeList = {}
	functions = []
	for assignee in assignees.select():
		functions.append(assignee.function)
	functions = list(set(functions))
	for function in functions:
		assigneeList[function] = assignees.select().where(assignees.function == function)

	return render_template('corporateNetwork/dmz/client.html', assignees = assigneeList, gateways = gatewayList, locations = locations, functions = functions, clientArray = client, progress = bar, currentStatus = status, time = timeInStatus, printNotes = notesHtml, lastDate = lastNoteDate, lastContent = lastNoteContent, splitcases = remedycases, splitcrs = remedycrs)

# New Client Form
@app.route('/corporateNetwork/dmz/addClient')
def dmzAddClient():
	gatewayList = {}
	locations = []
	for gateway in gateways.select():
		locations.append(gateway.location)
	locations = list(set(locations))
	for location in locations:
		gatewayList[location] = gateways.select().where(gateways.location == location)

	return render_template('corporateNetwork/dmz/addClient.html', gateways = gatewayList, locations = locations)

# Logic to add a new client to the database
@app.route('/corporateNetwork/dmz/addingClient', methods=['POST'])
def addingClient():
	if int(request.form['inservice']) == 1:
		newStatus = 1
	else:
		newStatus = 2

	newGoLiveDate = request.form['golivedate']
	if newGoLiveDate == "":
		newGoLiveDate = None

	newTargetDate = request.form['targetdate']
	if newTargetDate == "":
		newTargetDate = None

	newLabId = request.form['labid']
	if newLabId == '':
		newLabId = None

	departmentid = str(request.form['billtoid'])
	if departmentid == '':
		departmentid = None

	if len(request.form.getlist('servicegateways')) == 0:
		gateway1 = None
		gateway2 = None
	elif len(request.form.getlist('servicegateways')) == 1:
		gateway1 = str(request.form.getlist('servicegateways')[0])
		gateway2 = None
	else:
		gateway1 = str(request.form.getlist('servicegateways')[0])
		gateway2 = str(request.form.getlist('servicegateways')[1])

	newClient = clients.insert(
					    activityconducted = request.form['activityconducted'],
    					billtoid = str(departmentid),
    					billtoname = request.form['billtoname'],
    					remedycase = request.form['remedycase'],
    					implementationcr = request.form['implementationcr'],
    					comments = request.form['comments'],
    					connectionowner = request.form['connectionowner'],
    					crosscharge = request.form['crosscharge'],
    					estimatedmaximumbandwidth = request.form['estimatedmaximumbandwidth'],
    					golivedate = newGoLiveDate,
    					implementation = request.form['implementation'],
    					inservice = int(request.form['inservice']),
    					labid = newLabId,
    					labname = request.form['labname'],
    					labstatus = request.form['labstatus'],
    					location = request.form['location'],
    					othercontact = request.form['othercontact'],
    					otherservices = request.form['otherservices'],
    					plans = request.form['plans'],
    					primarycontact = request.form['primarycontact'],
    					securityinfo = int(request.form['securityinfo']),
    					architecturereview = request.form['architecturereview'],
    					aclreview = request.form['aclreview'],
    					servicegateway1 = gateway1,
    					servicegateway2 = gateway2,
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
						addressspace = request.form['addressspace'],
						statustimestart = datetime.fromtimestamp(time.time()))
	newClient.execute()

	nextid = 0
	for result in dmzaasClients.execute_sql('SELECT MAX(engagementid) FROM clients'):
		nextid = result[0]

	return redirect('/corporateNetwork/dmz/client?id=' + str(nextid))

# Cross Charge Reports
@app.route('/corporateNetwork/dmz/report')
def dmzReport():
	html = ""
	departments = {}
	totalCrossCharge = 0
	for client in clients.select().where(clients.inservice == True):
		departments.update({client.billtoid:client.billtoname})
		if client.crosscharge == '' or client.crosscharge == None:
			client.crosscharge = 0
		totalCrossCharge += int(client.crosscharge)

	html += "<h2>DMZaaS Cross Charge Report<span class='pull-right'>Total: $" + str(totalCrossCharge) + "</span></h2><hr />"

	for departmentId, departmentName in departments.iteritems():
		totalDepartmentCharge = 0
		for client in clients.select().where((clients.billtoid == departmentId) & (clients.inservice == True)):
			if client.crosscharge == '' or client.crosscharge == None:
				client.crosscharge = 0
			totalDepartmentCharge += int(client.crosscharge)
		html += "<h3>" + departmentId + " <small>" + departmentName + "</small></h3><span class='pull-right' style='font-weight:bold'>$ " + str(totalDepartmentCharge) + "</span>"

		html += "<table class='table table-condensed'><tbody>"
		for client in clients.select().where((clients.billtoid == departmentId) & (clients.inservice == True)):
			if client.crosscharge == '' or client.crosscharge == None:
				client.crosscharge = 0
			html += '''<tr>
						<td style='width:75%;'>''' + client.subscriber + '''</td>
						<td style='width:75%;'>$ ''' + str(client.crosscharge) + '''</td>
					</tr>'''
		html += "</tbody></table>"

	return render_template('/corporateNetwork/dmz/report.html', costReport = html)

# Primary point of contact report
@app.route('/corporateNetwork/dmz/pocs')
def dmzaasPocs():
	return render_template('/corporateNetwork/dmz/contacts.html', clients = clients.select().where(clients.status == 1))

@app.route('/corporateNetwork/dmz/billing')
def dmzRez():
	return render_template('/corporateNetwork/dmz/billing.html', clients = clients.select().where(clients.status == 1))

# Primary point of contact report
@app.route('/corporateNetwork/dmz/billing')
def dmzBillingReport():
	return render_template('/corporateNetwork/billing.html', clients = clients.select().where(clients.status == 1))

@app.route('/corporateNetwork/dmz/billing/download')
def downloadDMZBillingReport():
	csv = 'SubscriberID, Lab ID, Subscriber, Location, Department ID, Department Name, Status, Go Live Date, Monthly Recovery\r\n'
	for client in clients.select().where(clients.status == 1):
		csv += '"' + str(client.engagementid) + '","' + str(client.labid) + '","' + str(client.subscriber.strip()) + '","' + str(client.location.strip()) + '","' + str(client.billtoid.strip()) + '","' + str(client.billtoname.strip()) + '","' + str(client.status.strip()) + '","' + str(client.golivedate.strip()) + '","' + str(client.crosscharge.strip()) + '"\r\n'
	response = make_response(csv)
	response.headers["Content-Disposition"] = "attatchment; filename=" + time.strftime("%d/%m/%Y") + "_dmzaasBilling.csv"
	return response

# Logic to withdrawn a client
@app.route('/corporateNetwork/dmz/withdrawClient', methods=['POST'])
@requires_auth
def dmzWithdrawClient():
	withdrawnClient = clients.update(status = 3).where(clients.engagementid == request.form['clientId'])
	withdrawnClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientId'])

# Logic to delete a client
@app.route('/corporateNetwork/dmz/deleteClient', methods=['POST'])
@requires_auth
def dmzDeleteClient():
	noteList = getNotesByClient(request.form['clientId'])
	for note in noteList:
		noteid = note.noteid
		deleteNote = notes.delete().where(notes.noteid == noteid)
		deleteNote.execute()
	deleteClient = clients.delete().where(clients.engagementid == request.form['clientId'])
	deleteClient.execute()
	return redirect('/corporateNetwork/dmz')

# Logic to edit a client
@app.route('/corporateNetwork/dmz/editClient', methods=['POST'])
@requires_auth
def editClient():
	isInService = int(request.form['inservice'])
	newStatus = 2
	if isInService == 1:
		newStatus = 1

	newGoLiveDate = request.form['golivedate']
	if newGoLiveDate == "" or newGoLiveDate == "None":
		newGoLiveDate = None

	newTargetDate = request.form['targetdate']
	if newTargetDate == "" or newTargetDate == "None":
		newTargetDate = None

	newLabId = request.form['labid']
	if newLabId == '' or newLabId == "None":
		newLabId = None

	newDepartmentId = str(request.form['departmentid'])
	if newDepartmentId == '' or newDepartmentId == "None":
		newDepartmentId = None

	client = clients.get(clients.engagementid == request.form['clientid'])
	updateFlag = 0
	if ((client.securityinfo != int(request.form['securityinfo'])) or (client.architecturereview != request.form['architecturereview']) or (client.addressspace != request.form['addressspace']) or (client.aclreview != request.form['aclreview']) or (client.implementation != request.form['implementation']) or (client.inservice != int(request.form['inservice']))):
		updateFlag = 1

	if len(request.form.getlist('servicegateways')) == 0:
		gateway1 = None
		gateway2 = None
	elif len(request.form.getlist('servicegateways')) == 1:
		gateway1 = str(request.form.getlist('servicegateways')[0])
		gateway2 = None
	else:
		gateway1 = str(request.form.getlist('servicegateways')[0])
		gateway2 = str(request.form.getlist('servicegateways')[1])

	onHoldStatus = request.form['onhold']
	if onHoldStatus == "False" or onHoldStatus == False:
		onHoldStatus = 0
	elif onHoldStatus == "True" or onHoldStatus == True:
		onHoldStatus = 1
	else:
		onHoldStatus = None

	updatedClient = clients.update(
					    activityconducted = request.form['activityconducted'],
					    assignee = request.form['assignee'],
    					billtoid = str(newDepartmentId),
    					billtoname = request.form['departmentname'],
    					remedycase = request.form['remedycase'],
    					implementationcr = request.form['implementationcr'],
    					comments = request.form['comments'],
    					connectionowner = request.form['connectionowner'],
    					crosscharge = request.form['crosscharge'],
    					estimatedmaximumbandwidth = request.form['maxbandwidth'],
    					golivedate = newGoLiveDate,
    					implementation = request.form['implementation'],
    					inservice = isInService,
    					labid = newLabId,
    					labname = request.form['labname'],
    					labstatus = request.form['labstatus'],
    					location = request.form['location'],
    					othercontact = request.form['othercontact'],
    					otherservices = request.form['otherservices'],
    					onhold = onHoldStatus,
    					plans = request.form['plans'],
    					primarycontact = request.form['primarycontact'],
    					securityinfo = int(request.form['securityinfo']),
    					architecturereview = request.form['architecturereview'],
    					aclreview = request.form['aclreview'],
    					servicegateway1 = gateway1,
    					servicegateway2 = gateway2,
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
    					addressspace = request.form['addressspace']).where(clients.engagementid == request.form['clientid'])
	updatedClient.execute()

	if updateFlag == 1:
		updatedClient = clients.update(statustimestart = str(datetime.fromtimestamp(time.time()))).where(clients.engagementid == request.form['clientid'])
		updatedClient.execute()

		# Status Change E-Mail
		# if (client.assignee != None) and (client.assignee != ""):
		# 	sender = '"DMZ-Service" <dmz-service@cisco.com>'
		# 	login = re.search(r"\(([A-Za-z0-9_]+)\)", client.assignee)
		# 	recipient = str(login.group(1)) + "@cisco.com"
		# 	subject = "DMZaaS: " + str(client.subscriber)
		# 	message = "Hello,\n\nThis is an automated mail informing you that the DMZaaS deployment " + str(client.subscriber).upper() + " has been updated and you are currently listed as the assignee for this project.\n\nPlease check the information at http://networkservices-dev/corporateNetwork/dmz/client?id=" + str(client.engagementid) + " and complete any required action.\n\nIf you believe this wrongly assigned or need more information, please reply to dmz-service@cisco.com.\n\nMany thanks,\n\nThe DMZ-Service Team."
		# 	server = smtplib.SMTP('outbound.cisco.com')
		# 	m = "From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: networkservices-dev.cisco.com\r\n\r\n" % (sender, recipient, subject)
		# 	server.sendmail(sender, recipient, m+message)
		# 	server.quit()

	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientid'])

# Logic to create a note
@app.route('/corporateNetwork/dmz/newNote', methods=['POST'])
def newNote():
	client = request.form['clientId']
	noteContent = request.form['noteContent']
	newNote = notes.insert(engagementid = client, content = noteContent)
	updateClient = clients.update(updated = datetime.now()).where(clients.engagementid == client)
	newNote.execute()
	updateClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + client)

# @app.route('/corporateNetwork/dmz/editNote', methods=['POST'])
# def editNote():
# 	noteid = request.form['noteid']
# 	newContent = request.form['newContent']
# 	updatedNote = notes.update(content = newContent).where(notes.noteid == int(request.form['noteid']))
# 	updatedNote.execute()
# 	return redirect('/corporateNetwork/dmz/client?id=' + str(request.form['engagementid']))

# Logic to delete a note
@app.route('/corporateNetwork/dmz/deleteNote', methods = ['POST'])
@requires_auth
def deleteNote():
	noteid = request.form['noteid']
	delete = notes.delete().where(notes.noteid == int(request.form['noteid']))
	updateClient = clients.update(updated = datetime.now()).where(clients.engagementid == request.form['engagementid'])
	delete.execute()
	updateClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + str(request.form['engagementid']))

# Computes the status of a client
def getProgress(client):
	if client.status == 3:
		result = {}
		result['status'] = 'Withdrawn'
		result['bar'] =  '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">
    				<span class="sr-only">100% Complete (danger)</span>
  				</div>
			</div>'''
		return result

	if client.inservice == 1:
		result = {}
		result['status'] = 'In Service'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">
    				<span class="sr-only">100% Complete (success)</span>
  				</div>
			</div>'''
		return result

	if client.onhold == 1:
		result = {}
		result['status'] = 'On Hold'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">
    				<span class="sr-only">100% Complete (success)</span>
  				</div>
			</div>'''
		return result

	if client.implementation == 'Completed':
		result = {}
		result['status'] = 'Implementation Completed'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 75%">
    				<span class="sr-only">75% Complete (success)</span>
  				</div>
			</div>'''
		return result

	if client.implementation == 'In Progress':
		result = {}
		result['status'] = 'Implementation in progress'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 75%">
    				<span class="sr-only">75% Complete (warning)</span>
  				</div>
			</div>'''
		return result

	if (client.architecturereview == 'Completed') and (client.aclreview == 'Completed'):
		result = {}
		result['status'] = 'Security Review completed'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (success)</span>
  				</div>
			</div>'''
		return result

	if (client.architecturereview == 'In Progress') or (client.aclreview == 'In Progress'):
		result = {}
		result['status'] = 'Security Review in progress'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (warning)</span>
  				</div>
			</div>'''
		return result

	if client.securityinfo == 0 or client.securityinfo == None:
		result = {}
		result['status'] = 'Initially engaged/collecting information'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100" style="width: 25%">
    				<span class="sr-only">25% Complete</span>
  				</div>
			</div>'''
		return result

	if client.securityinfo == 1:
		result = {}
		result['status'] = 'Security Review not started'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (Danger)</span>
  				</div>
			</div>'''
		return result

# Returns list of all notes by client
def getNotesByClient(clientid):
	noteList = []
	for note in notes.select().join(clients).where(clients.engagementid == clientid).order_by(notes.posted.desc()):
		noteList.append(note)
	return noteList

# Get all notes for a client
def getNotes(client):
	html = ''
	for note in notes.select().join(clients).where(clients.engagementid == client.engagementid).order_by(notes.posted.desc()):
		note.posted = (note.posted).strftime("%Y-%m-%d %H:%M:%S")
		html += '''
			<div class="well">
				<form method="POST" action="/corporateNetwork/dmz/deleteNote" onsubmit='return confirm(&quot;Do you really want to delete this note?&quot;);'>
					<input type="hidden" name="noteid" value="''' + str(note.noteid) + '''">
					<input type="hidden" name="engagementid" value="''' + str(client.engagementid) + '''">
					<input type="submit" class="close" aria-hidden="true" value="&times;">
				</form>
				<h4>''' + str(note.posted) + '''</h4>
				<p>''' + str(note.content) + '''</p>
			</div>'''
	return html

# Gets the latest note for a client
def getLatestNote(client):
	for note in notes.select().join(clients).where(clients.engagementid == client.engagementid).order_by(notes.posted.desc()):
		return note

###################
# OLD ITaaC Views #
###################

# # Form to add new ITaaC Project
# @app.route('/corporateNetwork/itaac/addProject')
# def itaacAddProject():
# 	return render_template('corporateNetwork/itaac/addProject.html')

# # Display details of ITaaC project
# @app.route('/corporateNetwork/itaac/project')
# def itaacViewProject():
# 	project = Projects.get(Projects.projectid == request.args.get('id', ''))
# 	return render_template('corporateNetwork/itaac/project.html', project = project)

# # Logic to add new ITaaC project
# @app.route('/corporateNetwork/itaac/addingProject', methods=['POST'])
# def itaacAddingProject():
# 	# File Upload
# 	requirementsFilename = ""
# 	requirements = request.files['requirementsurl']
# 	if requirements and allowed_file(requirements.filename):
# 		requirementsFilename = secure_filename(requirements.filename)
# 		requirements.save(os.path.join(app.config['UPLOAD_FOLDER'], requirementsFilename))

# 	documentationFilename = ""
# 	documentation = request.files['documentation']
# 	if documentation and allowed_file(documentation.filename):
# 		documentationFilename = secure_filename(documentation.filename)
# 		documentation.save(os.path.join(app.config['UPLOAD_FOLDER'], documentationFilename))

# 	newRequestDate = request.form['requestdate']
# 	if newRequestDate == "":
# 		newRequestDate = None

# 	newDeliveryDate = request.form['deliverydate']
# 	if newDeliveryDate == "":
# 		newDeliveryDate = None
# 	newProject = Projects.insert(
# 				accesstype = request.form['accesstype'],
# 				activity = request.form['activity'],
# 				buildingid_a = request.form['buildingid_A'],
# 				buildingid_b = request.form['buildingid_B'],
# 				businessimpact = request.form['businessimpact'],
# 				businessunit = request.form['businessunit'],
# 				cellnumber_a = request.form['cellnumber_A'],
# 				cellnumber_b = request.form['cellnumber_B'],
# 				circuitsize = request.form['circuitsize'],
# 				city_a = request.form['city_A'],
# 				city_b = request.form['city_B'],
# 				company_a = request.form['company_A'],
# 				company_b = request.form['company_B'],
# 				contacttitle_a = request.form['contacttitle_A'],
# 				contacttitle_b = request.form['contacttitle_B'],
# 				contactcompany_a = request.form['contactcompany_A'],
# 				contactcompany_b = request.form['contactcompany_B'],
# 				contactemail_a = request.form['contactemail_A'],
# 				contactemail_b = request.form['contactemail_B'],
# 				contactname_a = request.form['contactname_A'],
# 				contactname_b = request.form['contactname_B'],
# 				contactnumber_a = request.form['contactnumber_A'],
# 				contactnumber_b = request.form['contactnumber_B'],
# 				comments = request.form['comments'],
# 				deliverydate = newDeliveryDate,
# 				department = request.form['department'],
# 				dependencies = request.form['dependencies'],
# 				diversity = request.form['diversity'],
# 				documentation = documentationFilename,
# 				floor_a = request.form['floor_A'],
# 				floor_b = request.form['floor_B'],
# 				intercampus = request.form['intercampus'],
# 				latency = request.form['latency'],
# 				nickname = request.form['nickname'],
# 				othercontacts = request.form['othercontacts'],
# 				otherinfo = request.form['otherinfo'],
# 				projectname = request.form['projectname'],
# 				projectscope = request.form['projectscope'],
# 				protection = request.form['protection'],
# 				requestdate = newRequestDate,
# 				requestorname = request.form['requestorname'],
# 				requirementsurl = requirementsFilename,
# 				state_a = request.form['state_A'],
# 				state_b = request.form['state_B'],
# 				street_a = request.form['street_A'],
# 				street_b = request.form['street_B'],
# 				teammailer = request.form['teammailer'],
# 				tel_a = request.form['tel_A'],
# 				tel_b = request.form['tel_B'],
# 				tmsorder = request.form['tmsorder'],
# 				zipcode_a = request.form['zipcode_A'],
# 				zipcode_b = request.form['zipcode_B'],
# 				status = 2)
# 	newProject.execute()

# 	nextid = 0
# 	for result in itaacProjects.execute_sql('SELECT MAX(projectid) FROM Projects'):
# 		nextid = result[0]

# 	return redirect('/corporateNetwork/itaac/project?id=' + str(nextid))

# # Logic to add new ITaaC project
# @app.route('/corporateNetwork/itaac/editProject', methods=['POST'])
# def itaacEditProject():
# 	# File Upload
# 	requirementsFilename = ""
# 	requirements = request.files['requirementsurl']
# 	if requirements and allowed_file(requirements.filename):
# 		requirementsFilename = secure_filename(requirements.filename)
# 		requirements.save(os.path.join(app.config['UPLOAD_FOLDER'], requirementsFilename))

# 	documentationFilename = ""
# 	documentation = request.files['documentation']
# 	if documentation and allowed_file(documentation.filename):
# 		documentationFilename = secure_filename(documentation.filename)
# 		documentation.save(os.path.join(app.config['UPLOAD_FOLDER'], documentationFilename))

# 	newRequestDate = request.form['requestdate']
# 	if newRequestDate == "":
# 		newRequestDate = None

# 	newDeliveryDate = request.form['deliverydate']
# 	if newDeliveryDate == "":
# 		newDeliveryDate = None

# 	editProject = Projects.update(
# 				accesstype = request.form['accesstype'],
# 				activity = request.form['activity'],
# 				buildingid_a = request.form['buildingid_A'],
# 				buildingid_b = request.form['buildingid_B'],
# 				businessimpact = request.form['businessimpact'],
# 				businessunit = request.form['businessunit'],
# 				cellnumber_a = request.form['cellnumber_A'],
# 				cellnumber_b = request.form['cellnumber_B'],
# 				circuitsize = request.form['circuitsize'],
# 				city_a = request.form['city_A'],
# 				city_b = request.form['city_B'],
# 				company_a = request.form['company_A'],
# 				company_b = request.form['company_B'],
# 				contacttitle_a = request.form['contacttitle_A'],
# 				contacttitle_b = request.form['contacttitle_B'],
# 				contactcompany_a = request.form['contactcompany_A'],
# 				contactcompany_b = request.form['contactcompany_B'],
# 				contactemail_a = request.form['contactemail_A'],
# 				contactemail_b = request.form['contactemail_B'],
# 				contactname_a = request.form['contactname_A'],
# 				contactname_b = request.form['contactname_B'],
# 				contactnumber_a = request.form['contactnumber_A'],
# 				contactnumber_b = request.form['contactnumber_B'],
# 				comments = request.form['comments'],
# 				deliverydate = newDeliveryDate,
# 				department = request.form['department'],
# 				dependencies = request.form['dependencies'],
# 				diversity = request.form['diversity'],
# 				documentation = documentationFilename,
# 				floor_a = request.form['floor_A'],
# 				floor_b = request.form['floor_B'],
# 				intercampus = request.form['intercampus'],
# 				latency = request.form['latency'],
# 				nickname = request.form['nickname'],
# 				othercontacts = request.form['othercontacts'],
# 				otherinfo = request.form['otherinfo'],
# 				projectname = request.form['projectname'],
# 				projectscope = request.form['projectscope'],
# 				protection = request.form['protection'],
# 				requestdate = newRequestDate,
# 				requestorname = request.form['requestorname'],
# 				requirementsurl = requirementsFilename,
# 				state_a = request.form['state_A'],
# 				state_b = request.form['state_B'],
# 				street_a = request.form['street_A'],
# 				street_b = request.form['street_B'],
# 				teammailer = request.form['teammailer'],
# 				tel_a = request.form['tel_A'],
# 				tel_b = request.form['tel_B'],
# 				tmsorder = request.form['tmsorder'],
# 				zipcode_a = request.form['zipcode_A'],
# 				zipcode_b = request.form['zipcode_B'],
# 				status = 2).where(Projects.projectid == request.form['projectid'])
# 	editProject.execute()

# 	return redirect('/corporateNetwork/itaac/project?id=' + request.form['projectid'])
