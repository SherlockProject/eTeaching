from sherlock.alchemy.alchemyapi import AlchemyAPI

class LangAnalyser:

    def __init__(self):
        self.alchemyapi = AlchemyAPI()

    def analyse(self, text):


        # currently, no analysis
        return text

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
