import requests
import json 
from pysafebrowsing import SafeBrowsing

def virustotal(url):

	api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
	params = {
	'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c',
	'resource':'http://malware.wicar.org/data/eicar.com'
	}
	# params = {'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c', 'resource':'url'}
	response = requests.get(api_url, params=params)
	result = response.json()
	print(result['positives'])
	
	return (result['positives'] > 0)
	
# https://www.synology.com/en-global/knowledgebase/SRM/tutorial/Safe_Access/How_to_generate_Google_Safe_Browsing_API_keys		
def google_safe_browsing(url):
	s = SafeBrowsing("AIzaSyDfJHAoaO8Tktak09FxYWEGScCpyl0wZV8")
	# url can be an array
	# r = s.lookup_urls(['http://malware.testing.google.test/testing/malware/'])
	r = s.lookup_urls(url)
	# E.g {'http://malware.testing.google.test/testing/malware/': {'platforms': ['ANY_PLATFORM'], 'threats': ['MALWARE', 'SOCIAL_ENGINEERING'], 'malicious': True, 'cache': '300s'}}
	# Will be either True or False
	return list(r.values())[0]['malicious']
	
	
def check_urls(email):
	urls = email.urls
	malicious = false
	
	for url in urls:
		res = virustotal(url)
		