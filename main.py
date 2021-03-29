import sys
import os
import glob


DEBUG = False


import visual
from visual.prints import print_success, print_info, print_error, print_debug, print_section
from visual.banner import print_banner
visual.prints.DEBUG = DEBUG

from model.Email import Email

from checks.url import check_urls
from checks.certificate import check_certificates
from checks.attachment import check_attachments
from checks.email import check_email_headers_and_dmarc



def initialize():

	print_banner()
	if len(sys.argv) < 2:
		print_error("Usage: python main.py \"Path to msg or eml\"")
		exit(1)
	print_section("START")
	print_success("Script started.")


	files = glob.glob(os.path.dirname(__file__)+"/temp/*" )
	for f in files:
		os.remove(f)
	print_debug("Deleted contents of temp folder.")

def end():
	print_section("END")
	print_success("Script ended succesfully.")


def main():

	initialize()
	# create email object
	path_to_email = sys.argv[1]
	email = Email(path_to_email)
	check_urls(email)
	check_certificates(email)
	check_attachments()
	check_email_headers_and_dmarc(email)

	# AI starts here
	# os.system()
	end()





def debug():
	global DEBUG
	DEBUG = True
	visual.prints.DEBUG = DEBUG

	initialize()
	# create email object
	path_to_email = sys.argv[1]
	email = Email(path_to_email)

	check_urls(email)
	check_certificates(email)
	check_attachments()
	check_email_headers_and_dmarc(email)

	# AI starts here

	end()


#main()
debug()
