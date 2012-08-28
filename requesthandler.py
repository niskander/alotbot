# requesthandler.py
# author: Nancy (github: C-xC-q)

import urllib2
import urllib
import cookielib
import time
from customexceptions import *


class RequestHandler:
    """Handles http requests."""
    def __init__(self):
        # The useragent will later be set to something
        # specified by the bot
        useragent = 'Default user agent'
        self.headers = { 'User-Agent' : useragent }

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.lastapicall = None
        urllib2.install_opener(self.opener)
        # I'm almost positive that I'm not doing this cookie business 
        # as I should
        
    def setuseragent(self, useragent):
        self.headers = { 'User-Agent' : useragent }
    
    def savecookiefile(self, cookiename):
        self.cj.save(cookiename)
        
    def postrequest(self, url, data):
        data_encoded = urllib.urlencode(data)
        print 'encoded data: %s' % str(data_encoded)
        request = urllib2.Request(url, data_encoded, self.headers)
        return self.getresponse(request)

    def getrequest(self, url):
        return self.getresponse(url)

    def wastetime(self):
        """Wastes two seconds if necessary, since reddit limits the
        number of api calls to 30 per minute.
        """
        if self.lastapicall is None: return
        while time.clock() - self.lastapicall < 2: pass

    def getresponse(self, request):
        """Takes a request and returns a response. 10 attempts are made.
        The reddit api seems to return 429 error often. Has something to do
        with the rate limit and/or user-agent. There are related threads on the
        reddit-dev google group and one on StackOverflow (though I haven't
        contributed to any). Usually works after 4 tries.
        """
        self.wastetime()
        attemptsremaining = 10
        while attemptsremaining > 0:
            try:
                response = urllib2.urlopen(request, timeout=60)
                break
            except urllib2.HTTPError as e:
                #print 'Http request failed. Request = %s' % request.str()
                print 'Error code: %d. Retrying...' % e.code
                time.sleep(5)
                attemptsremaining -= 1
        if attemptsremaining == 0:
            raise FailedFetch('nil', 'nil', e.code)
        self.lastapicall = time.clock()
        return response

reqhandler = RequestHandler()
