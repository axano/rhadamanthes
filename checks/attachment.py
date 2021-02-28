import requests
import json 
import hashlib
from os import walk



from visual.prints import print_success, print_info, print_error, print_debug
import os.path


MD5_HASHES = []
FILES = []

def get_files():
	global FILES
	
	path = os.path.dirname(__file__) + "/../temp/"
	_, _, filenames = next(walk(path))
	for file in filenames:
		FILES.append(path+file)

	

def get_md5_hashes():
	global FILES
	global MD5_HASHES
	
	for f in FILES:
		MD5_HASHES.append(hashlib.md5(open(f,'rb').read()).hexdigest())

def analyze_hashes():
	global MD5_HASHES
	
	keys_file = open(os.path.dirname(__file__) + "/../keys/virus_total.txt")
	lines = keys_file.readlines()
	api_key = lines[0].rstrip() 
	
	headers = {'x-apikey' : api_key}
	
	for h in MD5_HASHES:
		url = "https://www.virustotal.com/api/v3/files/"+h
		response = requests.get(url,headers=headers)
		result = response.json()
		print_success(str(result))

	
def analyze_attachments():
	get_files()
	get_md5_hashes()
	analyze_hashes()