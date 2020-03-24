import requests
import lxml.html
import json
import http.cookiejar as cookie
from bs4 import BeautifulSoup

s = requests.session()

login = s.get('https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092')
login_html = lxml.html.fromstring(login.text)

hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

print(form)

form['email'] = 'PUTYOUREMAILHERE'
form['password'] = 'PUTYOURPASSHERE'
response = s.post('https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092', data=form)


print('-' * 20)
print('RESPONSE URL: ')
print(response.url)
print('STATUS CODE: ')
print(response.status_code)
print('-' * 20 + '\n')
print('RESPONSE COOKIES: ')
print(response.cookies.get_dict())
print('-' * 20 + '\n')


if response.status_code == 200:
    print('Oh boy, you are in!')

    response = s.get('https://nakup.itesco.cz/groceries/cs-CZ/slots/delivery/2020-03-31?slotGroup=2', cookies=response.cookies.get_dict(), headers={'accept': 'application/json'})

    if response.status_code == 200:
        print('Bruv')
        slots = json.loads(response.content)['slots']

        for x in slots:
            print(x['status'])
            if x['status'] != 'UnAvailable':
                print('Send mail bruv')
else:
    print('Sorry, you messed up again... Bruh...')

print(response.status_code)




# -----------------------------------------
# OLD TESTING CODE
# -----------------------------------------
# import requests
# from requests import get
# from bs4 import BeautifulSoup
#
#
# URL = 'https://nakup.itesco.cz'
# LOGIN_URL = 'https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092'
# HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
#
#
# s = requests.session()
# # csrf_token = s.get(LOGIN_URL).cookies['_csrf']
# csrf_token = s.get(LOGIN_URL)
#
# LOGIN_DATA = {
#     'email': 'diviline@gmail.com',
#     'password': 'FVxvaVgirN%!77y',
#     '_csrf': csrf_token
# }
#
# login_req = s.post(LOGIN_URL, headers=HEADERS, data=LOGIN_DATA)
# print(login_req.status_code)
#
# cookies = login_req.cookies
#
# response = get(LOGIN_URL)
# print(response.text[:5000])
#
# # soup = BeautifulSoup(response.text, 'html.parser')
# # text = soup.findAll(text=True)
# #
# #
# # output = ''
# # blacklist = [
# # 	'[document]',
# # 	'noscript',
# # 	'header',
# # 	'meta',
# # 	'head',
# # 	'input',
# # 	'script',
# # ]
# #
# # for t in text:
# # 	if t.parent.name not in blacklist:
# # 		output += '{} '.format(t)
# #
# # print(output)