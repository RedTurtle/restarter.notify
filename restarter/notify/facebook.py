from urlparse import parse_qsl
import requests
from celery.task import task
import json


def get_fb_token(client_id, client_secret):
    params = {'grant_type': 'client_credentials',
              'client_id': client_id,
              'client_secret': client_secret}
    response = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
    if response.status_code == 200:
        return dict(parse_qsl(response.content))


def get_page_token(page_secret):
    response = requests.get('https://graph.facebook.com/me/accounts?access_token=%s' % page_secret)
    if response.status_code == 200:
        data = json.loads(response.text)
        for page in data['data']:
            if page['name'] == u'FacciamoAdesso':
                return {'access_token': page['access_token']}


@task
def post_an_action(client_id, client_secret, facebook_id, action, **params):
    token = get_fb_token(client_id, client_secret)
    if not token:
        return {'KO': 'Can not get fb token.'}
    params.update(token)
    response = requests.post('https://graph.facebook.com/%s/%s' % (facebook_id, action), params=params)
    return {'OK':response.text}


@task
def post_on_wall(page_secret, facebook_id, message):
    params = {}
    token = get_page_token(page_secret)
    if not token:
        return {'KO': 'Can not get fb token.'}
    params.update(token)
    params['id'] = facebook_id
    params['message'] = message
    response = requests.post('https://graph.facebook.com/feed', params=params)
    return {'OK':response.text}


@task
def post_on_page(page_secret, link, name, description, properties, actions):
    params = {}
    token = get_page_token(page_secret)
    if not token:
        return {'KO': 'Can not get fb token.'}
    params.update(token)
    params['link'] = link
    params['caption'] = link
    params['name'] = name
    params['description'] = description
    params['picture'] = '%s/leadImage_mini' % link
    params['properties'] = json.dumps(properties)
    params['actions'] = json.dumps(actions)
    response = requests.post('https://graph.facebook.com/facciamoadesso/feed', params=params)
    return {'OK':response.text}

