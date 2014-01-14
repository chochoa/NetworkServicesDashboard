from networkServicesDashboard import *
from flask import render_template, redirect
from databaseConnection import *
incidentList = []

#####################
#		Routing		#
#####################

@app.route('/perlTest')
def perl():
	pipe = subprocess.Popen(["perl", "/testScript.pl"], stdin=subprocess.PIPE)
	pipe.stdin.close()
	return render_template('/test.html',
							test = scriptResult)

@app.route('/buildList')
def build():
	siteSetup.generateCountryMappings()
	return redirect("/")

@app.route('/corporateNetwork/remoteOffice/sites/world')
def world():
	return render_template('/corporateNetwork/sites/world.html',
							printArea = siteSetup.printRegionList())

# AMER, AMER-LATAM, EMEA, APAC
@app.route('/corporateNetwork/remoteOffice/sites/region')
def region():
	region = request.args.get('r','')
	return render_template('/corporateNetwork/sites/region.html',
							printArea = siteSetup.printCountriesList(region),
							printRegion = region)

# Lowercase ISO code e.g (us,uk,za,cn)
@app.route('/corporateNetwork/remoteOffice/sites/country')
def country():
	country = request.args.get('c','')
	region = siteSetup.getParentRegion(country)
	return render_template('/corporateNetwork/sites/country.html',
							printArea = siteSetup.printSites(country),
							printRegion = region,
							printCountry = siteSetup.returnCountryName(country),
							printCountryCode = country)

# Lowercase site code
@app.route('/corporateNetwork/remoteOffice/sites/site')
def site():
	siteID = request.args.get('s','')
	country = siteSetup.getParentCountry(siteID)
	countryName = siteSetup.returnCountryName(country)
	region = siteSetup.getParentRegion(country)
	return render_template('/corporateNetwork/sites/site.html',
							printArea = siteSetup.printSiteInfo(siteID),
							printRegion = region,
							printCountry = country,
							printCountryName = countryName,
							printSite = siteID)

# Lowercase site code
@app.route('/corporateNetwork/remoteOffice/sites/router')
def link():
	router = request.args.get('r','')
	siteID = siteSetup.getParentSite(router)
	country = siteSetup.getParentCountry(siteID)
	countryName = siteSetup.returnCountryName(country)
	region = siteSetup.getParentRegion(country)
	return render_template('/corporateNetwork/sites/link.html',
							printArea = siteSetup.printRouterInfo(router),
							printRegion = region,
							printCountry = country,
							printCountryName = countryName,
							printSite = siteID,
							printRouter = router)


@app.route('/corporateNetwork/remoteOffice/sites/linkType')
def filterLink():
	filterValue = request.args.get('l','')
	return render_template('/corporateNetwork/sites/filter.html',
							printArea = siteSetup.printFilter('Link Type', filterValue),
							printType = 'Link Type',
							printValue = filterValue)


@app.route('/corporateNetwork/remoteOffice/sites/classification')
def filterClassification():
	filterValue = request.args.get('c','')
	return render_template('/corporateNetwork/sites/filter.html',
							printArea = siteSetup.printFilter('Site Classification', filterValue),
							printType = 'Site Classification',
							printValue = filterValue)

@app.route('/corporateNetwork/remoteOffice/sites/listing')
def fullListing():
	return render_template('/corporateNetwork/sites/fullListing.html',
							printArea = siteSetup.printSites('all'))

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
	#for rows html += rows
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
	for client in Clients.select():
		if client.status == 2:
			result = getProgress(client)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.engagementid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzInProgress.html', inProgressClients = html)

@app.route('/corporateNetwork/dmz/inService')
def dmzInService():
	html = ''
	for client in Clients.select():
		if client.status == 1:
			result = getProgress(client)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.engagementid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzInService.html', inServiceClients = html)

@app.route('/corporateNetwork/dmz/withdrawn')
def dmzWithdrawn():
	html = ''
	for client in Clients.select():
		if client.status == 3:
			result = getProgress(client)
			html += '''
						<tr class="clickable">
							<td><a href='/corporateNetwork/dmz/client?id=''' + str(client.engagementid) + ''''>''' + str(client.engagementid) + '''</a></td>
							<td>''' + str(client.subscriber) + '''</td>
							<td>''' + result['status'] + '''</td>
							<td>''' + str(client.updated) + '''</td>
						</tr>
					'''
	return render_template('corporateNetwork/dmzWithdrawn.html', withdrawnClients = html)

@app.route('/corporateNetwork/dmz/client')
def client():
	clientId = request.args.get('id', '')
	client = Clients.get(Clients.engagementid == clientId)

	result = getProgress(client)
	status = result['status']
	bar = result['bar']

	notesHtml = getNotes(client)
	lastNote = getLatestNote(client)

	if lastNote == None:
		lastNoteDate = ''
		lastNoteContent = "N/A"
	else:
		lastNoteDate = str(lastNote.posted)
		lastNoteContent = str(lastNote.content)

	return render_template('corporateNetwork/dmzClient.html', clientArray = client, progress = bar, currentStatus = status, printNotes = notesHtml, lastDate = lastNoteDate, lastContent = lastNoteContent)

@app.route('/corporateNetwork/dmz/addClient')
def dmzAddClient():
	for result in database.execute_sql("SELECT MAX(engagementid) FROM CLIENTS"):
		currentId = result[0] + 1
	return render_template('corporateNetwork/dmzAddClient.html', clientId = currentId)

@app.route('/corporateNetwork/dmz/addingClient', methods=['POST'])
def addingClient():
	for result in database.execute_sql("SELECT MAX(engagementid) FROM CLIENTS"):
		currentId = result[0] + 1

	isInService = request.form['inservice']
	if isInService == "Yes":
		isInService = 1
		newStatus = 1
	else:
		isInService = 0
		newStatus= 2

	newGoLiveDate = request.form['golivedate']
	if newGoLiveDate == None:
		newGoLiveDate == "0000-01-01"

	newTargetDate = request.form['targetdate']
	if newTargetDate == None:
		newTargetDate = "0000-01-01"

	newClient = Clients.insert(
						engagementid = int(currentId),
					    activityconducted = request.form['activity'],
    					billtoid = request.form['departmentid'],
    					billtoname = request.form['departmentname'],
    					case = request.form['case'],
    					comments = request.form['comments'],
    					connectionowner = request.form['connectionowner'],
    					crosscharge = request.form['crosscharge'],
    					estimatedmaximumbandwidth = request.form['maxbandwidth'],
    					golivedate = newGoLiveDate,
    					implementation = request.form['implementation'],
    					inservice = isInService,
    					labid = request.form['labid'],
    					labname = request.form['labname'],
    					labstatus = request.form['labstatus'],
    					location = request.form['location'],
    					othercontact = request.form['othercontact'],
    					otherservices = request.form['otherservices'],
    					plans = request.form['plans'],
    					primarycontact = request.form['primarycontact'],
    					securityinfo = request.form['securityinfo'],
    					securityreview = request.form['securityreview'],
    					servicegateway1 = request.form['servicegateway1'],
    					servicegateway2 = request.form['servicegateway2'],
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
    					vapapproval = request.form['vapapproval'])
	newClient.execute()

	return redirect('/corporateNetwork/dmz/client?id=' + (int(currentId) + 1))

@app.route('/corporateNetwork/dmz/withdrawClient', methods=['POST'])
def dmzWithdrawClient():
	withdrawnClient = Clients.update(status = 3).where(Clients.engagementid == request.form['clientId'])
	withdrawnClient.execute()
	return redirect('/corporateNetwork/dmz/client?id=' + request.form['clientId'])

@app.route('/corporateNetwork/dmz/deleteClient', methods=['POST'])
def dmzDeleteClient():
	deleteClient = Clients.delete().where(Clients.engagementid == request.form['clientId'])
	deleteClient.execute()
	return redirect('/corporateNetwork/dmz')

@app.route('/corporateNetwork/dmz/newNote', methods=['POST'])
def newNote():
	# engagementId, content is going to be posted across
	client = request.form['clientId']
	noteContent = request.form['noteContent']

	for result in database.execute_sql("SELECT MAX(noteid) FROM Notes"):
		currentId = result[0]

	newNote = Notes.insert(noteid = int(currentId) + 1, engagementid = client, content = noteContent)
	newNote.execute()

	return redirect('/corporateNetwork/dmz/client?id=' + client)

@app.route('/corporateNetwork/dmz/editClient', methods=['POST'])
def editClient():
	client = request.form['clientidhidden']

	isInService = request.form['inservice']
	newStatus = 0
	if isInService == "Yes":
		isInService = 1
		newStatus = 1
	else:
		isInService = 0
		newSatus = 2

	newGoLiveDate = request.form['golivedate']
	if newGoLiveDate == None or newGoLiveDate == 'None':
		newGoLiveDate = "0000-01-01"

	newTargetDate = request.form['targetdate']
	if newTargetDate == None or newTargetDate == 'None':
		newTargetDate = "0000-01-01"

	updatedClient = Clients.update(
					    activityconducted = request.form['activity'],
    					billtoid = request.form['departmentid'],
    					billtoname = request.form['departmentname'],
    					case = request.form['case'],
    					comments = request.form['comments'],
    					connectionowner = request.form['connectionowner'],
    					crosscharge = request.form['crosscharge'],
    					estimatedmaximumbandwidth = request.form['maxbandwidth'],
    					golivedate = newGoLiveDate,
    					implementation = request.form['implementation'],
    					inservice = isInService,
    					labid = request.form['labid'],
    					labname = request.form['labname'],
    					labstatus = request.form['labstatus'],
    					location = request.form['location'],
    					othercontact = request.form['othercontact'],
    					otherservices = request.form['otherservices'],
    					plans = request.form['plans'],
    					primarycontact = request.form['primarycontact'],
    					securityinfo = request.form['securityinfo'],
    					securityreview = request.form['securityreview'],
    					servicegateway1 = request.form['servicegateway1'],
    					servicegateway2 = request.form['servicegateway2'],
    					status = newStatus,
    					subscriber = request.form['subscriber'],
    					targetdate = newTargetDate,
    					teamname = request.form['teamname'],
    					vapapproval = request.form['vapapproval']).where(Clients.engagementid == client)
	updatedClient.execute()

	return redirect('/corporateNetwork/dmz/client?id=' + client)

@app.route('/corporateNetwork/itaac')
def itaac():
	html = ""
	return render_template('corporateNetwork/itaac.html',
							itaacIncidents = html)

@app.route('/testing')
def test():
	return '''<html>
				<body>
					<form name='caseQuery' action='/case' method='POST'>
						<input type='text' name='caseNo' />
						<input type='submit'>
					</form>
				</body>
			</html>'''

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

	if client.securityreview == 'Completed':
		result = {}
		result['status'] = 'Security Review completed'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (success)</span>
  				</div>
			</div>'''
		return result

	if client.securityreview == 'In Progress':
		result = {}
		result['status'] = 'Security Review in progress'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (warning)</span>
  				</div>
			</div>'''
		return result

	if client.securityinfo == 'No' or client.securityinfo == None:
		result = {}
		result['status'] = 'Initially engaged/collecting information'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100" style="width: 25%">
    				<span class="sr-only">25% Complete</span>
  				</div>
			</div>'''
		return result

	if client.securityinfo == 'Yes':
		result = {}
		result['status'] = 'Security Review not started'
		result['bar'] = '''
			<div class="progress progress-striped active">
  				<div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%">
    				<span class="sr-only">50% Complete (Danger)</span>
  				</div>
			</div>'''
		return result

def getNotes(client):
	html = ''
	for note in Notes.select().join(Clients).where(Clients.engagementid == client.engagementid).order_by(Notes.posted.desc()):
		html += '''
			<div class="well">
				<h4>''' + str(note.posted) + '''</h4>
				<p>''' + str(note.content) + '''</p>
			</div>'''
	return html

def getLatestNote(client):
	for note in Notes.select().join(Clients).where(Clients.engagementid == client.engagementid).order_by(Notes.posted.desc()):
		return note