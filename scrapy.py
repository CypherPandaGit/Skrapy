import requests
from bs4 import BeautifulSoup


URL = 'https://nakup.itesco.cz/groceries/'
LOGIN_URL = 'https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%2F'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


s = requests.session()
csrf_token = s.get(URL).cookies['_csrf']

LOGIN_DATA = {
    'email': 'mail',
    'password': 'heslo',
    '_csrf': csrf_token
}

login_req = s.post(URL + LOGIN_URL, headers = HEADERS, data = LOGIN_DATA)
print(login_req.status_code)
print(login_req.text[:500])

cookies = login_req.cookies
