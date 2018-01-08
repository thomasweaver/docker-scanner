from . import DockerUtil
from . import DockerImage
from . import Mount
import os
import time

SCANNERMAPS={"Ubuntu" : "ubuntu.openscap"}

class Scan():

	def __init__(self, imageName):
		self.imageName = imageName
		self.scanCommands=['']
		self.objImage = DockerImage.DockerImage(imageName)
		self.objDocker = DockerUtil.DockerUtil()
		#print self.objImage
		self.resultsDir = '/mnt/%s-results' % self.objImage.imageID.split(":")[1]
		self.createResultsDir()
		self.mountImage()
		self.getOS()
		self.performScan()

	def mountImage(self):
		self.mountObj = Mount.Mount(self.objImage)
		print self.mountObj.mountCommand
		self.mountObj.performMount()

	def getOS(self):
		if os.path.exists("%s/etc/os-release" %self.mountObj.mountpoint):
			with open("%s/etc/os-release" %self.mountObj.mountpoint) as fh:
				if( "NAME=\"Ubuntu\"" in fh.read()):
					print "IMAGE IS Ubuntu"
					self.dist = "Ubuntu"
	#self, image, command, volumes)
	def createResultsDir(self):
		if not os.path.exists(self.resultsDir):
			os.mkdir(self.resultsDir)

	def performScan(self):
		#{'/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'}, '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}}
		self.volumes = {self.mountObj.mountpoint : {'bind': '/mnt/rootfs', 'mode': 'ro'}, self.resultsDir: {'bind': '/mnt/results', 'mode': 'rw'}}
		self.objContainer = self.objDocker.runContainer(SCANNERMAPS[self.dist], self.volumes)
		print self.objContainer.status
		self.waitContainerChange("exited")
		self.containerLogs = self.objContainer.logs()
		print self.containerLogs
		self.objContainer.remove()
		#print container

	def waitContainerChange(self, status, timeout=60):
		count=0
		while self.objContainer.status != status:
			self.objContainer.reload()
			print self.objContainer.status
			time.sleep(1)
			count = count +1
			if count > timeout:
				self.containerLogs = self.objContainer.logs()
				print "CONTAINER LOGS: %s" % self.containerLogs
				self.objContainer.remove()
				raise Exception("Timeout")

