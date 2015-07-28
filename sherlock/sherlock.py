# base program: MANAGER

from sherlock.vision.visanalyser import VisAnalyser
from sherlock.language.langanalyser import LangAnalyser
from sherlock.response.dialoguehandler import DialogueHandler

class Sherlock:

    # Initialise clean Instance.
    def __init__(self, string):
        self.noSessions = 0
        self.activeSession = False
        self.currImage = ''

        # Bind and instantiate all analysers
        self.Vision = VisAnalyser()
        self.Language = LangAnalyser()
        self.Dialoge = DialogueHandler()

    # public access to processing in the sherlock project!
    # will return a dict with return type, message and possibly
    # the path to an image. See specification of Frontend-Backend
    # communication.
    def process(self, request):

        if request['type'] == 'start'
            respMsg = self.__startSession()
            response = {'type': 'image',
                        'img_path': self.currImage,
                        'text': respMsg}
            return response

        elif request['type'] == 'message'
            if self.activeSession = False:
                return response = {'type': 'message',
                                   'text': 'ERROR: No active Session'}
            # gather all analytics in one object.
            analysis = self.__analyse(request['text'], self.currImage)

            # based on the analysis, compute response and return.
            return self.__respond(analysis)

        else
            response = {'type': 'message',
                        'text': 'ERROR: Unknown Request Type'}

    # Analyse a std message and store information!
    # 1st Iteration - SIMPLE
    # private.
    def __analyse(self, text, imagePATH):
        # get list of image tags
        tagList = self.Vision.getTags(imagePATH)

        # get Relations, Trees, ..
        lingAnalysis = self.Language.analyse(text)

        # combine, clean up
        pass

        # store
        pass

        analysis = {'tags': tagList,
                    'linguistics': lingAnalysis}
        # return
        return analysis


    # Computes response based on analysis.
    # Will return a comlete response dict.
    # private.
    def __respond(self, analysis):

        resonse = self.Dialogue.respond(analysis)
        # housekeeping: new Image? compose proper response dict etc...
        pass
        return response

    # Start a session:
    # Reset Interactions; Set SessionID;
    # Flag active Session; Get 'Hello' Message
    # private.
    def __startSession(self):
        self.noInteraction = 0
        self.sessionID = self.noSessions + 1
        self.activeSession = True

        # Set first Image;
        self.currImage = 'a140032.jpg'
        return 'Hello, I am Sherlock! Please describe the picture on the left!'

    # End a session:
    # Reset flags!
    # private.
    def __endSession(self):
        self.currImage =  ''
        self.activeSession = False
