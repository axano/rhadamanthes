import requests

def virustotal(url):

	api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
	params = {'apikey': 'f55c7aa43fe06eda741a7590069c5ae62a04f71d189115958840d813b6dd825c', 'resource':url}
	response = requests.get(api_url, params=params)
	print(response.json())



def check_urls(urls):
	for url in urls:
		