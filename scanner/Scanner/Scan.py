from . import DockerUtil
from . import DockerImage
from . import Mount

SCANNERMAPS={"Ubuntu" : "ubuntu.openscap"}

class Scan():

	def __init__(self, imageName):
		self.imageName = imageName
		self.scanCommands=['']
		self.objImage = DockerImage.DockerImage(imageName)
		self.objDocker = DockerUtil.DockerUtil()
		print self.objImage
		self.mountImage()
		self.getOS()

	def mountImage(self):
		self.mountObj = Mount.Mount(self.objImage)
		print self.mountObj.mountCommand
		self.mountObj.performMount()

	def getOS(self):
		if os.path.exists("%s/etc/lsb_release" %self.mountObj.mountPoint):
			with open("%s/etc/lsb_release" %self.mountObj.mountPoint) as fh:
				if( "DISTRIB_ID=Ubuntu" in fh.read()):
					self.dist = "Ubuntu"
	#self, image, command, volumes)

	def performScan(self):
		self.objDocker.runContainer(SCANNERMAPS[self.dist])

	#def getImageInspect(self):
		#elf.imageInspection = self.docker.inspectImage(self.imageObj[)
