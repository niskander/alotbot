#!/usr/bin/python
# alotbot.py

__author__ = 'Nancy; C-xC-q (github); n2iskand@uwaterloo.ca'

import redditbot
import drawalot
from redditthings import RedditComment


REDDITACCOUNT = 'alotbot/redditaccount.txt'

class AlotBot(redditbot.RedditBot):
    def __init__(self):
        lines = open(REDDITACCOUNT).read().splitlines()
        self.username = lines[0]
        self.password = lines[1]
        self.useragent = lines[2]
        botinfo = [self.username, self.password, self.useragent]
        botoptions = {}
        botoptions['subredditlist'] = ['all']
        botoptions['wantcomments'] = True
        botoptions['wantposts'] = True
        botoptions['fetchblocksize'] = 500
        botoptions['restart'] = True
        redditbot.RedditBot.__init__(self, *botinfo, **botoptions)
        self.selectorstrs = ['alot of']
        self.toquote = []
        self.alotofurls = {}
        self.alotofurls['alot more'] = 'http://i.imgur.com/v4RZN.png'
        self.drawalot = drawalot.DrawAlot(humanaid=True)
        

    def wantcomment(self, comment):
        if comment.name in self.replyhistory_str: return False
        if comment.author == self.username: return False

        returnvalue = False
        for selectorstr in self.selectorstrs:
            if selectorstr in comment.body.lower():
                print 'selecting comment: %s' % comment.body
                self.toquote.append(selectorstr)
                returnvalue = True
                print comment.name
                # print 'history: %s' % self.replyhistory_str
        if returnvalue:
            print "Selecting this comment: "
            print comment.body
        else:
            print "Skipping comment..."
        return returnvalue

    def composereply(self, thing):
        if isinstance(thing, RedditComment): text = thing.body
        else: text = thing.text
        text = text.encode('ascii', 'ignore')
        l = []
        for q in self.toquote:
            #l.append('> %s\n\n' % q)
            if q == 'alot':
                l.append('%s\n' % self.alotofurls['alot more'])
            elif q == 'alot of':
                words = str.split(text, 'alot of')
                if len(words) > 1: wordsafter = words[1]
                else: wordsafter = words[0]
                thingafter = str.split(wordsafter)[0]
                l.append('> %s %s\n\n' % ('alot of', thingafter))
                print text
                print 'thingafter: %s' % thingafter
                thingafter = raw_input('Thingafter? (Enter the name of the thing)')
                url = self.drawalot.drawandupload(thingafter)
                l.append('%s\n' % url)
        reply = ''.join(l)
        print 'reply: %s' % reply
        c = raw_input('proceed? ')
        if c == 'n': self.skip = True
        else: self.skip = False
        return reply

    def processcomments(self, comments_js):
        s = str(comments_js)
        if 'alot of' in s.lower(): return True
        else: return False

if __name__ == '__main__':
    alotbot = AlotBot()
    alotbot.roamposts()
