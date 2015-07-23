# base program: MANAGER

from sherlock.vision.see import See
from sherlock.language.hear import Hear
from sherlock.response.response import proc_userInp

class Sherlock:

    # DUMMY
    def __init__(self, string):
        self.noSessions = 0
        self.activeSession = False
        self.name = string

    def startSession(self):
        self.noInteraction = 0
        self.sessionID = self.noSessions + 1
        self.activeSession = True

    def endSession(self):
        self.activeSession = False

    def process(self, input):
        if not self.activeSession:
            self.startSession()
            response = {}
            response['text'] = proc_userInp('',self.noInteraction)
            response['imagePATH'] = 'a140032.jpg'

            return response
        else:
            self.noInteraction += 1
            response = {}
            response['text'] = proc_userInp(input, self.noInteraction)

            return response

    def visionTags(self, imagePath):
        tags = see.getTags(imagePath)
        return tags
