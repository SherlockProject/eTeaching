# base program: MANAGER

from vision.see import See
from language.hear import Hear
import response.response

class Sherlock:

    # DUMMY
    def __init__(self, string):
        noSessions = 0
        activeSession = False
        self.name = string

    def startSession(self):
        noInteraction = 0
        sessionID = noSession + 1
        activeSession = True

    def endSession(self):
        activeSession = False

    def process(self, input):
        if not activeSession:
            startSession()
            response['text'] = proc_UserInp('',noInteraction)
            response['imagePATH'] = 'a140032.jpg'

            return response
        else:
            noInteraction += 1
            reponse['text'] = proc_UserImp(input, noInteraction)

            return response

    def visionTags(self, imagePath):
        tags = see.getTags(imagePath)
        return tags
