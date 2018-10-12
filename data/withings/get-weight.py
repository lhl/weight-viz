import arrow
import json
from   nokia import NokiaApi, NokiaAuth, NokiaCredentials
from   pprint import pprint
import sys
from urllib.parse import parse_qs, urlparse

# This will break 2018-11-30 if endpoint isn't updated:
# https://github.com/orcasgit/python-nokia/pull/24

# Config File
if len(sys.argv) == 2:
  CFN = sys.argv[1]
else:
  CFN = 'nokia.config.json'


# Load up credentials, if we don't have credentials, launch 
def main():
  try:
    # Let's try to load up the config file...
    with open(CFN) as cf:
      c = json.load(cf)
    creds = NokiaCredentials(
              access_token=c['access_token'],
              token_expiry=c['token_expiry'],
              token_type=c['token_type'],
              refresh_token=c['refresh_token'],
              user_id=c['user_id'],
              client_id=c['client_id'],
              consumer_secret=c['consumer_secret'],
            )
  except:
    # Can't get credentials, let's go through the process...
    creds = nokia_auth()

  # And now we're ready to get our weights...
  get_weight(creds)


def nokia_auth():
  print('First we need your Client ID, Consumer Secret, and Callback URI')
  print('You can find it here: https://account.withings.com/partner/dashboard_oauth2')
  client_id = input('client_id: ')
  consumer_secret = input('consumer_secret: ')
  callback_uri = input('callback_uri: ')

  auth = NokiaAuth(client_id, consumer_secret, callback_uri=callback_uri)
  authorize_url = auth.get_authorize_url()
  print('Now you should open this authorization URL and give the app access: ')
  print(authorize_url)
  auth_url = input('Enter the response URL: ')

  # We have to parse the URL to extract the code from the query string
  u = urlparse(auth_url)
  auth_code = parse_qs(u.query)['code'][0]
  creds = auth.get_credentials(auth_code)

  # Save this so we don't have to do this again
  save_creds(creds)

  # Pass back
  return creds


def save_creds(creds):
  j = {
    'access_token': creds.access_token,
    'token_expiry': creds.token_expiry,
    'token_type': creds.token_type,
    'refresh_token': creds.refresh_token,
    'user_id': creds.user_id,
    'client_id': creds.client_id,
    'consumer_secret': creds.consumer_secret,
  }

  with open(CFN, 'w') as cf:
      c = json.dump(j, cf)


def get_weight(creds):
  client = NokiaApi(creds)

  # Refresh credentials if necessary
  # creds = client.get_credentials()


  # http://developer.withings.com/oauth2/#tag/measure%2Fpaths%2Fhttps%3A~1~1wbsapi.withings.net~1measure%3Faction%3Dgetmeas%2Fget
  # lastupdate for syncing...
  # 'timezone': 'America/Los_Angeles',
  # 'updatetime': <Arrow [2018-10-12T08:14:44+00:00]>}

  measures = client.get_measures(meastype=1, category=1, lastupdate=1534748400) # limit=1)
  for measure in measures:
    '''
    pprint(vars(measure))
    pprint('---')
    pprint(vars(measures))
    sys.exit()
    '''

    pprint(measure.date)
    pprint(measure.weight)
    print()


if __name__ == '__main__':
  main()
