import sys
import os
import glob


DEBUG = False


import visual
from visual.prints import print_success, print_info, print_error, print_debug
from visual.banner import print_banner
visual.prints.DEBUG = DEBUG

from model.Email import Email

from checks.url import check_urls
from checks.certificate import check_certificates
from checks.attachment import analyze_attachments



def initialize():
	
	files = glob.glob(os.path.dirname(__file__)+"/temp/*" )
	for f in files:
		os.remove(f)
	print_debug("Deleted contents of temp folder.")
	
	
def main(path_to_email):
	
	print_banner()
	print_success("Script started.")
	initialize()
	# create email object
	email = Email(path_to_email)
	check_urls(email)
	check_certificates(email)
	analyze_attachments()
	
	# AI starts here

	
	print_success("Script ended succesfully.")
	
	
	
def debug(path_to_email):
	global DEBUG
	DEBUG = True
	visual.prints.DEBUG = DEBUG
	
	print_banner()
	print_success("Script started.")
	initialize()
	# create email object
	email = Email(path_to_email)
	check_urls(email)
	check_certificates(email)
	analyze_attachments()
	
	# AI starts here

	
	print_success("Script ended succesfully.")
	

main(sys.argv[1])
#debug(sys.argv[1])