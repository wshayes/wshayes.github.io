---
title: "Python SSH Tunnel Example"
date: 2015-02-04T06:13:00.001Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

Notes for myself and hopefully others.

```
def createTunnel(localport, remoteport, identityfile, user, server):
    """Create SSH Tunnels for Database connections"""

    import shlex
    import subprocess
    import time

    sshTunnelCmd = "ssh -N -L %s:127.0.0.1:%s -i %s %s@%s" % (
		localport, remoteport, identityfile, user, server
	)

    args = shlex.split(sshTunnelCmd)
    tunnel = subprocess.Popen(args)

    time.sleep(2)  # Give it a couple seconds to finish setting up

    return tunnel  # return the tunnel so you can kill it before you stop
				   # the program - else the connection will persist 
				   # after the script ends

def closeSSHTunnel(tunnels):
    """Close SSH tunnels - given the process handles"""

    for tunnel in tunnels:
        tunnel.kill()

localport = 27018  # local port for MongoDB
remoteport = 27017  # remote server port for MongoDB
identityfile = '/home//.ssh/id_rsa.pem'
user = 'ubuntu'
server = 'example.com'

# Start tunnel
tunnel = createTunnel(localport, remoteport, identityfile, user, server)

try:
	# Example usage
	db_server = 'localhost'
	db_port = 27018
	client = pymongo.MongoClient('mongodb://{}:{}'.format(db_server, db_port))
	pydb = client.agencies

finally:
	closeSSHTunnel([tunnel])
```
