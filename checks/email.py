import requests
import json
from pysafebrowsing import SafeBrowsing
from visual.prints import print_success, print_info, print_error, print_debug, print_section
import sys
import os
import os.path
from urllib.parse import urlparse
# https://domainaware.github.io/checkdmarc/checkdmarc.html
import checkdmarc
import re



def check_dmarc(email):

	results = checkdmarc.check_domains([email.sender_domain], skip_tls=True)
	json_report = json.dumps(results, ensure_ascii=False, indent=2)
	report = json.loads(json_report)
	if report['spf']['valid']:
		print_success("SPF record is present.")
	else:
		print_error("SPF RECORD DOES NOT EXIST. SENDER MIGHT BE SPOOFED.")

	if report['dmarc']['valid']:
		print_success("DMARC record is present.")
	else:
		print_error("DMARC RECORD DOES NOT EXIST. SENDER MIGHT BE SPOOFED.")



def check_reply_to_address(email):
	header = str(email.header)
	sender = str(email.sender)

	match = re.search(r'^Reply-To:.*', header, re.MULTILINE)
	try:
		results = str((match.group(0)))
	except:
		print_success("Reply-to header is not present.")
		return

	if not results == "":
		print_error("REPLY-TO HEADER IS SET WHICH MIGHT INDICATE THAT A SPOOFED EMAIL IS USED")
		print_error("SENDER: "+sender)
		print_error("REPLY-TO HEADER: "+results)
	# if return path is not equals to sender error out



def check_email_headers_and_dmarc(email):
	print_section("EMAIL HEADERS & DMARC")
	check_reply_to_address(email)
	check_dmarc(email)
