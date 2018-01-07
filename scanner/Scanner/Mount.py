from . import DockerUtil
from subprocess import call
import os

class Mount():
	def __init__(self, image, mountpoint=""):
		self.image=image
		if mountpoint == "":
			self.mountpoint="/mnt/%s" %self.image.imageID.split(":")[1]
		else:
			self.mountpoint = "/mnt/imagerootfs"
		if image.storageType == "overlay" or image.storageType == "overlay2":
			self.parseOverlay()
			self.buildOverlay()
                #self.storageType = self.imageInspect['GraphData']['Name']
                #self.storageData = self.imageInspect['GraphData']['Data']

	def parseOverlay(self):
		self.lowerdir = self.image.storageData['LowerDir']
		self.upperdir = self.image.storageData['UpperDir']
		self.workdir = self.image.storageData['WorkDir']

	def buildOverlay(self):
		self.mountCommand = ["/bin/mount","-t","overlay","overlay","-r","-o","lowerdir=%s,upperdir=%s,workdir=%s" % (self.lowerdir, self.upperdir, self.workdir), self.mountpoint]

	def performMount(self):
		if not os.path.exists(self.mountpoint):
			print "Creating patch"
			os.mkdir(self.mountpoint)
		call(self.mountCommand)
