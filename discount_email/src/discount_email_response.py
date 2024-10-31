
import base64
import pickle
from email.mime.text import MIMEText
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from jinja2 import Environment, PackageLoader, select_autoescape

from discount_email.src.logger import logger

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_creds():
    logger.info("Getting credentials")
    token_path = Path('..', 'token.pickle')
    creds = None
    if token_path.exists():
        with token_path.open('rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with token_path.open('wb') as token:
            pickle.dump(creds, token)
    return creds


def get_gmail_service():
    logger.info("Getting Gmail service")
    creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_emails(service):
    logger.info("Getting emails using Gmail service")
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    return results.get('messages', [])


def get_email_content(service, msg_id):
    logger.info(f"Getting email {msg_id}")
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    headers = payload['headers']

    subject = next(header['value'] for header in headers if header['name'] == 'Subject')
    sender = next(header['value'] for header in headers if header['name'] == 'From')

    if (parts := payload.get('parts')):
        body = parts[0]['body']
    else:
        body = payload['body']

    data = body.get('data', "")
    content = base64.urlsafe_b64decode(data).decode('utf-8')

    return subject, sender, content


def create_draft_response(service, to, subject, body):
    logger.info(f"Creating Draft response for {to}")
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    draft = {'message': {'raw': raw}}

    service.users().drafts().create(userId='me', body=draft).execute()


def generated_response(name, reason, sender):
    logger.info(f"Generating response for reason: {reason}")
    env = Environment(
        loader=PackageLoader("discount_email_response"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("discount.html")
    args = {
        'name': name,
        'reason': reason,
        'sender': sender,
    }
    return template.render(**args)
