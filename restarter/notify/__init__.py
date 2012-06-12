
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid_mailer import get_mailer

from restarter.notify import sms, emails, facebook


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('notify_sms', '/notify/sms')
    config.add_route('notify_email', '/notify/email')
    config.add_route('fb_register_notify', '/notify/fb/register')
    config.add_route('fb_sell_notify', '/notify/fb/sell')
    config.add_route('fb_newcompany_notify', '/notify/fb/newcompany')
    config.scan()
    return config.make_wsgi_app()


@view_config(route_name='fb_newcompany_notify', renderer='json', request_param='facebook_id', request_method='POST')
def fb_newcompany_notify(request):
    company_url = request.params.get('company_url')
    if not company_url:
        return {'KO': 'No company_url provided.'}
    settings = request.registry.settings
    client_id = settings.get('fb.app_id')
    client_secret = settings.get('fb.app_secret')
    facebook_id = request.params['facebook_id']
    facebook.post_an_action.delay(client_id, client_secret, facebook_id, 'facciamoadesso:newcompany', company=company_url)
    return 'OK'


@view_config(route_name='fb_sell_notify', renderer='json', request_param='facebook_id', request_method='POST')
def fb_sell_notify(request):
    product_url = request.params.get('product_url')
    if not product_url:
        return {'KO': 'No product_url provided.'}
    settings = request.registry.settings
    client_id = settings.get('fb.app_id')
    client_secret = settings.get('fb.app_secret')
    facebook_id = request.params['facebook_id']
    facebook.post_an_action.delay(client_id, client_secret, facebook_id, 'facciamoadesso:sell', product=product_url)
    return 'OK'


@view_config(route_name='fb_register_notify', renderer='json', request_param='facebook_id', request_method='POST')
def fb_register_notify(request):
    settings = request.registry.settings
    client_id = settings.get('fb.app_id')
    client_secret = settings.get('fb.app_secret')
    facebook_id = request.params['facebook_id']
    facebook.post_an_action.delay(client_id, client_secret, facebook_id, 'facciamoadesso:register', website='http://www.facciamoadesso.it')
    return 'OK'


@view_config(route_name='notify_email', renderer='json', request_param='email', request_method='POST')
def email_notify(request):
    email = request.params.get('email')
    message = request.params.get('message')
    if not message:
        return {'KO': 'No message provided.'}

    mailer = get_mailer(request)
    emails.send_email.delay(mailer, message, email)
    return 'OK'


@view_config(route_name='notify_sms', renderer='json', request_param='phone', request_method='POST')
def sms_notify(request):
    settings = request.registry.settings
    phone = request.params['phone']
    message = request.params.get('message')
    if not message:
        return {'KO': 'No message provided.'}

    login = settings.get('sms.username')
    password = settings.get('sms.password')
    sms.send_sms.delay(login, password, message, phone)
    return 'OK'

