import subprocess
import re

class Command():
	def __init__(self, command, regex="", returnCode=0):
		self.command = command
		self.returnCode=returnCode
		self.actualReturnCode = returnCode
		self.regex = regex

	def runCommand(self):
		try:
			self.output = subprocess.check_output(self.command)
			print "Output: %s" %self.output
		except subprocess.CalledProcessError as e:
			if e.returncode != self.returnCode:
				self.actualReturnCode = e.returncode
				self.output = e.output
				print "Output: %s" %self.output
				#raise Exception({'output': self.output, 'returncode': e.returncode})

	def parseOutput(self):
		#print self.format['split']
		self.arrOutput = re.split(r'\n', self.output)
		self.arrParsed= []
		p = re.compile(self.regex)
		regexIndex = p.groupindex
		self.parsedOutput=""
		for line in self.arrOutput:
			m = p.match(line)
			if m:
				print m.groups()
				objLine = {}
				count=1
				for element in m.groups():
					for i in regexIndex:
						if regexIndex[i] == count:
							name = i
							break
					objLine[name] = element
					count=count+1
				self.arrParsed.append(objLine)
				print objLine
			else:
				print "%s DIDNT MATCH REGEX" % line
		#print self.arrParsed
		#print re.split(self.format['split'], self.output)
