import requests
from celery.task import task

TIMEOUT = 5
#GATEWAY = 'http://gateway.airtelco.com/raven/sms'
GATEWAY = 'http://localhost'
FROM = 'restartER Team'

@task
def send_sms(login, password, message, phone):
    payload = {'login': login,
               'password': password,
               'phone': phone,
               'from' : FROM,
               'encoding' : 'utf8',
               'quality' : 's', #standard not premium
               'body' : message }
    try:
        r = requests.get('%s/send' % GATEWAY, params=payload, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        return {'NOK': 'Timeout'}
    except requests.exceptions.ConnectionError:
        return {'NOK': 'No connection'}
    text = r.text
    if 'ERR' in text:
        return {'NOK': text}
    else:
        return {'OK': text}
