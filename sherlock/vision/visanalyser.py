# base class for Computer Vision.
# for now, this means returning a simple .json with best alchemy API results.
# first Version: DUMMY

from sherlock.alchemy.alchemyapi import AlchemyAPI

class VisAnalyser:

    def __init__(self):
        self.alchemyapi = AlchemyAPI()
        self.opt = {'forceShowAll': 0, 'knowledgeGraph': 0}

    def process(self, imgPATH):
         temp = self.__getAlchemyTags(imgPATH)
         res = temp['imageKeywords'].values().sort(key = lambda tup: tup[0], reverse = True)

         return res

    def __getAlchemyTags(self, imagePATH):
        res = self.alchemyapi.imageTagging('image',imagePATH, self.opt)

        return res
