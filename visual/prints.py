from datetime import datetime

DEBUG = True
# Colors
# https://pypi.org/project/colorama/
from colorama import init
from colorama import Fore, Back, Style

init()



def get_time():
	now = datetime.now()
	return str(now.strftime("%H:%M:%S"))

def print_success(string):
	print(Fore.GREEN+"[+] "+get_time()+" "+string)
	print(Style.RESET_ALL, end = '')
	
def print_info(string):
	print(Fore.WHITE+"[*] "+get_time()+" "+string)
	print(Style.RESET_ALL, end = '')

def print_debug(string):
	global DEBUG
	if DEBUG:
		print(Fore.CYAN+"[!] "+get_time()+" "+string)
		print(Style.RESET_ALL, end = '')
	
	
def print_error(string):
	print(Fore.RED+"[-] "+get_time()+" "+string)
	print(Style.RESET_ALL, end = '')
	
def print_section(string):
	print_info("*************************************************************")
	print_info("\t\t\t\t"+string)
	print_info("*************************************************************")
	