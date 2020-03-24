import requests
import lxml.html
import json
import http.cookiejar as cookie
from bs4 import BeautifulSoup

def log_writer(my_string):
    with open('date.txt','a') as log_file:
        log_file.write(my_string + '\n')

s = requests.session()

login = s.get('https://nakup.itesco.cz/groceries/cs-CZ/login?from=https%3A%2F%2Fnakup.itesco.cz%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224.991395514.1584977092-2139990256.1584977092')
login_html = lxml.html.fromstring(login.text)

hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

print(form)

form['email'] = 'EMAIL'
form['password'] = 'PASS'
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
    print('Oh boy, you are in!\n')

    response = s.get('https://nakup.itesco.cz/groceries/cs-CZ/slots/delivery',
                     cookies=response.cookies.get_dict(), headers={'accept': 'application/json'})
    # response = s.get('https://nakup.itesco.cz/groceries/cs-CZ/slots/delivery/2020-03-31?slotGroup=2', cookies=response.cookies.get_dict(), headers={'accept': 'application/json'})

    if response.status_code == 200:
        print('Bruh, it looks good.\n')
        slots = json.loads(response.content)['slots']

        print('X' * 20)
        print(slots)
        print('X' * 20 + '\n')

        for x in slots:
            # print(x['status'])
            if x['status'] != 'UnAvailable':
                # print('Send mail bruh. Presto.')
                date = x['start']
                formated_date = date[0:10] + ', ' + date[10:]

                for i in range(1):
                    new_string = 'Available: {0}'.format(str(formated_date))
                    log_writer(new_string)


else:
    print('Sorry, you messed up again... Bruh...')

print(response.status_code)
