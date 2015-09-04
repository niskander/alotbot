#!/usr/bin/python
# prawbot.py

import time
import praw
import drawalot
import os
import sys

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
        if not hasattr(comment, "body"): return False
        if comment.id in self.already_responded: return False
        if hasattr(comment, "author") and hasattr(comment.author, "name") and comment.author.name == self.username: return False

        index = comment.body.lower().find('alot of')
        
        if index != -1:
            print "Selected comment:"
            print comment.body[max(index-50,0):max(index+50,len(comment.body))]
            
            os.system('say "Alotbot needs input"')
            p = raw_input("Proceed? ('y'/'n') ")
            if p == 'y': 
                return True

        print "Skipping comment..."
        return False

    def processcomment(self, comment):
        if self.wantcomment(comment):
            text = self.composereply(comment)
            comment.reply(text)
            comment.upvote()
            print "Reply posted!"
            self.already_responded.append(comment.id)
    
    def recentloop(self):
        while True:
            # Get all recent comments
            print "In recent comments loop!"

            all_comments = self.r.get_comments('all', limit=100)
            for comment in all_comments:
               self.processcomment(comment) 

            print "Will sleep for a bit. Time = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            time.sleep(3)

    def hotloop(self):
        while True:
            # Get all hot threads
            print "In hot comments loop!"

            subreddit = self.r.get_subreddit("all")
            for submission in subreddit.get_hot(limit=100):
                forest_comments = submission.comments
                flat_comments = praw.helpers.flatten_tree(forest_comments)
                for comment in flat_comments:
                    self.processcomment(comment)

            print "Will sleep for a bit. Time = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            time.sleep(300)

    def composereply(self, comment):
        thingafter = raw_input('Thingafter? (Enter the name of the thing) ')
        url = self.drawalot.drawandupload(thingafter)
        text = "> alot of %s\n\n %s" % (thingafter, url)
        return text
    
def usage():
    print "Usage: python prawbot.py [-r|--recent|-h|--hot]"
    print "\t-r|--recent: Looks at all recent comments"
    print "\t-h|--hot   : Looks at comments in all hot threads"
    sys.exit(0)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        usage()

    recent = True # default is recent
    if len(args) == 2:
        arg = args[1]
        if arg == "-r" or arg == "--recent":
            recent = True
        elif arg == "-h" or arg == "--hot":
            recent = False
        else:
            usage()
            
    alotbot = PrawAlotBot()
    if recent:
        alotbot.recentloop()
    else: 
        alotbot.hotloop()
    
