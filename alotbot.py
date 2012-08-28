#!/usr/bin/python
# alotbot.py
# author: Nancy (github: C-xC-q)

import redditbot
from redditthings import RedditComment

class AlotBot(redditbot.RedditBot):
    def __init__(self):
        self.username = 'likethisalot'
        self.password = 'alotbotpassword'
        self.useragent =  'Mozilla/5.0 alotbot/1.0 (thealotbot@gmail.com)'
        botinfo = [self.username, self.password, self.useragent]
        botoptions = {}
        botoptions['subredditlist'] = ['all']
        botoptions['wantcomments'] = True
        botoptions['wantposts'] = False
        redditbot.RedditBot.__init__(self, *botinfo, **botoptions)
        self.selectorstrs = [ 'alot', 'would of', 'should of', 'could of' ]
        self.toquote = []
        self.alotofurls = {}
        self.alotofurls['alot more'] = 'http://i.imgur.com/v4RZN.png'
        

    def wantcomment(self, comment):
        if comment.name in self.replyhistory_str: return False
        returnvalue = False
        for selectorstr in self.selectorstrs:
            if selectorstr in comment.body:
                print 'selecting comment: %s' % comment.body
                self.toquote.append(selectorstr)
                returnvalue = True
                print comment.name
                # print 'history: %s' % self.replyhistory_str
        return returnvalue

    def composereply(self, thing):
        if isinstance(thing, RedditComment): text = thing.body
        else: text = thing.text
        l = []
        for q in self.toquote:
            l.append('> %s\n\n' % q)
            if q == 'alot':
                l.append('%s\n' % self.alotofurls['alot more'])
            elif q == 'would of':
                l.append('would\'ve')
            elif q == 'should of':
                l.append('would\'ve')
            elif q == 'could of':
                l.append('could\'ve')
        reply = ''.join(l)
        print 'reply: %s' % reply
        return reply

if __name__ == '__main__':
    alotbot = AlotBot()
    alotbot.roamposts()
