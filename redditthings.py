# redditthings.py
# author: Nancy (github: C-xC-q)

"""Wrapper for some reddit objects (posts and comments), and an iterator
for posts.
"""

import json
import requesthandler
from customexceptions import *

REDDITURL = 'http://reddit.com'

class RedditThing(object):
    """Extracts/Stores attributes common to posts/comments from the
    json returned by reddit.
    """
    def __init__(self, data_js):
        self.author = data_js['author'] # username
        self.name = data_js['name'] # kind_id
        self.created = data_js['created']
        self.created_utc = data_js['created_utc']
        self.subreddit_id = data_js['subreddit_id']
        self.subreddit = data_js['subreddit']
        self.edited = data_js['edited'] # 'true' or 'false'
        self.id = data_js['id']
        self.downs = data_js['downs']
        self.ups = data_js['ups']
        self.approved_by = data_js['approved_by'] # e.g. as in r/iama
        self.num_reports = data_js['num_reports']
        self.js = data_js
        

class RedditPost(RedditThing):
    """Extends RedditThing. Extracts/Stores post attributes from js."""
    def __init__(self, data_js):
        super(RedditPost, self).__init__(data_js)
        # so as to make things maintainable if the json changes
        self.kind = 't3'
        self.domain = data_js['domain']
        self.title = data_js['title']
        self.over_18 = data_js['over_18']
        self.score = data_js['score']
        self.num_comments = data_js['num_comments']
        self.is_self = data_js['is_self'] # 'true' or 'false'
        self.permalink = data_js['permalink']
        self.url = data_js['url']
        self.permalink = data_js['permalink']
        if self.is_self == 'true':
            self.is_self = True
            self.self_text = data_js['self_text']
        else:
            self.is_self = False
            self.self_text = ''


class RedditComment(RedditThing):
    """Extends RedditThing. Extracts/Stores comment attributes from js."""
    def __init__(self, data_js):
        super(RedditComment, self).__init__(data_js)
        self.kind = 't1'
        self.body = data_js['body']
        self.body_html = data_js['body_html']
        self.parent_id = data_js['parent_id']
        self.link_id = data_js['link_id']
        if type(data_js['replies']) is not str:
            try:
                self.replies_js = data_js['replies']['data']['children']
            except TypeError:
                self.replies_js = None
        else:
            self.replies_js = None


class RedditIterator(object):
    """Fetches listings of posts and comments, and iterates over posts.
    (Iterating over posts is, at this point, more invovled than iterating
    over comments (which isn't handled by a separate class) because of page
    flipping. There's currently nothing that retrieves 'more' comments.)
    """
    # subreddits: List of subreddits to search
    def __init__(self, subreddits=None, query=None, blocksize=50):
        if not subreddits: subreddits = ['all']
        self.subredditlist = '+'.join(subreddits)
        # TODO: Make sure subreddit names are valid

        self.query = query
        self.blocksize = blocksize
        self.index = 0
        self.posts_js = None
        self.after = None

    def fetchposts(self):
        """Fetches the first or next listing of posts"""
        url = '%s/r/%s.json?limit=%s' % \
              (REDDITURL, self.subredditlist, str(self.blocksize))

        # TODO: Restrict search by domain (before fetching)
        # Very easy, but I probably won't do it

        # self.after is set whenever posts are fetched; 'flips' the page
        if self.after is not None:
            url = '%s&after=%s' % (url, self.after)
        response = requesthandler.reqhandler.getrequest(url)
        if not response: return []

        js = json.loads(response.read())
        try:
            self.posts_js = js['data']['children']
        except KeyError:
            raise FailedFetch('posts', response.getcode(), js)
            return
        self.after = js['data']['after']
        
    def nextpost(self):
        if self.posts_js is None or self.index >= len(self.posts_js):
            self.fetchposts()
            self.index = 0
        post = RedditPost(self.posts_js[self.index]['data'])
        self.index += 1
        return post

    def fetchcomments(self, post):
        """Returns the comments page of the post as js"""
        url = '%s%s.json' % (REDDITURL, post.permalink)
        response = requesthandler.reqhandler.getrequest(url)
        if not response: return []

        js = json.loads(response.read())
        try:
            comments_js = js[1]['data']['children']
        except KeyError:
            raise FailedFetch('comments', response.getcode(), js)
            return
        return comments_js
        
