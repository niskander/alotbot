#!/usr/bin/python
# prawbot.py

import time
import praw
import drawalot
import os

__author__ = 'Nancy Iskander; nancy.iskander@mail.utoronto.ca'

REDDITACCOUNT = 'alotbot/redditaccount.txt'
ALOTURL = 'http://hyperboleandahalf.blogspot.ca/2010/04/alot-is-better-than-you-at-everything.html'
ALOTBOTURL = 'https://github.com/niskander/redditbot'

class PrawAlotBot:
    def __init__(self):
        lines = open(REDDITACCOUNT).read().splitlines()
        self.username = lines[0]
        self.password = lines[1]
        self.useragent = lines[2]
        self.r = praw.Reddit(user_agent = self.useragent)
        self.r.login(self.username, self.password)
        self.already_responded = []
        self.drawalot = drawalot.DrawAlot(humanaid=True)
        self.signature = "\n\n [ALOT](%s), [AlOTBOT](%s)\n" % (ALOTURL, ALOTBOTURL)

    def wantcomment(self, comment):
        if comment.id in self.already_responded: return False
        if comment.author.name == self.username: return False

        if 'alot' in comment.body.lower():
            print "Selected comment:"
            print comment.body
            os.system('say "Alotbot needs input"')
            p = raw_input("Proceed? ('y'/'n') ")
            if p == 'y': 
                return True

        print "Skipping comment..."
        return False
    
    def loop(self):
        while True:
            '''
            subreddit = r.get_subreddit("askreddit")
            for submission in subreddit.get_hot(limit=10):
                forest_comments = submission.comments
                flat_comments = praw.helpers.flatten_tree(forest_comments)
                for comment in flat_comments:
                    if self.wantcomment(comment):
                        # do something
                        print "Found comment!"
            '''
            # Get all recent comments
            print "In loop!"

            all_comments = self.r.get_comments('all', limit=100)
            for comment in all_comments:
                if self.wantcomment(comment):
                    text = self.composereply(comment)
                    comment.reply(text)
                    print "Reply posted!"
                    self.already_responded.append(comment.id)

            print "Will sleep for a bit. Time = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            time.sleep(30)

    def composereply(self, comment):
        thingafter = raw_input('Thingafter? (Enter the name of the thing) ')
        url = self.drawalot.drawandupload(thingafter)
        text = "> alot of %s\n\n %s" % (thingafter, url)
        return text
    

if __name__ == "__main__":
    alotbot = PrawAlotBot()
    alotbot.loop()
