The Alot: http://hyperboleandahalf.blogspot.ca/2010/04/alot-is-better-than-you-at-everything.html

The Alot Bot
===============
- User: http://www.reddit.com/user/likethisalot
- Operation:
  1. Finds comments containing "alot of [noun-phrase]"
  2. Gets an image of [noun-phrase] from google image search 
  3. Draws an alot of using that image and a pre-drawn cookiecutter alot
  4. Uploads the created image to imgur and posts the link in a reply
- The mythical alot creature was created by HyperboleAndAHalf.blogspot.ca
- Compatible with Python 3

Libraries Used
===============
- PRAW: http://praw.readthedocs.org
- Google Search: https://github.com/BirdAPI/Google-Search-API
  (I've had to modify this to get it to work with the new google image search; planning to commit back to the original repo after clean up)
- Python Image Library: http://www.pythonware.com/products/pil/
- ImgurAPI
- NLTK, stanford parser

