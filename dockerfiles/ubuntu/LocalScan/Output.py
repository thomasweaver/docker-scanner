import os
import json

class Output():
	def __init__(self, objCommands, **kwargs):
		self.objCommands = objCommands
		print kwargs
		self.objOutput={}
		self.createOutputObj()
		self.parseKwargs(kwargs)

	def createOutputObj(self):
		self.objOutput = []
		for command in self.objCommands:
			tmpObj={}
			tmpObj['command'] = command.command
			tmpObj['returnCode'] = command.actualReturnCode
			tmpObj['rawOutput'] = command.output
			tmpObj['parsedOutput'] = command.arrParsed
			self.objOutput.append(tmpObj)

	def performOutput(self):
		if self.type == 'file':
			self.writeToFile()

	def writeToFile(self):
		with open(self.file, 'w') as fh:
			fh.write(json.dumps(self.objOutput))

	def parseKwargs(self, kwargs):
		if 'type' in kwargs:
			self.type = kwargs['type']
		else:
			self.type = 'file'

		if self.type == "file":
			if not 'file' in kwargs:
				raise Exception("Using file output you must specify a file to write to")
			self.file = kwargs['file']
		if self.type == 'http':
			if not 'url' in kwargs:
				raise Exception("Using HTTP POST you must specify a url")
			self.url = kwargs['url']

#	def outputToFile(self):
