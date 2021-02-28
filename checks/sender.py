# https://pypi.org/project/pyhibp/#description
import pyhibp


HIBP_API_KEY = None
# Set the API key prior to using the functions which require it.
pyhibp.set_api_key(key=HIBP_API_KEY)

# Get pastes affecting a given email address
resp = pyhibp.get_pastes(email_address="test@example.com")

# Get breaches that affect a given account
resp = pyhibp.get_account_breaches(account="test@example.com", truncate_response=True)