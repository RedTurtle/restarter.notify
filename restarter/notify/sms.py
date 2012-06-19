import requests
from celery.task import task

TIMEOUT = 5
GATEWAY = 'http://gateway.airtelco.com/raven/sms'
FROM = 'facciamoadesso.it'
DEBUG = False

@task
def send_sms(login, password, message, phone):
    payload = {'login': login,
               'password': password,
               'phone': phone,
               'from' : FROM,
               'encoding' : 'utf8',
               'quality' : 'p', #standard not premium
               'body' : message }
    try:
        if DEBUG:
            print 'Going to send sms: %s' % payload
            return {'OK'}
        else:
            r = requests.get('%s/send' % GATEWAY, params=payload, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        return {'KO': 'Timeout'}
    except requests.exceptions.ConnectionError:
        return {'KO': 'No connection'}
    text = r.text
    if 'ERR' in text:
        return {'KO': text}
    else:
        return {'OK': text}
