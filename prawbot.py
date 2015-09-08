#!/usr/bin/python
# prawbot.py

"""
Main module for running the reddit bot. Goes through recent or hot thread
comments and calls on AlotBot to process/respond to them
"""

import time
import praw
import os
import sys

import alotbot

__author__ = 'Nancy Iskander; nancy.iskander@mail.utoronto.ca'

REDDITACCOUNT = 'alotbot/redditaccount.txt'

class PrawAlotBot:
    def __init__(self):
        lines = open(REDDITACCOUNT).read().splitlines()
        self.username = lines[0]
        self.password = lines[1]
        self.useragent = lines[2]
        self.r = praw.Reddit(user_agent = self.useragent)
        self.r.login(self.username, self.password)
        self.already_responded = []
        self.alotbot = alotbot.AlotBot()

    def wantcomment(self, comment):
        if not hasattr(comment, "body"): return False
        if comment.id in self.already_responded: return False
        if hasattr(comment, "author") and hasattr(comment.author, "name") and comment.author.name == self.username: return False

        self.things = self.alotbot.wanttext(comment.body)
        if len(self.things) == 0:
            print("Skipping comment...")
            return False
        return True

    def processcomment(self, comment):
        if self.wantcomment(comment):
            text = self.composereply(comment)
            comment.reply(text)
            comment.upvote()
            print("Reply posted!")
            self.already_responded.append(comment.id)
    
    def recentloop(self):
        while True:
            # Get all recent comments
            print("In recent comments loop!")

            all_comments = self.r.get_comments('all', limit=100)
            for comment in all_comments:
               self.processcomment(comment) 

            print("Will sleep for a bit. Time = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            time.sleep(3)

    def hotloop(self):
        while True:
            # Get all hot threads
            print("In hot comments loop!")

            subreddit = self.r.get_subreddit("all")
            for submission in subreddit.get_hot(limit=100):
                forest_comments = submission.comments
                flat_comments = praw.helpers.flatten_tree(forest_comments)
                for comment in flat_comments:
                    self.processcomment(comment)

            print("Will sleep for a bit. Time = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            time.sleep(300)

    def composereply(self, comment):
        #thingafter = raw_input('Thingafter? (Enter the name of the thing) ')
        #url = self.drawalot.drawandupload(thingafter)
        text = ""
        for (thing,url) in self.things:
            text += "> alot of %s\n\n %s\n\n" % (thing, url)
        return text
    
def usage():
    print("Usage: python prawbot.py [-r|--recent|-h|--hot]")
    print("\t-r|--recent: Looks at all recent comments")
    print("\t-h|--hot   : Looks at comments in all hot threads")
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
    
