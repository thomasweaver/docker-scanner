from LocalScan import Command
from LocalScan import Output

commands=[]
commandsRaw=[[["dpkg", "--list"], r'^(?P<status>[a-zA-Z]+)\s+(?P<pkgname>.*?)\s+(?P<pkgversion>.*?)\s+(?P<pkgarch>.*?)\s+(?P<pkgdesc>.*)'], [["apt-get", "-s", "upgrade"], r'^(?P<upgraded>\d+) upgraded, (?P<newlyinstalled>\d+) newly installed, (?P<removed>\d+) to remove and (?P<notupgraded>\d+) not upgraded']]
for command in  commandsRaw:
	command = Command.Command(command[0], command[1])
	command.runCommand()
	command.parseOutput()
	commands.append(command)

#command=Command.Command(["dpkg", "--list"], r'^(?P<status>[a-zA-Z]+)\s+(?P<pkgname>.*?)\s+(?P<pkgversion>.*?)\s+(?P<pkgarch>.*?)\s+(?P<pkgdesc>.*)')
#command.runCommand()
#command.parseOutput()
#commands.append(command)
#command=Command.Command(["apt-get", "-s", "upgrade"], r'^(?P<upgraded>\d+) upgraded, (?P<newlyinstalled>\d+) newly installed, (?P<removed>\d+) to remove and (?P<notupgraded>\d+) not upgraded')
#178 upgraded, 0 newly installed, 0 to remove and 5 not upgraded.
#command.runCommand()
#command.parseOutput()
#commands.append(command)

output = Output.Output(commands, type="file", file="/mnt/results/command-output.json")
output.performOutput()
