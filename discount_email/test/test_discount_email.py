import pytest

from discount_email.src.discount import is_discount_request_ai

# Email text

manning_text = """
9 HOURS LEFT!

Save half on all print books, including MEAP preorders.

Plus save 35% on everything else.

Offer ends midnight PT tonight. Only at manning.com.

The witching hour is soon! In just a few hours we’ll roll over to another special sale!
"""

udacity_text = """
Time is running out!

This offer isn't a trick—get 40% off before it's gone

Use code TREAT40 at checkout to unlock 40% off your Udacity subscription. Offer ends Sunday, November 3rd. Don't be left with an outdated skillset.
"""

oreilly1_text = """
Hurry. Because before you know it this deal will be *poof* gone.

Jump on this deal by midnight on October 31 to lock in a year at 40% off.

Use code FLASHSALE2024
Expires October 31
"""

oreilly2_text = """
This offer is nontransferable and expires on October 31, 2024, at 11:59pm PT. This offer is for individual memberships only. Team (multiuser) and enterprise accounts are not eligible. The US$299/year offer is valid for the first year of your membership. Memberships renew at the then-current price (currently US$499/year) unless you cancel in accordance with our Membership Agreement. Tax not included.
"""

fullstack_io_text = """
Louis is a Tech Lead with a decade of experience in startups and consulting. He’s built GenAI applications for international organizations (UNESCO, Singapore Government, etc.) and private companies (Renault, Private Equity Funds).

And now that you’ve stayed with me in my agony of writing this email, I have a Gift, especially for you:

You can check out the entire first 5 lessons of the course for free!

If you’re hooked on this newfound enlightenment, don’t forget to check out Responsive LLM Applications with Server-Sent Events with Louis Sanna. (Currently on sale)
"""

ama_build_text = """
What have you built? Send a photo and a short description to AMA’s social media manager, Lee Ray, for possible inclusion on the I Fly AMA Facebook page. And don’t forget the October issue of Model Aviation is dedicated to building and the AMA Plans Service is offering 20% off of all orders until October 31! Additional resources can be found at www.modelaircraft.org/IBUILDAMA.
"""

trading1_text = """
Right now, this revolutionary tool is running in demo mode, but it’s moving into live trading in 2025. Ready to join the first wave of fully automated trading? Make sure you’re on the waiting list— Premium subscribers get first dibs on entering their names on the list when it opens up.

Join Premium Today!
Save 25% with code MONSTER25
Hit refresh on your trading game. This is trading as it should be
"""


trading2_text = """
P.S. Spots on the waitlist are limited, and first come first served. Don’t miss your chance—join premium and be ready for the next round.
"""

fandango1_text = """
Buy movie tickets through your Fandango account on fandango.com or the Fandango app or movietickets.com, and receive 125 Fandango FanRewardsPoints for each movie ticket. All or at least some portion of the purchase for each ticket must be paid using a credit or debit card, PayPal, credit in your Fandango account from a prior exchanged purchase or a Fandango gift card (i.e., if you use a promo code then only part of that purchase can be paid for using the promo code) to qualify for FanRewards Points. Movie tickets must be for a movie with a showtime starting before 11:59pm PT on the last day of the promotion period. When you receive 500 FanRewards Points, you will receive a $5.00 Discount Reward which you will need to convert into a Discount Promo Code for use on a qualifying purchase on http://www.fandango.com (which can be used on http://www.movietickets.com) or http://www.FandangoAtHome.com.
"""


matt_harrison1_text = """
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


matt_harrison2_text = """

Hey Hugh ,

It’s Halloween, and we’re kicking off a series of spine-tingling flash sales you won’t want to miss! If the thought of mastering Python gives you chills, we’ve got the perfect antidote for you:

🎉 Learning Python for Data is 30% off for the next 24 hours! 🎉

Imagine walking into your next project confidently, with no gaps in your Python foundation to trip you up. With Learning Python for Data, you’ll breeze through the fundamentals that every data scientist and analyst needs to know. From core syntax to data structures and common libraries, this guide will ensure you start strong.

You have 3 options:

Just the book

Book and video course

Book, course, and personal calls

https://store.metasnake.com/learningpy use coupon LEARNPY

Why Grab It Now?
Because like any good Halloween scare, this discount will disappear in just 24 hours! When the clock strikes midnight, the price goes back up. Secure this essential guide and get ready to build a rock-solid foundation that’ll last you a lifetime.

🎃 Halloween Deal: 30% Off!

Don’t let Python haunt you anymore – tackle it with confidence!

Happy Halloween,
Matt Harrison

P.S. Stay tuned for more spooktacular flash sales this week!
"""

subscriber_text = "Latest articles\nIf you’re not a subscriber, here’s what you missed this month."


scale_up_ai_text = """
Join Insight Partners at ScaleUp:AI
ScaleUp:AI just released passes for their developer-focused conference.

Top engineers from Google, Meta, Bardeen, Writer, and Databricks present technical deep-dives on AI implementation and deployment.

The program covers AI systems architecture, adoption frameworks, and industry-specific optimization.

Virtual attendees get direct access to a Q&A session with Andrew Ng, pioneering ML researcher.

Get virtual access now: $99 with code Alpha99 for AlphaSignal readers (regular price $159).
"""

# Fixtures

@pytest.fixture
def manning():
    return manning_text


@pytest.fixture
def udacity():
    return udacity_text


@pytest.fixture
def oreilly1():
    return oreilly1_text


@pytest.fixture
def oreilly2():
    return f"{oreilly1_text}\n{oreilly2_text}"


@pytest.fixture
def fullstack_io():
    return fullstack_io_text


@pytest.fixture
def ama_build():
    return ama_build_text


@pytest.fixture
def trading1():
    return trading1_text


@pytest.fixture
def trading2():
    return trading2_text


@pytest.fixture
def fandango1():
    return fandango1_text


@pytest.fixture
def matt_harrison1():
    return matt_harrison1_text


@pytest.fixture
def matt_harrison2():
    return matt_harrison2_text


@pytest.fixture
def subscriber():
   return subscriber_text


@pytest.fixture
def scaleup_ai():
   return scale_up_ai_text


# Tests

def test_subscriber_no_discount_request(subscriber):
    request = is_discount_request_ai(subscriber)
    assert not request.is_discount


def test_matt_harrison1_no_discount_request(matt_harrison1):
    request = is_discount_request_ai(matt_harrison1)
    assert not request.is_discount


def test_matt_harrison2_no_discount_request(matt_harrison2):
    request = is_discount_request_ai(matt_harrison2)
    assert not request.is_discount


def test_fandango1_no_discount_request(fandango1):
    request = is_discount_request_ai(fandango1)
    assert not request.is_discount


def test_trading1_no_discount_request(trading1):
    request = is_discount_request_ai(trading1)
    assert not request.is_discount


def test_trading2_no_discount_request(trading2):
    request = is_discount_request_ai(trading2)
    assert not request.is_discount


def test_ama_build_no_discount_request(ama_build):
    request = is_discount_request_ai(ama_build)
    assert not request.is_discount


def test_fullstack_io_no_discount_request(fullstack_io):
    request = is_discount_request_ai(fullstack_io)
    assert not request.is_discount


def test_oreilly1_no_discount_request(oreilly1):
    request = is_discount_request_ai(oreilly1)
    assert not request.is_discount


def test_oreilly2_no_discount_request(oreilly2):
    request = is_discount_request_ai(oreilly2)
    assert not request.is_discount


def test_udacity_no_discount_request(udacity):
    request = is_discount_request_ai(udacity)
    assert not request.is_discount


def test_manning_no_discount_request(manning):
    request = is_discount_request_ai(manning)
    assert not request.is_discount


def test_scaleup_ai_no_discount_request(scaleup_ai):
    request = is_discount_request_ai(manning)
    assert not request.is_discount
