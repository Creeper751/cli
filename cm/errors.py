class ConfigEmptyException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(message)


class ConfigParseException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(message)


class ConfigMissingException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(message)
