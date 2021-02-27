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
	def parse_eml(self, path_to_email):
		with open(path_to_email, 'rb') as fhdl:
			raw_email = fhdl.read()
		ep = eml_parser.EmlParser()
		parsed_eml = ep.decode_email_bytes(raw_email)
		print(json.dumps(parsed_eml, default=json_serial))
		
	# https://stackoverflow.com/questions/26322255/parsing-outlook-msg-files-with-python
	# https://github.com/TeamMsgExtractor/msg-extractor
	def parse_msg(self, path_to_email):
		# extracts urls
		extractor = URLExtract()
	
	
		msg = extract_msg.Message(path_to_email)
		msg_sender = msg.sender
		msg_date = msg.date
		msg_subj = msg.subject
		msg_message = msg.body
		msg_header = msg.header
		self.urls = extractor.find_urls(msg_message)
		
		print('Sender: {}'.format(msg_sender))
		print('Sent On: {}'.format(msg_date))
		print('Subject: {}'.format(msg_subj))
		print('Body: {}'.format(msg_message))
		print('Urls in body:')
		for url in self.urls:
			print(url)
			
		print('Header: {}'.format(msg_header))
		
		"""for att in dir(msg):
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
		
		
		
		
		

