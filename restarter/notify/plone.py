import os
import socket
from ftplib import FTP
from celery.task import task

TIMEOUT = 5

@task
def upload_photo(plone_key, filepath, filename, company_path):

    logger = upload_photo.get_logger()
    user, password = plone_key.split(':')
    photo = open(filepath, "rb")
    path = '%s/foto' % company_path
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
