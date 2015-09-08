#!/usr/bin/python
# alotofbrain.py

import nltk
import os
from nltk.parse import stanford

__author__ = 'Nancy Iskander; nancy.iskander@mail.utoronto.ca'

PARSERPATH = '/Users/nancyiskander/dev/nlp/stanford-parser-full-2015-04-20'
MODELPATH = PARSERPATH + '/englishPCFG.ser.gz'


class AlotOfBrain:
    def __init__(self):
        os.environ['STANFORD_PARSER'] = PARSERPATH
        os.environ['STANFORD_MODELS'] = PARSERPATH
        self.parser = stanford.StanfordParser(model_path=MODELPATH, encoding='utf8')

    def alotofwhat(self, text):
        # TODO: Make exception for "alot of alot/alots"?
        sentences = nltk.sent_tokenize(text.lower())
        tokenized_sents = [nltk.word_tokenize(sent) for sent in sentences]
        # We only care about sentences that have 'alot', and we filter
        # after tokenization in order not to mistake words like 'zealot'
        # for alots
        filtered_sents = []
        for i in range(len(tokenized_sents)):
            if 'alot' in tokenized_sents[i]:
                # Get sentences that have 'alot of'
                index = tokenized_sents[i].index('alot')
                if index != -1 \
                and len(tokenized_sents[i]) > index+1 \
                and tokenized_sents[i][index+1] == 'of':
                    filtered_sents.append(' '.join(tokenized_sents[i][index+2:]))
        parsed_sents = self.parser.raw_parse_sents(filtered_sents)
        # All parsed sents start with:
        # (ROOT
        #   (S
        #     (NP
        #       (NP (NN alot))
        #       (PP (IN of) (NP ... )))
        # Actually, they start after 'alot of', so we need to find
        # the first and shallowest (closest to the leafs) NP
        things = []
        for line in parsed_sents:
            for tree in line:
                if tree.height() < 2: continue
                firstNP = tree[0][0]
                things.append(' '.join(firstNP.leaves()))
        print(things)
        return things
        
if __name__ == "__main__":
    alotofbrain = AlotOfBrain()
    text = raw_input("Enter text: ")
    alotofbrain.alotofwhat(text)
