import sys

from visual.banner import print_banner

from model.Email import Email

from checks.url import check_urls

def main(path_to_email):
	
	print_banner()
	
	# create email object
	email = Email(path_to_email)
	check_urls(email)

	
main(sys.argv[1])