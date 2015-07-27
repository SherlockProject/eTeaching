
class Answer:

	def rndmReply(self,sentence, num_interaction):
		if num_interaction == 0:
			return "Hello, I'm Sherlock, who are you?"
		elif num_interaction == 1:
			return "What does the picture in the left show?"
		elif num_interaction > 2:
			rand = random.randint(1, 3)
			if rand == 1:
				return "Could you try to be more specific?"
			elif rand == 2:
				return "Could you try to be more general?"
			elif rand == 3: # If answer does not contain annotation
				return "Can you also see (tag 1)?"
