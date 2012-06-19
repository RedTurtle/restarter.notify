from pyramid_mailer.message import Message
from celery.task import task

FROM = "info@facciamoadesso.it"

@task
def send_email(mailer, message, subject, email):
    subject = '[FacciamoAdesso] %s' % subject
    message = Message(subject = subject,
                      sender = FROM,
                      recipients=[email],
                      body = message)
    mailer.send_immediately(message)
    return {'OK': 'Done'}
