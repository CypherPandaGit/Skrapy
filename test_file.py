import requests
import lxml.html
import json
from datetime import date
from datetime import timedelta



def log_writer(my_string):
    with open('date.txt','a') as log_file:
        log_file.write(my_string + '\n')


TUESDAY = 1  # it begins from ZERO

def get_closest_tuesday(for_date):
    tuesday = None
    weekday = for_date.weekday()

    if (weekday == TUESDAY):
        tuesday = for_date
    else:
        to_add = TUESDAY - for_date.weekday()
        tuesday = for_date + timedelta(days=to_add)

    return tuesday


s = requests.session()

login = s.get('https://nakup.itesco.cz/groceries/cs-CZ/'
              'login?from=https%3A%2F%2Fnakup.itesco.cz'
              '%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224'
              '.991395514.1584977092-2139990256.1584977092')
login_html = lxml.html.fromstring(login.text)

hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

print(form)

form['email'] = 'MAILHERE'
form['password'] = 'PASSHERE'
response = s.post('https://nakup.itesco.cz/groceries/cs-CZ/'
                  'login?from=https%3A%2F%2Fnakup.itesco.cz'
                  '%2Fgroceries%2Fcs-CZ%3F_ga%3D2.255516224'
                  '.991395514.1584977092-2139990256.1584977092',
                  data=form)


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


def data_mining(date_list, response=response):

    response = s.get('https://nakup.itesco.cz/groceries/cs-CZ/slots/'
                     'delivery/{0}?slotGroup=2'.format(date_list),
                     cookies=response.cookies.get_dict(),
                     headers={'accept': 'application/json'})

    if response.status_code == 200:
        print('Bruh, it looks good.\n')
        slots = json.loads(response.content)['slots']

        print('X' * 20)
        print(slots)
        print('X' * 20 + '\n')

        for x in slots:
            # print(x['status'])
            if x['status'] != 'UnAvailable':
                # If AVAILABLE send mail bruh. Presto!
                mined_date = x['start']
                formated_date = mined_date[0:10] + ', ' + mined_date[10:]

                for i in range(1):
                    new_string = 'Available: {0}'.format(str(formated_date))
                    log_writer(new_string)

    else:
        print('Sorry, you messed up again... Bruh...')
    return 'end'


print(data_mining(get_closest_tuesday(date.today())))
print(data_mining(get_closest_tuesday(date.today() + timedelta(days=7))))
print(data_mining(get_closest_tuesday(date.today() + timedelta(days=14))))
print(data_mining(get_closest_tuesday(date.today() + timedelta(days=21))))