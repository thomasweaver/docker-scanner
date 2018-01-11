#import argparse
import sys
import json
from Scanner import Mount
from Scanner import DockerUtil
from Scanner import DockerImage
from Scanner import Scan


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "You must provide a command"
		sys.exit(1)
	else:
		command = sys.argv[1].lower()

	if command == "scan":
		if len(sys.argv) < 3:
			print "You must provide an image name"
			sys.exit(1)

		imageName = sys.argv[2]

		scanner = Scan.Scan(imageName)
		#docker = DockerUtil.DockerUtil()
		#images = docker.getImages()
		#print images[0]['attrs']
		#inspection = docker.inspectImage(images[0]['Id'])
		#print inspection
		#print json.dumps(inspection)
		#print ""
		#print "FS type is: %s" %inspection['GraphDriver']['Name']
		#print "LAYERS are: %s" %inspection['GraphDriver']['Data']
	elif command == "mount":
		if len(sys.argv) < 3:
			print "You must provide an image name"
			sys.exit(1)
		imageName = sys.argv[2]
		mount = Mount.Mount(DockerImage.DockerImage(imageName))
		mount.performMount()
	elif command == "enter":
		if len(sys.argv) < 4:
			print "You must provide an image name to start and image name to mount"
			sys.exit(1)
		imageNameStart = sys.argv[2]
		imageNameMount = sys.argv[3]
		mount = Mount.Mount(DockerImage.DockerImage(imageNameMount))
                mount.performMount()
		docker= DockerUtil.DockerUtil()
		volumes = {mount.mountpoint : {'bind': '/mnt/rootfs', 'mode': 'ro'}}
                objContainer = docker.runContainer(imageNameStart, volumes, "/bin/sh -c 'while true; do sleep 10; done'")
