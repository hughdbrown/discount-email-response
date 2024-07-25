import re

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


client = instructor.from_openai(OpenAI())


class DiscountRequest(BaseModel):
    is_discount: bool = Field(..., description="Whether the user is requesting a discount or not")
    reason: str = Field(..., description="Simple summary of why the user wants a discount")
    ai_reason: str = Field(..., description="Excerpt from the email that supports the conclusion that the user wants a discount")


def is_discount_request(content) -> bool:
    # Simple check for discount-related keywords
    keywords = ['discount', 'coupon', 'promo', 'sale', 'deal']
    return any(keyword in content.lower() for keyword in keywords)


def generate(data: str) -> DiscountRequest:
    return client.chat.completions.create(
        # model="gpt-3.5-turbo-0613",
        # model="gpt-3.5-turbo",
        # model="gpt-4o",
        model="gpt-4o-mini",
        response_model=DiscountRequest,
        messages=[
            {
                "role": "system",
                "content":
                    "The following is an email from a user. "
                    "The user may be asking for a discount on the price of a course.",
            },
            {
                "role": "user",
                "content": 
                    "Create the DiscountRequest for the following email:\n"
                    "-----\n"
                    f"{data}\n"
                    "-----\n"
                    "These are not discount requests:\n"
                    "- political donation solicitations\n"
                    "- anything mentioning Donald Trump or Kamala Harris\n" 
                    "- offers to sell some item (including subscriptions, homes, books, stock services)\n"
                    "- offers to give away some item\n"
                    "- offers of a discount\n"
                    "If the email includes a request for a discount, then: \n"
                    "- set is_discount to True\n"
                    "- use the reason field to summarize briefly the user's reason for wanting the discount\n"
                    "- use the ai_reason field to show the text in the email that most strongly supports the conclusion that a discount is requested\n"
                    "else set the is_discount field to False.",
            },
        ],
    )


def is_discount_request_ai(content) -> bool:
    return generate(content)


def extract_info(sender, content):
    name = re.search(r'(?:^|\s)([A-Z][a-z]+ [A-Z][a-z]+)', sender)
    name = name.group(1) if name else "Customer"
    
    email = re.search(r'[\w\.-]+@[\w\.-]+', sender).group(0)
    
    # reason = re.search(r'(?i)(?:because|reason|why).*?([^.!?]+[.!?])', content)
    # reason = reason.group(1).strip() if reason else "No specific reason provided."
    #
    #return name, email, reason
    return name, email
