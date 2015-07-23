# base program: MANAGER

from vision import see

class Sherlock:

    # DUMMY
    def __init__(self, string):
        self.name = string;

    def visionTags(imagePath):
        tags = see.getTags(imagePath)
        return tags
