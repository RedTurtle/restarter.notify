import datetime

from dogpile.cache import make_region
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid_mailer import get_mailer

from restarter.notify import sms, emails


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('notify', '/notify')
    config.scan()
    return config.make_wsgi_app()


@view_config(route_name='notify', renderer='json', request_param='message') #request_method='POST')
def notify(request):

    settings = request.registry.settings
    message = request.params['message']
    phone = request.params.get('phone')
    email = request.params.get('email')

    status = []

    if phone:
        login = settings.get('sms.username')
        password = settings.get('sms.password')
        sms.send_sms.delay(login, password, message, phone)
        status.append('SMS sent')

    if email:
        mailer = get_mailer(request)
        emails.send_email.delay(mailer, message, email)
        status.append('Email sent')

    return status


@view_config(route_name='notify', renderer='json', request_param='userid')
def mytest(request):
    return load_user_info(request.params['userid'])

region = make_region().configure('dogpile.cache.redis',
                                  expiration_time = 10,
                                  arguments = {'host': 'localhost',
                                               'port': 6379,
                                               'db': 0,
                                               'redis_expiration_time': 60*60*2,   # 2 hours
                                               'distributed_lock':True
                                               })

@region.cache_on_arguments()
def load_user_info(userid):
    print 'getting number'
    return str(datetime.datetime.now())
