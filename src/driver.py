#!/usr/bin/env python3
from os import environ

from . import logger
from .discount import (
    extract_info,
    is_discount_request_ai,
)
from .discount_email_response import (
    create_draft_response,
    generated_response,
    get_emails,
    get_email_content,
    get_gmail_service,
)


def main():
    assert environ["OPEN_AI_SECRET"]
    service = get_gmail_service()
    assert service is not None
    messages = get_emails(service)
    logger.info(f"{len(messages)} messages")

    for i, message in enumerate(messages):
        msg_id = message['id']
        logger.info(f"{'-' * 30} {i}/{len(messages)} {msg_id}")
        subject, sender, content = get_email_content(service, msg_id)

        try:
            request = is_discount_request_ai(content)
        except Exception:
            logger.exception("??")
        else:
            if request.is_discount:
                logger.info(
                    f"This supports the idea that a discount is requested: {request.ai_reason}"
                )
                name, email = extract_info(sender, content)
                response_body = generated_response(name, request.reason, sender)
                create_draft_response(service, email, f"Re: {subject}", response_body)
                print(f"Draft response created for {email}")


if __name__ == '__main__':
    main()
