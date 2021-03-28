import ssl, socket
import requests
from urllib.parse import urlparse

from visual.prints import print_success, print_info, print_error, print_debug, print_section

def check_certificates(email):

	print_section("CERTIFICATES")
	urls = email.urls

	if len(urls) == 0:
		print_info("No URLS found.")
		return

	for url in urls:
		print_debug("Checking certificate for url: "+url)
		if url.startswith("https"):
			hostname = urlparse(url).netloc
			ctx = ssl.create_default_context()
			with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
				try:
					s.connect((hostname, 443))
					cert = s.getpeercert()
					subject = dict(x[0] for x in cert['subject'])
					#issued_to = subject['commonName']
					issuer = dict(x[0] for x in cert['issuer'])
					issued_by = issuer['organizationName']
					if issued_by == "Let's Encrypt":
						print_error("CERTIFICATE FOR URL "+url+" IS ISSUED BY LETS ENCRYPT.")
					else:
						print_success("CERTIFICATE FOR URL "+url+" IS OK.")
				except:
					print_error("URL "+url+" IS UNREACHABLE")

		else:
			print_error("URL "+url+" DOES NOT USE HTTPS.")
