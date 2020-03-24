import requests
from requests import get
from bs4 import BeautifulSoup


URL = 'https://nakup.itesco.cz'
LOGIN_URL = 'https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


s = requests.session()
# csrf_token = s.get(LOGIN_URL).cookies['_csrf']
csrf_token = s.get(LOGIN_URL)

LOGIN_DATA = {
    'email': 'mail',
    'password': 'pass',
    '_csrf': csrf_token
}

login_req = s.post(LOGIN_URL, headers=HEADERS, data=LOGIN_DATA)
print(login_req.status_code)

cookies = login_req.cookies

response = get(LOGIN_URL)
print(response.text[:5000])

# soup = BeautifulSoup(response.text, 'html.parser')
# text = soup.findAll(text=True)
#
#
# output = ''
# blacklist = [
# 	'[document]',
# 	'noscript',
# 	'header',
# 	'meta',
# 	'head',
# 	'input',
# 	'script',
# ]
#
# for t in text:
# 	if t.parent.name not in blacklist:
# 		output += '{} '.format(t)
#
# print(output)