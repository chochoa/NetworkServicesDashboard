from networkServicesDashboard import *
from flask import render_template, redirect
from databaseConnection import *
import calendar
from datetime import datetime, timedelta
incidentList = []

def utcToLocal(time):
	timestamp = calendar.timegm(time.timetuple())
	local = datetime.fromtimestamp(timestamp)
	assert time.resolution >= timedelta(microseconds=1)
	return local.replace(microsecond=time.microsecond)

#####################
#		Routing		#
#####################

# @app.route('/perlTest')
# def perl():
# 	pipe = subprocess.Popen(["perl", "/testScript.pl"], stdin=subprocess.PIPE)
# 	pipe.stdin.close()
# 	return render_template('/test.html',
# 							test = scriptResult)

# @app.route('/buildList')
# def build():
# 	siteSetup.generateCountryMappings()
# 	return redirect("/")

# @app.route('/corporateNetwork/remoteOffice/sites/world')
# def world():
# 	return render_template('/corporateNetwork/sites/world.html',
# 							printArea = siteSetup.printRegionList())

# # AMER, AMER-LATAM, EMEA, APAC
# @app.route('/corporateNetwork/remoteOffice/sites/region')
# def region():
# 	region = request.args.get('r','')
# 	return render_template('/corporateNetwork/sites/region.html',
# 							printArea = siteSetup.printCountriesList(region),
# 							printRegion = region)

# # Lowercase ISO code e.g (us,uk,za,cn)
# @app.route('/corporateNetwork/remoteOffice/sites/country')
# def country():
# 	country = request.args.get('c','')
# 	region = siteSetup.getParentRegion(country)
# 	return render_template('/corporateNetwork/sites/country.html',
# 							printArea = siteSetup.printSites(country),
# 							printRegion = region,
# 							printCountry = siteSetup.returnCountryName(country),
# 							printCountryCode = country)

# # Lowercase site code
# @app.route('/corporateNetwork/remoteOffice/sites/site')
# def site():
# 	siteID = request.args.get('s','')
# 	country = siteSetup.getParentCountry(siteID)
# 	countryName = siteSetup.returnCountryName(country)
# 	region = siteSetup.getParentRegion(country)
# 	return render_template('/corporateNetwork/sites/site.html',
# 							printArea = siteSetup.printSiteInfo(siteID),
# 							printRegion = region,
# 							printCountry = country,
# 							printCountryName = countryName,
# 							printSite = siteID)

# # Lowercase site code
# @app.route('/corporateNetwork/remoteOffice/sites/router')
# def link():
# 	router = request.args.get('r','')
# 	siteID = siteSetup.getParentSite(router)
# 	country = siteSetup.getParentCountry(siteID)
# 	countryName = siteSetup.returnCountryName(country)
# 	region = siteSetup.getParentRegion(country)
# 	return render_template('/corporateNetwork/sites/link.html',
# 							printArea = siteSetup.printRouterInfo(router),
# 							printRegion = region,
# 							printCountry = country,
# 							printCountryName = countryName,
# 							printSite = siteID,
# 							printRouter = router)


# @app.route('/corporateNetwork/remoteOffice/sites/linkType')
# def filterLink():
# 	filterValue = request.args.get('l','')
# 	return render_template('/corporateNetwork/sites/filter.html',
# 							printArea = siteSetup.printFilter('Link Type', filterValue),
# 							printType = 'Link Type',
# 							printValue = filterValue)


# @app.route('/corporateNetwork/remoteOffice/sites/classification')
# def filterClassification():
# 	filterValue = request.args.get('c','')
# 	return render_template('/corporateNetwork/sites/filter.html',
# 							printArea = siteSetup.printFilter('Site Classification', filterValue),
# 							printType = 'Site Classification',
# 							printValue = filterValue)

# @app.route('/corporateNetwork/remoteOffice/sites/listing')
# def fullListing():
# 	return render_template('/corporateNetwork/sites/fullListing.html',
# 							printArea = siteSetup.printSites('all'))

# Root/Index Page
@app.route('/')
def index():
	return render_template('/index.html',
							homeAndRemoteIssues = 99,
							extranetIssues = 99,
							dcIssues = 99,
							corpNetworkIssues = len(incidentList))

# Home and Remote
@app.route('/homeAndRemote/homeOffice')
def homeAndRemote():
	return render_template('/homeAndRemote/homeOffice.html')

@app.route('/homeAndRemote/homeOffice/incidentClassification')
def homeAndRemoteIncidentClassification():
	return render_template('/homeAndRemote/homeOfficeIncidents.html')

@app.route('/homeAndRemote/vpn')
def vpn():
	return render_template('/homeAndRemote/vpn.html')

@app.route('/homeAndRemote/vpn/incidentClassification')
def vpnIncidentClassification():
	return render_template('/homeAndRemote/vpnIncidents.html')

# Extranet
@app.route('/extranet/siteConnection')
def extranet():
	return render_template('/extranet/siteConnection.html')

@app.route('/extranet/siteConnection/incidentClassification')
def incidentClassification():
	return render_template('/extranet/siteIncidents.html')

@app.route('/extranet/vpn')
def extranetVPN():
	return render_template('/extranet/vpn.html')

@app.route('/extranet/vpn/incidentClassification')
def extraincidentClassification():
	return render_template('/extranet/vpnIncidents.html')

# DC Networking
@app.route('/dcNetworking')
def dcNetworking():
	return render_template('/dcNetworking/dcNetworking.html')

# Corporate Network
@app.route('/corporateNetwork/')
@app.route('/corporateNetwork/core')
def core():
	return render_template('/corporateNetwork/core.html')

@app.route('/corporateNetwork/remoteOffice/')
def outages():
		critCount = 0
		highCount = 0
		medCount = 0
		html = ""

		if len(incidentList) > 0:
			for i in range(len(incidentList)):
				rowHTML = "<tr><td><a href='" + incidentList[i].link + "'>" + incidentList[i].title + "</a></td><td>" + incidentList[i].description + "</td></tr>"
				html += rowHTML
				incident = incidentList[i].title
				incident = incident.split("-", 1)
				incident = str(incident[0]).strip()
				if incident == "Critical Priority":
					critCount += 1
				elif incident == "High Priority":
					highCount += 1
				elif incident == "Medium Priority":
					medCount += 1

		return render_template('/corporateNetwork/remoteOffice.html',
								remoteOfficeOutages = html,
								outageNumber = 0,
								criticalNo = critCount,
								highNo = highCount,
								mediumNo = medCount)

#@app.route('/corporateNetwork/remoteOffice/sites')
#def siteInfo():
#	return render_template('/corporateNetwork/siteInfo.html', outageNumber = len(incidentList))

#@app.route('/corporateNetwork/remoteOffice/sites/region')
#def regions():
#	return render_template('/corporateNetwork/region.html')

@app.route('/corporateNetwork/remoteOffice/remoteIncidents')
def remoteIncidents():
	return render_template('/corporateNetwork/remoteIncidents.html')

@app.route('/corporateNetwork/wireless')
def wireless():
	html = ""
	#for rows html += row
	return render_template('/corporateNetwork/wireless.html',
							outageNumber = 0,
							wirelessIncidents = html,
							wirelessCriticalCount = 1,
							wirelessHighCount = 2,
							wirelessMediumCount = 4,
							wirelessLowCount = 10)

@app.route('/corporateNetwork/wireless/infra')
def wirelessInfra():
	return render_template('/corporateNetwork/wirelessInfra.html',
							apCount = 112546,
							controllerCount = 345)

@app.route('/corporateNetwork/wireless/status')
def wirelessStatus():
	return render_template('/corporateNetwork/wirelessStatus.html')

@app.route('/corporateNetwork/wireless/incidentClassification')
def wirelessIncidents():
	return render_template('/corporateNetwork/wirelessIncidents.html')

@app.route('/corporateNetwork/ion')
def ion():
	html = ""
	return render_template('corporateNetwork/ion.html',
							outageNumber = 0,
							ionIncidents = html,
							ionCriticalCount = 0,
							ionHighCount = 2,
							ionMediumCount = 5,
							ionLowCount = 0)

@app.route('/corporateNetwork/ion/stats')
def ionStats():
	return render_template('corporateNetwork/ionStats.html',
							outageNumber = 0,
							sponsorNo = 1601,
							guestNo = 5723,
							successNo = 4740,
							cecNo = 996)

@app.route('/corporateNetwork/cdn')
def cdn():
	html = ""
	return render_template('corporateNetwork/cdn.html',
							cdnIncidents = html,
							cdnCriticalCount = 0,
							cdnHighCount = 0,
							cdnMediumCount = 5,
							cdnLowCount = 10)

@app.route('/corporateNetwork/dmz')
def dmzInProgress():
	html = ''
	for client in clients.select():
		if client.status == 2:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M:%S")
			client.updated = utcToLocal(client.updated)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzInProgress.html', inProgressClients = html)

@app.route('/corporateNetwork/dmz/inService')
def dmzInService():
	html = ''
	for client in clients.select():
		if client.status == 1:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M:%S")
			client.updated = utcToLocal(client.updated)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.crosscharge) + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzInService.html', inServiceClients = html)

@app.route('/corporateNetwork/dmz/withdrawn')
def dmzWithdrawn():
	html = ''
	for client in clients.select():
		if client.status == 3:
			result = getProgress(client)
			client.updated = (client.updated).strftime("%Y-%m-%d %H:%M:%S")
			client.updated = utcToLocal(client.updated)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.labid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzWithdrawn.html', withdrawnClients = html)

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
		lastNote.posted = (lastNote.posted).strftime("%Y-%m-%d %H:%M:%S")
		lastNoteDate = str(lastNote.posted)
		lastNoteContent = str(lastNote.content)

	cases = client.remedycase.split(';')
	remedycases = ''
	for case in cases:
		if case[:3] == "INC":
			remedycases += "<a href='http://case/" + case + "' target='_blank'>" + case + "</a><br />"
		elif case[:3] == "CRQ" or case[0:2] == "RFC":
			remedycases += "<a href='http://rfc/" + case + "' target='_blank'>" + case + "</a><br />"
		else:
			remedycases += case + "<br />"

	return render_template('corporateNetwork/dmzClient.html', clientArray = client, progress = bar, currentStatus = status, printNotes = notesHtml, lastDate = lastNoteDate, lastContent = lastNoteContent, splitcases=remedycases)

# @app.route('/corporateNetwork/dmz/addClient')
# def dmzAddClient():
# 	nextid = 0
# 	for result in database.execute_sql('SELECT MAX(engagementid) FROM clients'):
# 		if result[0] == None:
# 			nextid = 1
# 		else:
# 			nextid = (result[0] + 1)
# 	return render_template('corporateNetwork/dmzAddClient.html', nextid = nextid)

@app.route('/corporateNetwork/dmz/addClient')
def dmzAddClient():
	return render_template('corporateNetwork/dmzAddClient.html')

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

	departmentid = request.form['billtoid']
	if departmentid == '':
		departmentid = None

	newClient = clients.insert(
					    activityconducted = request.form['activityconducted'],
    					billtoid = departmentid,
    					billtoname = request.form['billtoname'],
    					remedycase = request.form['remedycase'],
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
    					servicegateway1 = request.form['servicegateway1'],
    					servicegateway2 = request.form['servicegateway2'],
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
    					vapapproval = int(request.form['vapapproval']),
						addressspace = request.form['addressspace'])
	newClient.execute()

	nextid = 0
	for result in database.execute_sql('SELECT MAX(engagementid) FROM clients'):
		nextid = result[0]

	return redirect('/corporateNetwork/dmz/client?id=' + str(nextid))

@app.route('/corporateNetwork/dmz/withdrawClient', methods=['POST'])
def dmzWithdrawClient():
	withdrawnClient = clients.update(status = 3).where(clients.engagementid == request.form['clientId'])
	withdrawnClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientId'])

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

	newDepartmentId = request.form['departmentid']
	if newDepartmentId == '' or newDepartmentId == "None":
		newDepartmentId = None

	updatedClient = clients.update(
					    activityconducted = request.form['activityconducted'],
    					billtoid = newDepartmentId,
    					billtoname = request.form['departmentname'],
    					remedycase = request.form['remedycase'],
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
    					servicegateway1 = request.form['servicegateway1'],
    					servicegateway2 = request.form['servicegateway2'],
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
    					addressspace = request.form['addressspace'],
    					vapapproval = int(request.form['vapapproval'])).where(clients.engagementid == request.form['clientid'])
	updatedClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientid'])

@app.route('/corporateNetwork/dmz/newNote', methods=['POST'])
def newNote():
	client = request.form['clientId']
	noteContent = request.form['noteContent']
	newNote = notes.insert(engagementid = client, content = noteContent)
	newNote.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + client)

@app.route('/corporateNetwork/dmz/deleteNote', methods = ['POST'])
def deleteNote():
	noteid = request.form['noteid']
	delete = notes.delete().where(notes.noteid == int(request.form['noteid']))
	delete.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + str(request.form['engagementid']))

@app.route('/corporateNetwork/itaac')
def itaac():
	html = ""
	return render_template('corporateNetwork/itaac.html',
							itaacIncidents = html)

#########################
#		End Routing		#
#########################

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

def getNotesByClient(clientid):
	noteList = []
	for note in notes.select().join(clients).where(clients.engagementid == clientid).order_by(notes.posted.desc()):
		noteList.append(note)
	return noteList


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

def getLatestNote(client):
	for note in notes.select().join(clients).where(clients.engagementid == client.engagementid).order_by(notes.posted.desc()):
		return note