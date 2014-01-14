from Site import Site
from suds.client import Client
import xml.etree.ElementTree as ET
import json

# Build country name list
url = 'http://www.webservicex.net/country.asmx?WSDL'
client = Client(url)

# Initialises SiteList from sites.xml document
tree = ET.parse('networkServicesDashboard/sites.xml')
root = tree.getroot()
countryCodes = []

for childSite in root.findall('site'):
	theater = childSite.find('theater').text
	isoCountryCode = childSite.find('isoCountryCode').text
	countryCodes.append(isoCountryCode)

for code in countryCodes:
	countryMappings[code] = (ET.fromstring(client.service.GetCountryByCountryCode(code)))[0][1].text
with open ('countries.json','w') as f:
	f.write(json.dumps(countryMappings))