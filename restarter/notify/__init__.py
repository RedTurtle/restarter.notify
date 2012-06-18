
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid_mailer import get_mailer

from restarter.notify import sms, emails, facebook


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('notify', '/notify')
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


@view_config(route_name='notify', renderer='json', request_method='POST')
def notify(request):
    settings = request.registry.settings
    login = settings.get('sms.username')
    password = settings.get('sms.password')
    email = request.params.get('email')
    email_message = request.params.get('email_message')
    phone = request.params['phone']
    phone_message = request.params.get('phone_message')

    if not email_message and phone_message:
        return {'KO': 'No message provided.'}

    if not email and phone:
        return {'KO': 'No recipients.'}

    if email and email_message:
        mailer = get_mailer(request)
        emails.send_email.delay(mailer, email_message, email)

    if phone and phone_message:
        sms.send_sms.delay(login, password, phone_message, phone)

    return 'OK'
