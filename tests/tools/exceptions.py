class DataError(Exception):
	def __init__(self, msg):
		if not msg:
			print("Could not find specified value in test data provided.")
		else:
			print(msg)