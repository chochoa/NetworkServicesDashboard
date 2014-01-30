# from Site import Site
# from suds.client import Client
# import xml.etree.ElementTree as ET
# from collections import Counter
# import json
# import copy

# # Build country name list
# url = 'http://www.webservicex.net/country.asmx?WSDL'
# client = Client(url)

# # Initialises SiteList from sites.xml document
# tree = ET.parse('wanData.xml')
# root = tree.getroot()
# siteList = []
# countryCodes = []
# for childSite in root.findall('site'):
# 	theater = childSite.find('Theater').text
# 	siteCode = childSite.find('Site_Code').text
# 	siteName = childSite.find('Site_Name').text
# 	router = childSite.find('Router').text
# 	interface = childSite.find('Interface').text
# 	interfaceDescription = childSite.find('Interface_Description').text
# 	interfaceID = childSite.find('Unique_Interface_ID').text
# 	facility = childSite.find('Facility').text
# 	primaryBackupDual = childSite.find('PrimaryBackupDual').text
# 	HC = childSite.find('HC').text
# 	utilPeak = childSite.find('Util_Peak').text
# 	videoPeak = childSite.find('Video_Peak').text
# 	voicePeak = childSite.find('Voice_Peak').text
# 	defaultPeak = childSite.find('Default_Peak').text
# 	util95percentile = childSite.find('Util_95_Percentile').text
# 	video95percentile = childSite.find('Video_95_Percentile').text
# 	voice95percentile = childSite.find('Voice_95_Percentile').text
# 	default95percentile = childSite.find('Default_95_Percentile').text
# 	linkType = childSite.find('Link_Type').text
# 	siteClassification = childSite.find('Site_Classification').text
# 	isoCountryCode = childSite.find('isoCountryCode').text

# 	countryCodes.append(isoCountryCode)

# 	newSite = Site(theater,siteCode,siteName,router,interface,interfaceDescription,interfaceID,facility,primaryBackupDual,HC,utilPeak,videoPeak,voicePeak,defaultPeak,util95percentile,video95percentile,voice95percentile,default95percentile,linkType,siteClassification,isoCountryCode)
# 	siteList.append(newSite)

# countryCodes = set(countryCodes)

# # Load countrycodes mapping
# countryMappings = {}
# with open('countries.json') as data_file:
# 	countryMappings = json.load(data_file)

# def generateCountryMappings():
# 	for code in countryCodes:
# 		countryMappings[code] = (ET.fromstring(client.service.GetCountryByCountryCode(code)))[0][1].text
# 	with open ('../countries.json','w') as f:
# 		f.write(json.dumps(countryMappings))

# def returnCountryName(countryCode):
# 	return countryMappings[countryCode]

# # Returns a Counter dict of all Regions and their siteCount
# def getRegionalBreakdown():
# 	regionList = []
# 	for site in siteList:
# 		regionList.append(site.theater)
# 	return Counter(sorted(regionList))

# def getCountryBreakdown(region):
# 	countryList = []
# 	for site in siteList:
# 		if site.theater == region:
# 			countryList.append(site.isoCountryCode)	
# 	return Counter(sorted(countryList))

# def getSiteNameByID(siteID):
# 	for site in siteList:
# 		if site.siteCode == siteID:
# 			return site.siteName

# # Returns a list of sites in the specified Region
# # If getLength == True then this returns simply the number of sites in this region and no other details
# def getSitesByRegion(region, getLength):
# 	countryList = []
# 	for site in siteList:
# 		if site.theater == region:
# 			countryList.append(site)
# 	if (getLength == True):
# 		return len(countryList)
# 	return countryList

# def getParentRegion(country):
# 	for site in siteList:
# 		if site.isoCountryCode == country:
# 			return site.theater

# def getParentCountry(siteID):
# 	for site in siteList:
# 		if site.siteCode == siteID:
# 			return site.isoCountryCode

# def getParentSite(router):
# 	for site in siteList:
# 		if site.router == router:
# 			return site.siteCode

# def getRouter(router):
# 	for site in siteList:
# 		if site.router == router:
# 			return site

# # link or classification
# def filterBy(filterType, filterValue):
# 	results = []
# 	if (filterType == 'Link Type'):
# 		for site in siteList:
# 			if site.linkType == filterValue:
# 				results.append(site)
# 	elif (filterType == 'Site Classification'):
# 		for site in siteList:
# 			if site.siteClassification == filterValue:
# 				results.append(site)
# 	return results;

# # Returns a list of sites in the specified countries. 
# # If getLength == True then this returns simply the number of sites in this country and no other details
# def getSitesByCountry(country, getLength):
# 	countryList = []
# 	for site in siteList:
# 		if site.isoCountryCode == country:
# 			countryList.append(site)
# 	if (getLength == True):
# 		return len(countryList)
# 	return countryList

# # Returns a list of sites with the specified siteCode
# def getSitesBySiteCode(siteCode):
# 	returnList = []
# 	for site in siteList:
# 		if site.siteCode == siteCode:
# 			returnList.append(site)
# 	return returnList

# # Prints a list of the Regions
# def printRegionList():
# 	html = '''
# 			<table class='table table-condensed table-hover  ' id='dataTable'>
# 				<thead>
# 					<th>Region</th>
# 					<th>Site Count</th>
# 				</thead>
# 				<tbody>
# 			'''
# 	listOfSites = getRegionalBreakdown()

# 	for key,value in listOfSites.iteritems():
# 		html += '''
# 				<tr>
# 					<td>
# 						<a href='region?r=''' + key + ''''>''' + key + '''</a>
# 					</td>
# 					<td>
# 						''' + str(value) + '''
# 					</td>  
# 				</tr>
# 				'''
# 	html += '''
# 				</tbody>
# 			</table>
# 			'''
# 	return html

# # Prints out all countries with sites in specified region, with a site count breakdown.
# def printCountriesList(region):
# 	html = '''
# 			<table class='table table-condensed table-hover' id='dataTable'>
# 				<thead>
# 					<th>Country</th>
# 					<th>Site Count</th>
# 				</thead>
# 				<tbody>
# 			'''
# 	listOfSites = getCountryBreakdown(region)

# 	for key,value in listOfSites.iteritems():
# 		countryName = returnCountryName(key)

# 		html += '''
# 				<tr>
# 					<td>
# 						<a href='country?c=''' + key + ''''>''' + countryName + ''' (''' + key + ''')</a>
# 					</td>
# 					<td>
# 						''' + str(value) + '''
# 					</td>
# 				</tr>
# 				'''
# 	html += '''
# 				</tbody>
# 			</table>
# 			'''
# 	return html

# # Prints out a table of all sites and their details in the specified country. 
# def printSites(country):
# 	html = '''
# 			<table class='table table-condensed table-hover' id='dataTable'>
# 				<thead>
# 					<th>Site ID</th>
# 					<th>Site Location</th>
# 					<th>Country</th>
# 					<th>Site Classification</th>
# 					<th>Head Count</th>
# 				</thead>
# 				<tbody>
# 			'''

# 	if (country == 'all'):
# 		listOfSites = copy.deepcopy(siteList)
# 	else:
# 		listOfSites = getSitesByCountry(country, False)
# 		countryName = returnCountryName(country)

# 	for site in listOfSites:
# 		if (country == 'all'):
# 			countryName = returnCountryName(site.isoCountryCode)
# 		html += '''
# 				<tr>
# 					<td>	
# 						<a href='site?s=''' + site.siteCode + ''''>''' + site.siteCode + '''</a>
# 					</td>
# 					<td>
# 						''' + site.siteName + '''
# 					</td>
# 					<td>
# 						<a href='country?c=''' + site.isoCountryCode + ''''>''' + countryName + ''' (''' + site.isoCountryCode + ''')</a>
# 					</td>
# 					<td>
# 						<a href="classification?c=''' + site.siteClassification + '''">''' + site.siteClassification + '''</a>
# 					</td>
# 					<td>
# 						''' + site.HC + '''
# 					</td>
# 				</tr>
# 				'''
# 		listOfSites.remove(site)
# 		for currentSite in listOfSites:
# 			if currentSite.siteCode == site.siteCode:
# 				listOfSites.remove(currentSite)

# 	html += '''
# 				</tbody>
# 			</table>
# 			'''
# 	return html

# def printSiteInfo(siteID):
# 	sites = getSitesBySiteCode(siteID)
# 	html = ''
# 	if len(sites) > 1:
# 			html = '''
# 			<br />
# 			<div class="alert alert-info">
# 				<span><strong>Notice: </strong> There are multiple locations/links for this Site Code. All will be listed.</span>
# 			</div>
# 			'''
# 	html += '''
# 			<h3>Site Name: <small>''' + getSiteNameByID(siteID) + '''</small></h3>
# 			<h3>Site Code: <small>''' + siteID + '''</small></h3>

# 			<br />

# 			<table class='table table-hover'>
# 				<thead>
# 					<th>Router</th>
# 					<th>Link Type</th>
# 					<th>Classification</th>
# 				</thead>
# 				<tbody>'''
# 	for site in sites:
# 		html += '''
# 					<tr>
# 						<td><a href="router?r=''' + site.router + '''">''' +site.router + '''</a></td>
# 						<td><a href="linkType?l=''' + site.linkType + '''">''' + site.linkType + ''' (''' + site.primaryBackupDual + ''')</a></td>
# 						<td><a href="classification?c=''' + site.siteClassification + '''">''' + site.siteClassification + '''</a></td>
# 					</tr>
# 				'''
# 	html += '''
# 				</tbody>
# 			</table>'''
# 	return html

# def printRouterInfo(router):
# 	site = getRouter(router)
# 	html = '''
# 			<h3>Router: ''' + router + '''</h3>

# 			<hr />

# 			<h4>Parent Site: </h4>''' + site.siteCode + '''
# 			<br />
# 			<h4>Interface ID: </h4>''' + site.interfaceID + '''
# 			<h4>Interface: </h4>''' + site.interface + '''
# 			<h4>Interface Description: </h4>''' + site.interfaceDesc + '''
# 			<br />
# 			<h4>Facility: </h4>''' + site.facility + '''
			
# 			<hr />

# 			<h3>WAN Info</h3>

# 			<table class="table table-hover table-condensed">
# 				<thead>
# 					<th>Measure</th>
# 					<th>Peak</th>
# 					<th>95th Percentile</th>
# 				</thead>
# 				<tbody>
# 					<tr>
# 						<td>Util</td>
# 						<td>''' + site.utilPeak + '''</td>
# 						<td>''' + site.util95percentile + '''</td>
# 					</tr>
# 					<tr>
# 						<td>Video</td>
# 						<td>''' + site.videoPeak + '''</td>
# 						<td>''' + site.video95percentile + '''</td>
# 					</tr>
# 					<tr>
# 						<td>Voice</td>
# 						<td>''' + site.voicePeak + '''</td>
# 						<td>''' + site.voice95percentile + '''</td>
# 					</tr>
# 					<tr>
# 						<td>Default</td>
# 						<td>''' + site.defaultPeak + '''</td>
# 						<td>''' + site.default95percentile +'''</td>
# 					</tr>
# 				</tbody>
# 			</table>
# 		'''
# 	return html

# def printFilter(filterType, filterValue):
# 	sites = filterBy(filterType,filterValue)
# 	html = ''
# 	html += '''
# 			<table class='table table-hover' id='dataTable'>
# 				<thead>
# 					<th>Site ID</th>
# 					<th>Site Name</th>
# 					<th>Link Type</th>
# 					<th>Classification</th>
# 				</thead>
# 				<tbody>'''
# 	for site in sites:
# 		html += '''
# 					<tr>
# 						<td><a href="site?s=''' + site.siteCode + '''">''' + site.siteCode + '''</a></td>
# 						<td>''' + site.siteName + '''</td>
# 						<td><a href="linkType?l=''' + site.linkType + '''">''' + site.linkType + ''' (''' + site.primaryBackupDual + ''')</a></td>
# 						<td><a href="classification?c=''' + site.siteClassification + '''">''' + site.siteClassification + '''</a></td>
# 					</tr>
# 				'''
# 	html += '''
# 				</tbody>
# 			</table>'''
# 	return html