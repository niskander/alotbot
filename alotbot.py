#!/usr/bin/python
# alotbot.py

import time
import praw
import os
import sys

import drawalot
import alotofbrain

__author__ = 'Nancy Iskander; nancy.iskander@mail.utoronto.ca'

ALOTURL = 'http://hyperboleandahalf.blogspot.ca/2010/04/alot-is-better-than-you-at-everything.html'
ALOTBOTURL = 'https://github.com/niskander/redditbot'

class AlotBot:
    def __init__(self):
        self.already_responded = []
        self.drawalot = drawalot.DrawAlot(humanaid=True)
        self.signature = "\n\n [ALOT](%s), [AlOTBOT](%s)\n" % (ALOTURL, ALOTBOTURL)
        self.brain = alotofbrain.AlotOfBrain()
        
    def wanttext(self, text):
        accepted_things = []
        if 'alot of' in text.lower():
            print('Selected text' + text)
            things = self.brain.alotofwhat(text)
            for thing in things:
                print("Thing: " + thing)
                os.system('say "Alotbot needs input"')
                p = input("Accept? ('y'/'n'/'i') ")
                if p == 'i':
                    accepted_things.append(input("Input thing: "))
                elif p == 'y':
                    accepted_things.append(thing)
        if len(accepted_things) > 0:
            urls = self.geturls(accepted_things)
            return list(zip(accepted_things, urls))
        return []

    def geturls(self, things):
        urls = []
        for thing in things:
            urls.append(self.drawalot.drawandupload(thing))
        return urls
