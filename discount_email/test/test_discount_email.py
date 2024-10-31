import pytest

from discount_email.src.discount import is_discount_request_ai


@pytest.fixture
def matt_harrison():
    return """
Hey Hugh

If interviews still give you the chills, we’ve got a treat for you. For the next 24 hours, Effective Python Interviews is 30% off! 🎉

Imagine walking into your next interview and nailing every question confidently, without breaking a sweat. With Effective Python Interviews, you’ll be fully prepared to tackle even the trickiest Python problems and showcase your expertise in a way that impresses hiring managers.

Python Fundamentals and Advanced Topics: Master essential topics that appear in interviews with clear, practical explanations.

Real Coding Challenges and Solutions: Learn to think like an interviewer, with exercises and answers to boost your problem-solving skills.

Project Presentation Tips: Discover how to structure your GitHub projects and create a standout first impression.

Passion Project Insights: Learn how to connect your personal projects to the job, showing your enthusiasm and expertise.

Behavioral Interview Guidance: Tips on communicating your experience and insights so your personality shines through.

🎃 Halloween Flash Sale: 30% Off !

This is your chance to exorcise those interview jitters for good—offer ends at midnight!

Grab My 30% Discount Before It’s Gone ➜

https://store.metasnake.com/effective-python-interviews-digital-book?coupon=INTERVIEW30

With tips, strategies, and insights crafted to boost your Python interview performance, this guide is the edge you’ve been looking for.

Don’t wait! Like any good Halloween mystery, this deal will vanish into the mist soon.

Best of luck with your Python journey,  

Matt

P.S. Keep an eye out for more Halloween flash sales
"""

@pytest.fixture
def subscriber():
   return "Latest articles\nIf you’re not a subscriber, here’s what you missed this month." 

def test_subscriber_success(subscriber):
    try:
        content = subscriber
        request = is_discount_request_ai(content)
    except Exception as exc:
        print(f"Exception: {exc}")
        assert False
    else:
        assert not request.is_discount

def test_matt_harrison_success(matt_harrison):
    try:
        content = matt_harrison
        request = is_discount_request_ai(content)
    except Exception as exc:
        print(f"Exception: {exc}")
        assert False
    else:
        assert not request.is_discount

