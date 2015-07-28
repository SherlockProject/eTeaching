from sherlock.sherlock import Sherlock

handler = Sherlock('handler')

print(handler.activeSession)

exCall_1 = {'type': 'start',
            'sound': 'off'}

exCall_2 = {'type': 'message',
            'text': 'Two men facing the camera.  There is a row of buildings in the background and another row of buildings on the right side of the image.  A man behind the two men is walking away from the camera.  A person is walking towards the left of the image.  There is sky above the buidings in the background.  The ground is paved with stones',
            'sound': 'off'}

resp1 = handler.process('')
print(resp1['text'])

resp2 = handler.process('There is a house')
print(resp2['text'])

resp3 = handler.process('There is also a frenchman')
print(resp3['text'])
