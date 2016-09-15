# Running chart.py

Chart.py renders Splunk charts in Minecraft.  It has a number of dependencies which are required to run it.  Here's a list of commands on Ubuntu which will install them:

	sudo apt-get update && apt-get install -y python-cairo python-pycha python-pil python-pip
	sudo pip install pypng && pip install splunk-sdk
	sudo cp raspberryjuice-1.8.jar /<minecraftdir>/plugins/raspberryjuice-1.8.jar
	sudo cp pycha-pie.diff /<minecraftdir>/pycha-pie.diff
	sudo patch /usr/share/pyshared/pycha/pie.py /<minecraftdir>/pycha-pie.diff
	sudo cp chart.py /<minecraftdir>/chart.py
	sudo cp OpenSans-Regular.ttf /<minecraftdir>/OpenSans-Regular.ttf



# Docker Bukkit
## A Bukkit/Spigot server on docker
Bukkit, a moddable Minecraft server. On Docker. Neat, huh?

Tags follow Bukkit's version numbers, or you can track the latest version by using `latest`.
Tags: 
* `latest` ([latest/Dockerfile](https://github.com/bbriggs/docker-bukkit/blob/latest/Dockerfile))
* `1.8.8`  ([1.8.8/Dockerfile](https://github.com/bbriggs/docker-bukkit/blob/1.8.8/Dockerfile))
* `1.8.3`  ([1.8.3/Dockerfile](https://github.com/bbriggs/docker-bukkit/blob/1.8.3/Dockerfile))
* `1.8`  ([1.8/Dockerfile](https://github.com/bbriggs/docker-bukkit/blob/1.8/Dockerfile))

### Running the server
To start the server and accept the EULA in one fell swoop, just pass the `EULA=true` environment variable to Docker when running the container. I recommend mounting a directory from your host onto `/data` in the container to make map and server data persistent. 

Example:
`docker run -it -v /data:/data -p 25565:25565  -e EULA=true --name mc_server bbriggs/bukkit` 
