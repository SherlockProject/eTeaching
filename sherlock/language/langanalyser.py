from sherlock.alchemy.alchemyapi import AlchemyAPI

class LangAnalyser:

    def __init__(self):
        self.alchemyapi = AlchemyAPI()
        self.rel_opt = {'sentiment': 0, 'keywords': 0, 'entities': 1}
        self.key_opt = {'sentiment': 0}

    def analyse(self, text):
        # get Alchemy Results
        alchRelations = self.alchemyapi.relations('text', text, self.rel_opt)
        alchKeywords = self.alchemyapi.keywords('text', text, self.key_opt)
        rel = alchRelations['relations']
        key = alchKeywords['keywords'].values().sort(key = lambda x: x[0], reverse = True)

        # remove Relations without Keywords!
        for x, keyword in key:
            # check if kewword object or subject in relations, if not
            #                           remove from relations
            # PROBELM: the jsons become very ugly to handle, depth and keys
            #          are not well defined! 
            pass

        res = {}
        res['relations'] = rel
        res['keywords'] = key

        return res

    def testAlchemyLanguage(self, text):

        result = {}
        result['original_text'] = text

        result['entities'] = self.alchemyapi.entities('text', text, {'senitment': 1})
        result['keywords'] = self.alchemyapi.keywords('text', text, {'sentiment': 1})
        result['concepts'] = self.alchemyapi.keywords('text', text)
        result['sentiment'] = self.alchemyapi.sentiment('text', text)
        result['targeted_sentiment'] = self.alchemyapi.sentiment_targeted('text', text, 'Relational')
        result['language_detection'] = self.alchemyapi.language('text', text)

        rel_options = {'sentiment': 1, 'keywords': 1, 'entities': 1}
        result['relations'] = self.alchemyapi.relations('text', text, rel_options)
        result['category'] = self.alchemyapi.category('text', text)

        return result
