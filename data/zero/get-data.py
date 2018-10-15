#!/usr/bin/python

# https://developers.google.com/drive/api/v3/quickstart/python
'''
Note, the OAuth flow requires opening your browser and logging 
into your Google account so you may not be able to do this from
the CLI.

You will also need an OAuth 2.0 client credentials.json:
https://console.developers.google.com/apis/credentials

(there may be a way to get this sorted with a service account
but I didn't mess with it too much)
'''
# from   __future__ import print_function

import arrow
import csv
from   googleapiclient.discovery import build
from   httplib2 import Http
from   oauth2client import file, client, tools
from   io import StringIO
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('drive', 'v3', http=creds.authorize(Http()))

  # Call the Drive v3 API
  results = service.files().list(
    q='name="zero.csv"', orderBy='createdTime desc', pageSize=1, fields="nextPageToken, files(id, name)").execute()
  items = results.get('files', [])
  print(items)

  '''
  if not items:
    print('No files found.')
  else:
    print('Files:')
    for item in items:
      print(u'{0} ({1})'.format(item['name'], item['id']))
  '''

  try:
    f = service.files().get_media(fileId=items[0]['id'])
    c = f.execute()
  except:
    sys.exit('Could not find zero.csv') 

  # Read CSV
  r = csv.reader(StringIO(c.decode('utf-8')))
  for line in r:
    print(line)

  '''
  Turn Date into Array OrdereDict name
  store hours: fasted, eating, last-eaten time (ideally we'd be able to correlate to sleep time), need to look at hours for end

['8/24/18', '07:39', '00:33', '16', '0']
['8/25/18', '05:40', '23:41', '18', '11']
['8/26/18', '05:06', '06:44', '25', '11']
['8/27/18', '15:34', '12:25', '20', '0']
['8/28/18', '19:40', '13:24', '17', '1']
['8/29/18', '19:55', '15:18', '19', '1']
['8/30/18', '20:55', '17:36', '20', '2']
['8/31/18', '21:00', '14:08', '17', '2']
['9/1/18', '18:37', '12:46', '18', '0']
['9/2/18', '18:50', '11:50', '17', '0']
['9/3/18', '15:55', '09:55', '18', '0']
['9/4/18', '18:04', '10:26', '16', '0']
['9/5/18', '21:30', '13:46', '16', '3']
['9/6/18', '19:30', '13:28', '17', '1']
['9/7/18', '18:50', '13:05', '18', '0']
['9/9/18', '01:10', '12:19', '11', '7']
['9/9/18', '19:52', '13:15', '17', '1']
['9/10/18', '19:38', '11:43', '16', '1']
['9/11/18', '18:00', '11:01', '17', '0']
['9/12/18', '21:35', '19:00', '21', '3']
['9/13/18', '21:55', '13:20', '15', '3']
['9/14/18', '20:31', '09:03', '12', '2']
['9/15/18', '19:42', '10:01', '14', '1']
['9/16/18', '22:10', '15:06', '16', '4']
['9/17/18', '18:42', '16:01', '21', '0']
['9/18/18', '20:29', '13:53', '17', '2']
['9/19/18', '15:47', '04:05', '12', '0']
['9/20/18', '17:46', '10:47', '17', '0']
['9/21/18', '15:40', '08:25', '16', '0']
['9/22/18', '22:03', '13:12', '15', '4']
['9/23/18', '21:00', '10:47', '13', '3']
['9/24/18', '19:15', '18:32', '23', '1']
['9/25/18', '19:29', '12:06', '16', '1']
['9/26/18', '18:29', '12:05', '17', '0']
['9/27/18', '20:50', '13:09', '16', '2']
['9/28/18', '21:02', '14:14', '17', '3']
['9/29/18', '21:30', '15:06', '17', '3']
['9/30/18', '20:45', '11:47', '15', '2']
['10/1/18', '22:00', '11:10', '13', '4']
['10/2/18', '18:57', '14:39', '19', '1']
['10/3/18', '18:40', '10:40', '16', '0']
['10/4/18', '18:00', '13:04', '19', '0']
['10/5/18', '18:47', '19:00', '24', '0']
['10/6/18', '20:00', '15:12', '19', '2']
['10/7/18', '19:42', '16:11', '20', '1']
['10/8/18', '18:37', '11:39', '17', '0']
['10/9/18', '18:56', '11:20', '40', '1']
['10/11/18', '17:37', '15:17', '21', '0']
  '''

  

  



if __name__ == '__main__':
  main()
