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
        relL = alchRelations['relations']
        keyW = [( d['relevance'], d['text'] ) for d in alchKeywords['keywords']]
        keyW.sort(reverse = True)
        relations = self.__cleanupRelations(relL)


        relations[:] = [itm for itm in relations
                        if True in [x[1].lower() in (itm['obj'].lower() or
                                    itm['sbj'].lower()) for x in keyW]]

        res = {}
        res['relations'] = relations
        res['keywords'] = keyW

        return res

    def __cleanupRelations(self, relList):
        """clean up a dictionary of relations returned by AlchemyAPI.

        Args:
        relDict -- the dictionary of relations from an AlchemyAPI analysis.

        Returns:
        resDict -- cleaned up and determined structure containing the same
                   information contained in relDict; strucutre:
                   LIST:
                              'sbj'
                              'veb'
                              'obj'
                              'tns'
        """

        #TODO: objects come in different forms, with different keys. fuck that.

        clean_rels = []
        idx = 0
        for rel in relList:
            # small intermediate step for different object keys:
            object_L = [x for x in rel.keys() if not (x == 'subject' or
                                                      x == 'action' or
                                                      x == 'sentence')]
            object = object_L[0]
            clean_rels.append({})
            clean_rels[idx]['sbj'] = rel['subject']['text']
            clean_rels[idx]['vrb'] = rel['action']['lemmatized']
            clean_rels[idx]['obj'] = rel[object]['text']
            clean_rels[idx]['tns'] = rel['action']['verb']['tense']
            idx += 1

        return clean_rels




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
