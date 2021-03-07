import requests
import json 
import hashlib
from os import walk



from visual.prints import print_success, print_info, print_error, print_debug, print_section
import os.path


MD5_HASHES = []
FILES = []

def get_files():
	global FILES
	
	print_debug("Getting attachments...")
	
	path = os.path.dirname(__file__) + "/../temp/"
	_, _, filenames = next(walk(path))
	
	if len(filenames) == 0:
		print_info("No attachments found.")
		return
	
	for file in filenames:
		FILES.append(path+file)

	

def get_md5_hashes():
	global FILES
	global MD5_HASHES
	
	print_debug("Calculating md5 hashes...")
	for f in FILES:
		MD5_HASHES.append(hashlib.md5(open(f,'rb').read()).hexdigest())

def check_hashes():
	global MD5_HASHES
	
	print_debug("Querying hashes on VT...")
	keys_file = open(os.path.dirname(__file__) + "/../keys/virus_total.txt")
	lines = keys_file.readlines()
	api_key = lines[0].rstrip() 
	
	headers = {'x-apikey' : api_key}
	
	for h in MD5_HASHES:
		counter = 0
		url = "https://www.virustotal.com/api/v3/files/"+h
		response = requests.get(url,headers=headers)
		result = response.json()
		# print_debug(str(result))
		if response.status_code == 404:
			print_success("Attachment was not found in VT database.")
		else:
			vendors_data = json.dumps(result['data']['attributes']['last_analysis_results'])
			vendors = json.loads(vendors_data)
			vendor_count = 0
			malicious = 0
			for vendor in vendors:
				vendors[vendor]['category']
				vendor_count = vendor_count + 1
				if vendors[vendor]['category'] == "malicious":
					malicious = malicious + 1
			print_error("ATTACHMENT "+FILES[counter]+" WITH MD5 HASH "+h+" IS FLAGGED BY "+str(malicious)+" OUT OF THE "+str(vendor_count)+" VENDORS.")
		counter = counter + 1

	
def check_attachments():
	print_section("ATTACHMENTS")
	get_files()
	get_md5_hashes()
	check_hashes()