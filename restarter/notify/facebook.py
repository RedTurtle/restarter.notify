from urlparse import parse_qsl
import requests
from celery.task import task


def get_fb_token(client_id, client_secret):
    params = {'grant_type': 'client_credentials',
              'client_id': client_id,
              'client_secret': client_secret}
    response = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
    if response.status_code == 200:
        return dict(parse_qsl(response.content))


@task
def post_an_action(client_id, client_secret, facebook_id, action, **params):
    token = get_fb_token(client_id, client_secret)
    if not token:
        return {'KO': 'Can not get fb token.'}
    params.update(token)
    response = requests.post('https://graph.facebook.com/%s/%s' % (facebook_id, action), params=params)
    return {'OK':response.text}


@task
def post_on_wall(client_id, client_secret, facebook_id, message, endpoint):
    params = {}
    token = get_fb_token(client_id, client_secret)
    if not token:
        return {'KO': 'Can not get fb token.'}
    params.update(token)
    params['id'] = facebook_id
    params['message'] = message
    response = requests.post('https://graph.facebook.com/feed', params=params)
    return {'OK':response.text}
