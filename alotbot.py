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

ACCEPTEDPATH = 'alotbot/accepted.txt'
REJECTEDPATH = 'alotbot/rejected.txt'
UNDECIDEDPATH = 'alotbot/undecided.txt'

class AlotBot:
    def __init__(self):
        self.already_responded = []
        self.drawalot = drawalot.DrawAlot(humanaid=True)
        self.signature = "\n\n [ALOT](%s), [AlOTBOT](%s)\n" % (ALOTURL, ALOTBOTURL)
        self.brain = alotofbrain.AlotOfBrain()

        self.accepted_file = open(ACCEPTEDPATH, 'r+')
        self.rejected_file = open(REJECTEDPATH, 'r+')
        self.undecided_file = open(UNDECIDEDPATH, 'r+')
        self.accepted = self.accepted_file.read().splitlines()
        self.rejected = self.rejected_file.read().splitlines()
        self.undecided = self.undecided_file.read().splitlines()
        self.humanaid = True

    def writelist(self, list, file):
        list_str = '\n'.join(list)
        file.write(list_str)

    def updatefiles(self):
        self.writelist(self.accepted, self.accepted_file)
        self.writelist(self.rejected, self.rejected_file)
        self.writelist(self.undecided, self.undecided_file)

    def bookkeeping(self, thing):
        if thing in self.accepted:
            return thing
        if thing in self.rejected:
            return None
        if self.humanaid:
            print("Thing: " + thing)
            os.system('say "Alotbot needs input"')
            p = input("Accept? ('y'/'n'/'i') ")
            accepted_thing = None
            if p == 'i':
                accepted_thing = input("Input thing: ")
                self.accepted_file.write(accepted_thing + '\n')
            elif p == 'y':
                accepted_thing = thing
                self.accepted.append(thing)
                self.accepted_file.write(thing + '\n')
            else:
                self.rejected.append(thing)
                self.rejected_file.write(thing + '\n')
            return accepted_thing
        # No humanaid, can't tell
        self.undecided.append(thing)
        self.undecided_file.write(thing + '\n')
        return None
        
    def wanttext(self, text):
        accepted_things = []
        if 'alot of' in text.lower():
            print('Selected text' + text)
            things = self.brain.alotofwhat(text)
            for thing in things:
                accepted_thing = self.bookkeeping(thing)
                if accepted_thing:
                    accepted_things.append(accepted_thing)
                
        if len(accepted_things) > 0:
            urls = self.geturls(accepted_things)
            return list(zip(accepted_things, urls))
        return []

    def geturls(self, things):
        urls = []
        for thing in things:
            urls.append(self.drawalot.drawandupload(thing))
        return urls
