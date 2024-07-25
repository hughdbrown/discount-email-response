#!/usr/bin/env python3

from email.mime.text import MIMEText
import base64
import pickle
from pathlib import Path 

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from jinja2 import Environment, PackageLoader, select_autoescape

from discount import (
    # is_discount_request,
    is_discount_request_ai,
    extract_info,
)
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_creds():
    token_path = Path('token.pickle')
    creds = None
    if token_path.exists():
        with token_path.open('rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with token_path.open('wb') as token:
            pickle.dump(creds, token)
    return creds


def get_gmail_service():
    creds = get_creds() 
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    return results.get('messages', [])


def get_email_content(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    headers = payload['headers']
    
    subject = next(header['value'] for header in headers if header['name'] == 'Subject')
    sender = next(header['value'] for header in headers if header['name'] == 'From')
    
    if 'parts' in payload:
        parts = payload['parts']
        data = parts[0]['body']['data']
    else:
        data = payload['body']['data']
    
    content = base64.urlsafe_b64decode(data).decode('utf-8')
    
    return subject, sender, content


def create_draft_response(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    draft = {'message': {'raw': raw}}
    
    service.users().drafts().create(userId='me', body=draft).execute()


def generated_response(name, reason, sender):
    env = Environment(
        loader=PackageLoader("discount-email-response"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("discount.html")
    args = {
        'name': name,
        'reason': reason,
        'sender': sender,
    }
    return template.render(**args) 


def main():
    load_dotenv()
    service = get_gmail_service()
    messages = get_emails(service)
    
    for message in messages:
        msg_id = message['id']
        print(f"{'-' * 30} {msg_id}")
        subject, sender, content = get_email_content(service, msg_id)
        
        try:
            request = is_discount_request_ai(content)
        except Exception as exc:
            print(f"Exception: {exc}")
        else:
            if request.is_discount:
                print(f"This supports the idea that a discount is requested: {request.ai_reason}")
                name, email = extract_info(sender, content)
                response_body = generated_response(name, request.reason, sender)
                create_draft_response(service, email, f"Re: {subject}", response_body)
                print(f"Draft response created for {email}")


if __name__ == '__main__':
    main()
