import inspect
import logging

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

class Log():
	def __init__(self, level):
		self.level = level

	def setLevel(self, level):
		self.level = level

	def getLevel(self):
		return self.level

	def msg(self, level, text):
		if level < self.level:
			return False

		stack = inspect.stack()
		frame = stack[2][0]

		if 'self' in frame.f_locals:
			clazz = frame.f_locals['self'].__class__.__name__
		else:
			clazz = None

		if level == DEBUG:
			levelStr = 'DEBUG'
		elif level == INFO:
			levelStr = 'INFO'
		elif level == WARNING:
			levelStr = 'WARNING'
		elif level == ERROR:
			levelStr = 'ERROR'
		elif level == CRITICAL:
			levelStr = 'CRITICAL'
		else:
			levelStr = 'UNKNOWN LEVEL'

		method = frame.f_code.co_name

		id = f"{clazz}.{method}()"

		print(f"[{levelStr}]:{id}: {text}")

		return True

log = Log(INFO)

def getLogger():
	return log

def msg(level, text):
	log.msg(level, text)
