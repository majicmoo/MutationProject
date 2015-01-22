GITHUB_API = 'https://api.github.com'

from requests import *
import urllib2
from urllib2 import *
import json
from StringIO import *
from project import Project
from runMutationTools import RunMutationTools
import time
from retrying import retry
import requests
import getpass
from urlparse import urljoin

class Authenticate:
    def __init__(self):
        pass

    def doAuthenticate(self):
        username = raw_input('Github username: ')
        #print username
        password = getpass.getpass("Github password: ")
        note = raw_input('Note (optional): ')
        url = urljoin(GITHUB_API, 'user')
        #print url
        payload = {}
        if note:
            payload['note']=note
        res = requests.post(url, auth = (username, password), data=json.dumps(payload))
        #print res
        #print res.text
        #print res.status_code
        j = json.loads(res.text)
        if res.status_code >= 400:
            msg = j.get('message', ' UNDEFINED ERROR (no error description from server)')
            print 'ERROR: %s' % msg
            return
        return(username,password)