from pyramid.view import view_config
from pyramid_mailer import get_mailer

from restarter.notify import sms, emails, facebook


@view_config(route_name='page_product_notify', renderer='json', request_method='POST')
def page_product_notify(request):
    settings = request.registry.settings
    page_secret = settings.get('fb.page_secret')
    product_url = request.params.get('product_url')
    if not product_url:
        return {'KO': 'No product_url provided.'}
    product_title = request.params.get('product_title')
    if not product_title:
        return {'KO': 'No product_title provided.'}
    product_description = request.params.get('product_description')
    if not product_description:
        return {'KO': 'No product_description provided.'}

    facebook.post_on_page.delay(page_secret,
                            product_url,
                            product_title.title(),
                            product_description,
                            '%s/leadImage_mini' % product_url,
                            {'Tipo': {'text': 'Prodotti di Facciamo', 'href': 'http://www.facciamoadesso.it/prodotti'},
                             'Link': {'text': 'Azienda che lo vende', 'href': '%s/../../' % product_url}},
                            {"name": "Compra questo prodotto", 
                             "link": "%s/createObject?type_name=Order" % product_url
                            })
    return 'OK'


@view_config(route_name='page_company_notify', renderer='json', request_method='POST')
def page_company_notify(request):
    settings = request.registry.settings
    page_secret = settings.get('fb.page_secret')
    company_url = request.params.get('company_url')
    if not company_url:
        return {'KO': 'No company_url provided.'}
    company_title = request.params.get('company_title')
    if not company_title:
        return {'KO': 'No company_title provided.'}
    company_description = request.params.get('company_description')
    if not company_description:
        return {'KO': 'No company_description provided.'}

    facebook.post_on_page.delay(page_secret,
                                company_url,
                                company_title.title(),
                                company_description,
                                '%s/leadImage_mini' % company_url,
                                {'Tipo': {'text': 'Aziende di Facciamo', 'href': 'http://www.facciamoadesso.it/aziende'},
                                 'Link': {'text': 'Prodotti dell\'azienda', 'href': '%s/prodotti' % company_url}},
                                {"name": "Registrati ora", 
                                 "link": "http://www.facciamoadesso.it/il-progetto/partecipa"
                                })
    return 'OK'


@view_config(route_name='page_demand_notify', renderer='json', request_method='POST')
def page_demand_notify(request):
    settings = request.registry.settings
    page_secret = settings.get('fb.page_secret')
    demand_url = request.params.get('demand_url')
    if not demand_url:
        return {'KO': 'No demand_url provided.'}
    demand_title = request.params.get('demand_title')
    if not demand_title:
        return {'KO': 'No demand_title provided.'}
    demand_description = request.params.get('demand_description')
    if not demand_description:
        return {'KO': 'No demand_description provided.'}

    facebook.post_on_page.delay(page_secret,
                                demand_url,
                                demand_title.title(),
                                demand_description,
                                'http://www.facciamoadesso.it/logo_facciamo.png',
                                {'Tipo': {'text': 'Richieste di Facciamo', 'href': 'http://www.facciamoadesso.it/offerte'},
                                 'Link': {'text': 'Azienda che lo sta cercando', 'href': '%s/../../' % demand_url}},
                                {"name": "Registrati ora", 
                                 "link": "http://www.facciamoadesso.it/il-progetto/partecipa"
                                })
    return 'OK'


@view_config(route_name='page_newsitem_notify', renderer='json', request_method='POST')
def page_newsitem_notify(request):
    settings = request.registry.settings
    page_secret = settings.get('fb.page_secret')
    url = request.params.get('newsitem_url')
    if not url:
        return {'KO': 'No newsitem_url provided.'}
    title = request.params.get('newsitem_title')
    if not title:
        return {'KO': 'No title provided.'}
    description = request.params.get('description')
    if not description:
        return {'KO': 'No description provided.'}

    facebook.post_on_page.delay(page_secret,
                                url,
                                title.title(),
                                description,
                                '%s/image_mini' % url,
                                {'Altre notizie': {'text': 'www.facciamoadesso.it/notizie', 'href': 'http://www.facciamoadesso.it/notizie'}},
                                {"name": "Registrati ora", 
                                 "link": "http://www.facciamoadesso.it/il-progetto/partecipa"
                                })
    return 'OK'


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
    email_subject = request.params.get('email_subject', 'project notification')

    phone = request.params.get('phone')
    phone_message = request.params.get('phone_message')

    if not email_message and phone_message:
        return {'KO': 'No message provided.'}

    if not email and phone:
        return {'KO': 'No recipients.'}

    if email and email_message:
        mailer = get_mailer(request)
        emails.send_email.delay(mailer, email_message, email_subject, email)

    if phone and phone_message:
        sms.send_sms.delay(login, password, phone_message, phone)

    return 'OK'
