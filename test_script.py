from sherlock.sherlock import Sherlock

handler = Sherlock('handler')

resp1 = handler.process('')
print(resp1['text'])

resp2 = handler.process('There is a house')
print(resp2['text'])

resp3 = handler.process('There is also a frenchman')
print(resp3['text'])
