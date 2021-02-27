import sys
from model.Email import Email
from visual.banner import print_banner
def main(path_to_email):
	# create email object
	# parsed = Email(path_to_email)
	print_banner()
	Email(path_to_email)
		
main(sys.argv[1])