from networkServicesDashboard import *
from flask import render_template, redirect
import calendar
from datetime import datetime, timedelta
import time

#Databases
from dmzaasClients import *
from itaacProjects import *

#############################
# General Application Views #
#############################

#Index Page
@app.route('/')
def index():
	return render_template('/tutorial.html')

#Admin Interface
@app.route('/admin')
def adminInterface():
	locations = []
	for gateway in gateways.select():
		locations.append(gateway.location)
	locations = list(set(locations))
	return render_template('/admin.html', assignees = assignees.select(), gateways = gateways.select(), locations = locations)

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

@app.route('/tutorial')
def tutorial():
	return render_template('/tutorial.html')

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
							<td>''' + str(client.updated) + '''</td>
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
	for result in database.execute_sql('SELECT MAX(engagementid) FROM clients'):
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

# Logic to withdrawn a client
@app.route('/corporateNetwork/dmz/withdrawClient', methods=['POST'])
def dmzWithdrawClient():
	withdrawnClient = clients.update(status = 3).where(clients.engagementid == request.form['clientId'])
	withdrawnClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientId'])

# Logic to delete a client
@app.route('/corporateNetwork/dmz/deleteClient', methods=['POST'])
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

###############
# ITaaC Views #
###############

@app.route('/corporateNetwork/itaac')
def itaac():
	inServiceProjects = Projects.select().where(Projects.status == 2)
	return render_template('corporateNetwork/itaac/inProgress.html', projects = inServiceProjects)

@app.route('/corporateNetwork/itaac/addProject')
def itaacAddProject():
	return render_template('corporateNetwork/itaac/addProject.html')

@app.route('/corporateNetwork/itaac/project')
def itaacViewProject():
	project = Projects.get(Projects.projectid == request.args.get('id', ''))
	return render_template('corporateNetwork/itaac/project.html', project = project)

@app.route('/corporateNetwork/itaac/addingProject', methods=['POST'])
def itaacAddingProject():
	newRequestDate = request.form['requestdate']
	if newRequestDate == "":
		newRequestDate = None

	newDeliveryDate = request.form['deliverydate']
	if newDeliveryDate == "":
		newDeliveryDate = None
	newProject = Projects.insert(
				accesstype = request.form['accesstype'],
				activity = request.form['activity'],
				buildingid_a = request.form['buildingid_A'],
				buildingid_b = request.form['buildingid_B'],
				businessimpact = request.form['businessimpact'],
				businessunit = request.form['businessunit'],
				cellnumber_a = request.form['cellnumber_A'],
				cellnumber_b = request.form['cellnumber_B'],
				circuitsize = request.form['circuitsize'],
				city_a = request.form['city_A'],
				city_b = request.form['city_B'],
				company_a = request.form['company_A'],
				company_b = request.form['company_B'],
				contacttitle_a = request.form['contacttitle_A'],
				contacttitle_b = request.form['contacttitle_B'],
				contactcompany_a = request.form['contactcompany_A'],
				contactcompany_b = request.form['contactcompany_B'],
				contactemail_a = request.form['contactemail_A'],
				contactemail_b = request.form['contactemail_B'],
				contactname_a = request.form['contactname_A'],
				contactname_b = request.form['contactname_B'],
				contactnumber_a = request.form['contactnumber_A'],
				contactnumber_b = request.form['contactnumber_B'],
				deliverydate = newDeliveryDate,
				department = request.form['department'],
				dependencies = request.form['dependencies'],
				diversity = request.form['diversity'],
				documentation = request.form['documentation'],
				floor_a = request.form['floor_A'],
				floor_b = request.form['floor_B'],
				intercampus = request.form['intercampus'],
				latency = request.form['latency'],
				nickname = request.form['nickname'],
				othercontacts = request.form['othercontacts'],
				otherinfo = request.form['otherinfo'],
				projectname = request.form['projectname'],
				projectscope = request.form['projectscope'],
				protection = request.form['protection'],
				requestdate = newRequestDate,
				requestorname = request.form['requestorname'],
				requirementsurl = request.form['requirementsurl'],
				state_a = request.form['state_A'],
				state_b = request.form['state_B'],
				street_a = request.form['street_A'],
				street_b = request.form['street_B'],
				teammailer = request.form['teammailer'],
				tel_a = request.form['tel_A'],
				tel_b = request.form['tel_B'],
				zipcode_a = request.form['zipcode_A'],
				zipcode_b = request.form['zipcode_B'],
				status = 2)
	newProject.execute()

	nextid = 0
	for result in itaacProjects.execute_sql('SELECT MAX(projectid) FROM Projects'):
		nextid = result[0]

	return redirect('/corporateNetwork/itaac/project?id=' + str(nextid))
