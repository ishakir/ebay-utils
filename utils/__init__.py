def prompt_warning(message):
	text = raw_input("{}. Are you sure you wish to continue? (y/n)".format(message))
	if text != "y":
		raise ValueError("User declined to continue the program")