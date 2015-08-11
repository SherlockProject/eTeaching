from sherlock.alchemy.alchemyapi import AlchemyAPI

class LangAnalyser(object):
    """LangAnalyser wrapps all functionality needed for language analysis.

    __init__ will bind an AlchmeyAPI object to this one and formulate the
    dicionaries conatining AlchmeyAPI options.

    Note:
        Use the analyse function only!

    """

    def __init__(self):
        self._alchemyapi = AlchemyAPI()
        self._rel_opt = {'sentiment': 0, 'keywords': 0, 'entities': 1}
        self._key_opt = {'sentiment': 0}

    def analyse(self, text):
        """analyse short text paragraph; return py dict.

        Args:
        text -- short paragrpah of text in Str format.

        Returns:
        res -- python dictionary with fields:
            ... TODO: define !

        """
        # get Alchemy Results
        alchRelations = self._alchemyapi.relations('text', text, self._rel_opt)
        alchKeywords = self._alchemyapi.keywords('text', text, self._key_opt)
        rel = alchRelations['relations']
        key = alchKeywords['keywords'].values().sort(key = lambda x: x[0], reverse = True)

        # remove Relations without Keywords!
        for x, keyword in key:
            # check if kewword object or subject in relations, if not
            #                           remove from relations
            # PROBELM: the jsons become very ugly to handle, depth and keys
            #          are not well defined!
            # TODO: Complete __cleanupRelations
            pass

        res = {}
        res['relations'] = rel
        res['keywords'] = key

        return res

    def __cleanupRelaions(self, relDict):
        """clean up a dictionary of relations returned by AlchemyAPI.

        Args:
        relDict -- the dictionary of relations from an AlchemyAPI analysis.

        Returns:
        resDict -- cleaned up and determined structure containing the same
                   information contained in relDict; strucutre:
                   .... TODO: define!
        """


    def testAlchemyLanguage(self, text):
        """use all tools AlchmeyAPI provides for text analysis on text.

        Args:
        text -- short text that will get analysed by all AlchemyAPI algorithms.

        Returns:
        result -- dicionary containing AlchmeyAPI result dictionaries in
                  labled keys.
        """

        result = {}
        result['original_text'] = text

        result['entities'] = self._alchemyapi.entities('text', text, {'senitment': 1})
        result['keywords'] = self._alchemyapi.keywords('text', text, {'sentiment': 1})
        result['concepts'] = self._alchemyapi.keywords('text', text)
        result['sentiment'] = self._alchemyapi.sentiment('text', text)
        result['targeted_sentiment'] = self._alchemyapi.sentiment_targeted('text', text, 'Relational')
        result['language_detection'] = self._alchemyapi.language('text', text)

        rel_options = {'sentiment': 1, 'keywords': 1, 'entities': 1}
        result['relations'] = self._alchemyapi.relations('text', text, rel_options)
        result['category'] = self._alchemyapi.category('text', text)

        return result
