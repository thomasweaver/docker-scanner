import docker

class DockerUtil():
	def __init__(self):
		self.client = docker.from_env()
		self.advClient = docker.APIClient()

	def getImages(self, image=""):
		if image is "":
			images = self.advClient.images()
		else:
			try:
				images = self.client.images.get(image)
			except docker.errors.ImageNotFound as e:
				return ""
		return images
	def inspectImage(self, image):
		imageInspect = self.advClient.inspect_image(image)
		return imageInspect

	def runContainer(self, image, command, volumes):
		try:
			container = self.client.containers.run(image, command, auto_remove=True, volumes=volumes, detach=True)
		except docker.errors.ImageNotFound as e:
			raise Exception("Image not found")

		return container
