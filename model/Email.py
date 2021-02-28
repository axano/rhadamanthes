import datetime
import json
from urlextract import URLExtract


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
		# extracts urls
		extractor = URLExtract()
	
	
		msg = extract_msg.Message(path_to_email)
		self.sender = msg.sender
		self.date = msg.date
		self.subject = msg.subject
		self.body = msg.body
		self.header = msg.header
		self.urls = extractor.find_urls(self.body)

		
		"""
		for att in dir(msg):
			print (att, getattr(msg,att))
		"""
	# Path can point to either eml or msg
	def __init__(self, path_to_email):
		if path_to_email.endswith(".eml"):
			self.parse_eml(path_to_email)
		elif path_to_email.endswith(".msg"):
			self.parse_msg(path_to_email)
		else:
			assert "Mail cannot be parsed"
		
		
		
		
		

