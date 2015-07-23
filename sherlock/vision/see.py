# base class for Computer Vision.
# for now, this means returning a simple .json with best alchemy API results.
# first Version: DUMMY

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
    import urllib
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode
import json
from sherlock.alchemy.alchemyapi import AlchemyAPI
import requests

class See:

    alchemyapi = AlchemyAPI()


    def getTags(self, imagePATH):
        options = {'forceShowAll': '0', 'knowledgeGraph': '0'}
        res = self.alchemyapi.imageTagging('image',imagePATH, options)
        return res
