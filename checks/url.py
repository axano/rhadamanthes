import requests
import json 
from pysafebrowsing import SafeBrowsing
from visual.prints import print_success, print_info, print_error, print_debug, print_section
import os.path
from urllib.parse import urlparse

# TODO 

CACHE = ""

# This list is updated every day so it checks only
# against recent threats
def openphish(url):
	global CACHE
	
	feed = "https://openphish.com/feed.txt"
	
	if CACHE == "":
		print_debug("Cache is empty. Building cache...")
		CACHE = []
		response = requests.get(feed)
		temp = response.text
		for line in temp.splitlines():	
			subdomain = urlparse(line).netloc
			CACHE.append(subdomain)
	
	if urlparse(url).netloc in CACHE:
		print_error("[OPENFISH] MALICIOUS URL FOUND: "+url)
	else:
		print_success("[OPENFISH] url is clean: "+url)

def virustotal(url):

	api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
	keys_file = open(os.path.dirname(__file__) + "/../keys/virus_total.txt")
	lines = keys_file.readlines()
	api_key = lines[0].rstrip() 
	params = {
	'apikey': api_key,
	'resource':url
	}
	response = requests.get(api_url, params=params)
	result = response.json()
	
	if result['positives'] > 0:
		print_error("[VIRUS TOTAL] MALICIOUS URL FOUND: "+url)
	else:
		print_success("[VIRUS TOTAL] url is clean: "+url)
	
	
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
	if (list(r.values())[0]['malicious']):
		print_error("[GOOGLE SAFE BROWSING] MALICIOUS URL FOUND: "+url)
	else:
		print_success("[GOOGLE SAFE BROWSING] url is clean: "+url)

def custom_checks(url):
	suspicious_domains = [
						'forms.office.com'
						]
						
						
	if urlparse(url).netloc in suspicious_domains:
		print_error("[CUSTOM CHECKS] SUSPICIOUS URL FOUND: "+url)
	else:
		print_success("[CUSTOM CHECKS] url is clean: "+url)
		
def check_urls(email):
	
	print_section("URLS")
	urls = email.urls
	if len(urls) == 0:
		print_info("No URLS found.")
		return
		
	for url in urls:
		print_debug("Checking url: "+url)
		# VT has a very strict api limit for urls 4/min
		# print("VT: "+virustotal(url))
		google_safe_browsing(url)
		openphish(url)
		custom_checks(url)