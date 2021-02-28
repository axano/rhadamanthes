import requests
import json 
from pysafebrowsing import SafeBrowsing
from visual.prints import print_success, print_info, print_error
import os.path


# TODO https://openphish.com/feed.txt

def virustotal(url):

	api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
	keys_file = open(os.path.dirname(__file__) + "/../keys/virus_total.txt")
	lines = keys_file.readlines()
	api_key = lines[0].rstrip() 
	params = {
	'apikey': api_key,
	'resource':url
	}
	# params = {'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c', 'resource':'url'}
	response = requests.get(api_url, params=params)
	result = response.json()
	print(result['positives'])
	
	return (result['positives'] > 0)
	
# https://www.synology.com/en-global/knowledgebase/SRM/tutorial/Safe_Access/How_to_generate_Google_Safe_Browsing_API_keys		
def google_safe_browsing(url):
	keys_file = open(os.path.dirname(__file__) + "/../keys/google_safe_browsing.txt")
	lines = keys_file.readlines()
	api_key = lines[0].rstrip()
	
	
	s = SafeBrowsing(api_key)
	# API expects array
	url_array = [url]
	
	# r = s.lookup_urls(['http://malware.testing.google.test/testing/malware/'])
	r = s.lookup_urls(url_array)
	
	# E.g {'http://malware.testing.google.test/testing/malware/': {'platforms': ['ANY_PLATFORM'], 'threats': ['MALWARE', 'SOCIAL_ENGINEERING'], 'malicious': True, 'cache': '300s'}}
	# Will be either True or False
	return (list(r.values())[0]['malicious'])
	
	
def check_urls(email):
	urls = email.urls
	malicious = False
	
	for url in urls:
		# VT has a very strict api limit for urls 4/min
		# print("VT: "+virustotal(url))
		print_success("Google Safe: is "+url+" malicious: "+str(google_safe_browsing(url)))