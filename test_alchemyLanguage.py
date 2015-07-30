import os
import json
from sherlock.language.langanalyser import LangAnalyser

analyser = LangAnalyser()
counter = 1
print(os.getcwd())

for filename in os.listdir('data/imageDescriptions'):
    f = open('data/imageDescriptions/' + filename, 'r')
    text = f.read()

    analysis = analyser.testAlchemyLanguage(text)
    writeTo = 'data/benchmarkResults/descript_' + str(counter) + '.json'

    with open(writeTo, 'w') as resFile:
        json.dump(analysis, resFile)

    counter += 1
    if counter > 50: break
