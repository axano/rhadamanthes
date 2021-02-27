import requests
import json 

def virustotal(url):

	api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
	params = {'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c', 'resource':'http://malware.wicar.org/data/eicar.com'}
	# params = {'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c', 'resource':'url'}
	response = requests.get(api_url, params=params)
	result = response.json()
	print(result['positives'])
	return (result['positives'] > 0)
		


def check_urls(email):
	urls = email.urls
	malicious = false
	
	for url in urls:
		res = virustotal(url)
		