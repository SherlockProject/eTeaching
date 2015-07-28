# base class for Computer Vision.
# for now, this means returning a simple .json with best alchemy API results.
# first Version: DUMMY

from sherlock.alchemy.alchemyapi import AlchemyAPI

class VisAnalyser:

    def __init__(self):
        alchemyapi = AlchemyAPI()

    def getTags(self, imagePATH):
        options = {'forceShowAll': '0', 'knowledgeGraph': '0'}
        res = self.alchemyapi.imageTagging('image',imagePATH, options)
        # ... needs cleanUp!
        return res
