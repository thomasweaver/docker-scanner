from . import DockerUtil
import json

class DockerImage():
	def __init__(self, imageName):
                self.imageName = imageName
                self.docker = DockerUtil.DockerUtil()
                self.imageObj = self.docker.getImages(self.imageName)
                self.imageID = self.imageObj.id
                self.imageInspect = self.docker.inspectImage(self.imageID)
		self.parseInspection()

	def parseInspection(self):
		print json.dumps(self.imageInspect)
		self.storageType = self.imageInspect['GraphDriver']['Name']
		self.storageData = self.imageInspect['GraphDriver']['Data']
