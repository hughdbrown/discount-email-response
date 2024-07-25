# Purpose
Attempt to automate email responses. Friend runs a course that is popular and overwhelmed with requests for discounts.

So here is an OpenAI prompt to try to respond to this problem as economically as possible:
```
Write some code that I can plug into my gmail account (so that the code automatically reads my email in gmail, one email at a time) and have it:
- determine whether this is a person asking for a discount and if so
- determine the user's name, email address, and reason for wanting a discount, then
- craft an email response explaining the discount policy and storing this in my Drafts folder.
```

# Installation

1. Python setup
```
# Make a virtualenv
pyenv virtualenv 3.12.0 discount
pyenv activate discount

# Run the code
./discount-email-response.py
```

2. Set Up Gmail API
* Go to the [Google Cloud Console](https://console.cloud.google.com/welcome).
* Create a new project.
* Enable the Gmail API for your project.
* Create credentials for a Desktop application.
* Download the credentials file (`credentials.json`).
