import sys
import os
import glob


from visual.prints import print_success, print_info, print_error, print_debug
from visual.banner import print_banner

from model.Email import Email

from checks.url import check_urls
from checks.attachment import analyze_attachments

DEBUG = True

def initialize():
	
	files = glob.glob(os.path.dirname(__file__)+"/temp/*" )
	for f in files:
		os.remove(f)
	print_debug("Deleted contents of temp folder")
	
def main(path_to_email):
	
	print_banner()
	# initialize()
	# create email object
	email = Email(path_to_email)
	check_urls(email)
	analyze_attachments()
	
main(sys.argv[1])