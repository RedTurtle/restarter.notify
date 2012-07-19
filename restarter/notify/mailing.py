from pyramid_mailer.message import Message
from celery.task import task

FROM = "info@facciamoadesso.it"

@task
def send_emails(mailer, body, subject, emails):
    response = ['Mail send to,']
    subject = '[FacciamoAdesso] %s' % subject
    for email in set(emails):
        if email:
            message = Message(subject = subject,
                              sender = FROM,
                              recipients=[email],
                              body = body)
            mailer.send_immediately(message)
            response.append(email)
    return {'OK': ', '.join(response)}
