from pyramid_mailer.message import Message
from celery.task import task

SUBJECT = "Notification from restartER project"
FROM = "admin@restarter.it"

@task
def send_email(mailer, message, email):
    message = Message(subject = SUBJECT,
                      sender = FROM,
                      recipients=[email],
                      body = message)
    mailer.send_immediately(message)
    return {'OK': 'Done'}
