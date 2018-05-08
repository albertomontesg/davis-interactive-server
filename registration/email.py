import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httplib2
import oauth2client
from apiclient import discovery, errors
from django.conf import settings
from oauth2client import client, tools


def send_message(sender, to, subject, msg):
    """ Send email using Google Gmail API.
    """
    message = create_message_html(sender, to, subject, msg)
    if not settings.EMAIL_SILENT:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        result = send_message_internal(service, "me", message)
        return result
    # Silent email sending printing on terminal
    print(base64.urlsafe_b64decode(message['raw']).decode())
    return message


def get_credentials():
    credential_dir = settings.EMAIL_SECRETS_DIR
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    secret_file = os.path.join(settings.EMAIL_SECRETS_DIR,
                               settings.EMAIL_CLIENT_SECRET_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_file, settings.EMAIL_SCOPE)
        flow.user_agent = settings.EMAIL_APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def send_message_internal(service, user_id, message):
    message = (service.users().messages().send(userId=user_id,
                                               body=message).execute())
    print('Message Id: %s' % message['id'])
    return message


def create_message_html(sender, to, subject, msg):
    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}
