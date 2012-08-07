import os
import socket
from ftplib import FTP
from celery.task import task
from restarter.notify import mailing

TIMEOUT = 5
MESSAGE = """You have just uploaded %s into http://www.facciamoadesso.it%s folder.

-------------------
Il team di Facciamo"""


@task
def upload_photo(plone_key, filepath, filename, company_path, mailer, sender):

    logger = upload_photo.get_logger()
    user, password = plone_key.split(':')
    photo = open(filepath, "rb")
    path = '%s/foto' % company_path
    path = path.encode('utf8', 'ignore')
    if not path.startswith('/restarter'):
        return 'WRONG PATH %s' % path
    #upload using ftp
    try:
        ftp = FTP()
        ftp.connect('localhost', 8021, TIMEOUT)
        ftp.login(user, password)
        ftp.cwd(path)
        logger.info('Uploading %s to %s' % (filename, path))
        ftp.storbinary("STOR %s" % filename, photo, 1024)
        logger.info('Finished uploading %s' % filename)
        ftp.close()
    except socket.timeout, exc:
        photo.close()
        upload_photo.retry(exc=exc)

    photo.close()
    os.remove(filepath)

    mailing.send_emails.delay(mailer, MESSAGE % (filename, path), 'Photo upload confirmation', [sender,])
