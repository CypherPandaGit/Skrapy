import requests
import lxml.html
from bs4 import BeautifulSoup

s = requests.session()

login = s.get('https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092')
login_html = lxml.html.fromstring(login.text)

hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

print(form)

form['email'] = 'mail'
form['password'] = 'heslo'
response = s.post('https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092', data=form)

print(response.url)

if 'Dobrý den pane Měšťan' in response.text:
    print('Oh boy, you are in!')
else:
    print('Sorry, you messed up again... Bruh...')

