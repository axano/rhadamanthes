import datetime
import json
from urlextract import URLExtract
import os
import os.path
import csv
import glob

from visual.prints import print_success, print_info, print_error, print_debug

# msg
import extract_msg


# eml
import eml_parser


def json_serial(obj):
	serial = ""
	if isinstance(obj, datetime.datetime):
		serial = obj.isoformat()
	return serial
		
class Email:
	sender = ""
	urls = []
	sender_domain = ""
	email_headers = ""
	date = ""
	body = ""
	header = ""
	attachments = []
	
	# https://pypi.org/project/eml-parser/
	# Needs testing
	def parse_eml(self, path_to_email):
		with open(path_to_email, 'rb') as fhdl:
			raw_email = fhdl.read()
		ep = eml_parser.EmlParser()
		parsed_eml = ep.decode_email_bytes(raw_email)
		print(json.dumps(parsed_eml, default=json_serial))
	
	# Works
	# https://stackoverflow.com/questions/26322255/parsing-outlook-msg-files-with-python
	# https://github.com/TeamMsgExtractor/msg-extractor
	def parse_msg(self, path_to_email):
		print_debug("Parsing msg...")
		# extracts urls
		extractor = URLExtract()
	
	
		msg = extract_msg.Message(path_to_email)
		self.sender = msg.sender
		self.date = msg.date
		self.subject = msg.subject
		self.body = msg.body
		self.header = msg.header
		self.urls = extractor.find_urls(self.body)
		# Useless data
		# self.main_properties = msg.mainProperties
		
		# https://github.com/TeamMsgExtractor/msg-extractor/issues/88
		self.attachments = msg.attachments

		
		# Library parsing msg file does not support custom saving paths for attachments so
		# directory is changed manualy
		os.chdir(os.path.dirname(__file__) + "/../temp")
		
		for a in self.attachments:
			a.save()
			
		os.chdir(os.path.dirname(__file__) + "/../")
		"""
		for att in dir(msg):
			print (att, getattr(msg,att))
		"""
		
	
	def dump_to_csv(self):
		with open(os.path.dirname(__file__) + "/../ai/dump.csv", 'w', encoding="utf-8") as csv_file:
			wr = csv.writer(csv_file, delimiter=';')
			header = ['sender','date','subject','body','email_header (multiline)','URLS']
			row = [str(self.sender), str(self.date), str(self.subject), str(self.body), str(self.header), str(self.urls)]
			
			wr.writerow(header)
			wr.writerow(row)
				
	# Path can point to either eml or msg
	def __init__(self, path_to_email):
		if path_to_email.endswith(".eml"):
			self.parse_eml(path_to_email)
		elif path_to_email.endswith(".msg"):
			self.parse_msg(path_to_email)
		else:
			assert print_error("Mail cannot be parsed")
		self.dump_to_csv()