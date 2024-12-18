import re

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

from discount_email.src.logger import logger

client = instructor.from_openai(OpenAI())


class DiscountRequest(BaseModel):
    is_discount: bool = Field(..., description="Whether the user is requesting a discount or not")
    reason: str = Field(..., description="Simple summary of why the user wants a discount")
    ai_reason: str = Field(
        ..., description="Excerpt from the email that supports the conclusion that the user wants a discount"
    )


def generate(data: str) -> DiscountRequest:
    system_prompt = (
        "Please analyze the following email from a user. The user may be asking for a discount on the price of a course.\n"
        "We don't care if the user is offering a discount.\n"
        "These are not discount requests:\n"
        "- political donation solicitations\n"
        "- anything mentioning Donald Trump or Kamala Harris\n"
        "- offers to sell some item (including subscriptions, homes, books, stock services)\n"
        "- offers to give away some item\n"
        "- offers of a discount\n"
    )
    user_prompt = (
        "Create the DiscountRequest for the following email:\n"
        "-----\n"
        f"{data}\n"
        "-----\n"
        "If the email includes a request for a discount, then: \n"
        "- set is_discount to True\n"
        "- use the reason field to summarize briefly the user's reason for wanting the discount\n"
        "- use the ai_reason field to show the text in the email that most strongly supports the conclusion that a discount is requested\n"
        "else set the is_discount field to False."
    )

    return client.chat.completions.create(
        model="gpt-4o",
        # gpt-4o-mini is less expensive, but it does not reliably categorize emails correctly
        # model="gpt-4o-mini",
        response_model=DiscountRequest,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )


def is_discount_request_ai(content) -> bool:
    logger.info("Checking email for whether it is a discount request")
    assert client
    return generate(content)


def extract_info(sender, content):
    name = re.search(r'(?:^|\s)([A-Z][a-z]+ [A-Z][a-z]+)', sender)
    name = name.group(1) if name else "Customer"

    email = re.search(r'[\w\.-]+@[\w\.-]+', sender).group(0)
    logger.info(f"extract info: {sender = } {content[:100] = }")
    return name, email
