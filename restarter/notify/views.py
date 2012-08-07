import json
import requests
import hashlib, hmac
import os

from tempfile import mkstemp
from pyramid.view import view_config
from pyramid_mailer import get_mailer
from pyramid.httpexceptions import HTTPForbidden

from restarter.notify import sms, mailing, facebook, plone


BUFFER_SIZE = 8192
SHARE_LINK = 'http://www.facebook.com/share.php?u=%s'
PLONE = 'http://localhost:8081/restarter/%s'

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
                            {'Altre prodotti': {'text': 'http://www.facciamoadesso.it/prodotti', 'href': 'http://www.facciamoadesso.it/prodotti'},
                             'Link': {'text': 'Compra questo prodotto', 'href': "%s/createObject?type_name=Order" % product_url}},
                            {"name": "Share", 
                             "link": SHARE_LINK % product_url}
                            )
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
                                {'Aziende di Facciamo': {'text': 'http://www.facciamoadesso.it/aziende', 'href': 'http://www.facciamoadesso.it/aziende'},
                                 'Link': {'text': 'Prodotti dell\'azienda', 'href': '%s/prodotti' % company_url}},
                                {"name": "Share", 
                                 "link": SHARE_LINK % company_url}
                                )
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
                                {'Richieste di Facciamo': {'text': 'http://www.facciamoadesso.it/offerte', 'href': 'http://www.facciamoadesso.it/offerte'},
                                 'Link': {'text': 'Azienda che lo sta cercando', 'href': '%s/../../' % demand_url}},
                                {"name": "Share", 
                                 "link": SHARE_LINK % demand_url}
                                )
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
    description = request.params.get('newsitem_description')
    if not description:
        return {'KO': 'No description provided.'}

    facebook.post_on_page.delay(page_secret,
                                url,
                                title.title(),
                                description,
                                '%s/image_mini' % url,
                                {'Altre notizie': {'text': 'www.facciamoadesso.it/notizie', 'href': 'http://www.facciamoadesso.it/notizie'}},
                                {"name": "Share", 
                                 "link": SHARE_LINK % url}
                                )
    return 'OK'


@view_config(route_name='page_companystory_notify', renderer='json', request_method='POST')
def page_companystory_notify(request):
    settings = request.registry.settings
    page_secret = settings.get('fb.page_secret')
    url = request.params.get('item_url')
    if not url:
        return {'KO': 'No item_url provided.'}
    title = request.params.get('item_title')
    if not title:
        return {'KO': 'No title provided.'}
    description = request.params.get('item_description')
    if not description:
        return {'KO': 'No description provided.'}

    facebook.post_on_page.delay(page_secret,
                                url,
                                title.title(),
                                description,
                                '%s/leadImage_mini' % url,
                                {'Altre storie': {'text': 'www.facciamoadesso.it/storie', 'href': 'http://www.facciamoadesso.it/storie'}},
                                {"name": "Share", 
                                 "link": SHARE_LINK % url}
                                )
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
    emails = request.params.get('emails')
    if emails:
        emails = json.loads(emails)
    else:
        emails = []
    if email:
        emails.append(email)
    email_message = request.params.get('email_message')
    email_subject = request.params.get('email_subject', 'project notification')

    phone = request.params.get('phone')
    phone_message = request.params.get('phone_message')

    if not email_message and phone_message:
        return {'KO': 'No message provided.'}

    if not emails and phone:
        return {'KO': 'No recipients.'}

    if emails and email_message:
        mailer = get_mailer(request)
        mailing.send_emails.delay(mailer, email_message, email_subject, emails)

    if phone and phone_message:
        sms.send_sms.delay(login, password, phone_message, phone)

    return 'OK'


def verify(api_key, token, timestamp, signature):
        return signature == hmac.new(key=api_key,
                                     msg='{}{}'.format(timestamp, token),
                                     digestmod=hashlib.sha256).hexdigest()


def serialize_upload(input_file, length, filename):
    fd, filepath = mkstemp()
    with os.fdopen(fd,'wb') as output:
        q, r = divmod(length, BUFFER_SIZE)
        buffers = [BUFFER_SIZE] * q + [r]
        while buffers:
            chunk = input_file.read(buffers.pop(0))
            if not chunk:
                # We will get there only if the content length (advertised
                # by the browser) is larger than the effective length of
                # the file, which should not happen.
                break
            output.write(chunk)
            output.flush()
    return filepath

@view_config(route_name='mailgun_photos', renderer='json', request_method='POST')
def mailgun_photos(request):

    settings = request.registry.settings
    plone_key = settings.get('plone.key')
    api = settings.get('mailgun.api')
    token = request.params.get('token')
    signature = request.params.get('signature')
    timestamp = request.params.get('timestamp')

    sender = request.params.get('sender')
    uid = request.matchdict['uid']
    response = requests.get(PLONE % 'path_from_uid?uid=%s&sender=%s' % (uid,sender))
    if response.status_code != 200:
        raise HTTPForbidden()
    company_path = response.text

    isvalid = verify(api, token, timestamp, signature)
    if not isvalid:
        raise HTTPForbidden()

    attachments_length = int(request.params.get('attachment-count','0')) + 1

    for n in range(1,attachments_length):
        attachment = request.params.get('attachment-%s' % n)
        #attachment = request.params.get('fileattachment-%s' % n)
        if attachment is not None:
            attachment_path = serialize_upload(attachment.file, attachment.length, attachment.filename) 
            plone.upload_photo.delay(plone_key,
                               attachment_path,
                               attachment.filename,
                               company_path)

    return 'OK'

