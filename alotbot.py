#!/usr/bin/python
# alotbot.py
# author: Nancy (github: C-xC-q)

import redditbot

class AlotBot(redditbot.RedditBot):
    def __init__(self):
        self.username = 'likethisalot'
        self.password = 'alotbotpassword'
        self.useragent =  'alotbot/1.0 (thealotbot@gmail.com)'
        botinfo = [self.username, self.password, self.useragent]
        botoptions = {}
        botoptions['subreddits'] = ['all']
        botoptions['wantcomments'] = True
        botoptions['wantposts'] = False
        redditbot.RedditBot.__init__(self, *botinfo, **botoptions)
     

if __name__ == '__main__':
    alotbot = AlotBot()
    alotbot.roamposts()
