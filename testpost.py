import urllib2
import urllib
import cookielib
import json

cookiename = ('reddit%scookie_test.lwp' % 'likethisalot')


def getresponse(request, opener, cj):
    cj.add_cookie_header(request)
    try:
        response = opener.open(request)
        #print response.read()
        print "Success?"
        return response
    except urllib2.HTTPError as e:
        print 'getresponse: Error code: %d. Retrying...' % e.code
        print e.read()

def login(cj, opener):
    data = {}
    data['user'] = 'likethisalot'
    data['passwd'] = 'alotbotpassword'
    data['api_type'] = 'json'
    url = ('%s/%s' % ("https://www.reddit.com/api/login", data['user']))
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(url, encoded_data, { 'User-Agent' : 'Default user agent' })
    response = getresponse(request, opener, cj)
    
    js = json.loads(response.read())
    
    try:
        modhash = js['json']['data']['modhash']
        cookie = js['json']['data']['cookie']
        print modhash
        print cookie
    except KeyError:
        print "Key error"
    
    print "Logged in!"
    #cj.set_cookie(cookie)
    #cj.save(cookiename)
    return (modhash, response)

if __name__ == '__main__':
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    (modhash, login_response) = login(cj, opener)
    

    print modhash
    data = "text=%3E+alot+of+butthurt%0A%0Ahttp%3A%2F%2Fi.imgur.com%2FCa6KdaD.png%0A&thing_id=t1_cupastk&api_type=json"
    data += "&uh="
    data += modhash
    print data

    
    request = urllib2.Request("https://www.reddit.com/api/comment", data, { 'User-Agent' : 'Default user agent' })
    #cj.extract_cookies(login_response, request)
    #cj.save(cookiename)
    #cj.add_cookie_header(request)
    
    response = getresponse(request, opener, cj)
    print response.read()


