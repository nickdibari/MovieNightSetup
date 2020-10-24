# MovieNightSetup

Collection of scripts and config files for running a MovieNight server.


## Installation

This section documents how to set up and run the MovieNight Docker container on a server.

Before getting started, clone this repository to the host

`git clone https://github.com/nickdibari/MovieNightSetup.git ~/MovieNightSetup`

### 1. Install nginx

We use nginx as a reverse proxy for MovieNight, so the app isn't directly exposed to the Internet. This allows us to serve the app from the default HTTP ports, so users don't have to fiddle with the port to access the stream. Additionally using nginx allows us to serve the app over HTTPS which is a more secure approach to serving content over the Internet.

First, we need to install nginx on the server

`sudo apt-get update && sudo apt-get install nginx`

This will set up all the nginx configuration needed to run the webserver at `/etc/nginx/`. Next, we need to add our nginx config to the available sites so nginx can use the config when it runs the server process. Copy the config file from this repo to `/etc/nginx/sites-available`.

`sudo cp nginx/movie-night.conf /etc/nginx/sites-available/movie-night`

Next, update the config file with the name of the server in place of the `$server_name` placeholders. This sets the domain name nginx will listen to for handling requests.

After you have the config file set up properly, you need to set up a symlink to that config file in `/etc/nginx/sites-enabled`. The easiest way to do this is to remove the default config symlink and add one for your config.

```
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/movie-night /etc/nginx/sites-enabled/default
```

We next need to open the HTTP ports so nginx can listen on them for incoming requests. You can use `ufw` to allow incoming traffic to the needed ports

```
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

Restart nginx to run the webserver with your config

`sudo systemctl restart nginx.service`

Finally, you need to install the SSL certificates to enable HTTPS for your server. I recommend using [LetsEncrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04) to generate the certificates for your server.

### 2. Install MovieNight

Next up is actually installing and running the MovieNight application. I recommend using their Docker setup as it is more portable and easier to run. You first need to install docker, you can find [Docker installation instructions here](https://docs.docker.com/engine/install/ubuntu/).

Next, clone the MovieNight repository to your home directory.

`git clone https://github.com/zorchenhimer/MovieNight.git ~/MovieNight`

You'll want to copy the configuration file in this repository (MovieNightSetup) to `~/MovieNight/settings.json` to configure the Docker image with your settings. At the very least you'll need to supply a `StreamKey` value to secure the streaming service.

`cp ~/MovieNightSetup/settings.json ~/MovieNight/`

Next, build the Docker image

`cd ~/MovieNight && docker build -t movienight .`

Finally, you can run the Docker image to start the MovieNight app. There are helper scripts in this directory for running the container and viewing the logs from the container. You should add these to your $PATH and run them for managing the MovieNight container.

```
cd ~/MovieNightSetup/scripts
sudo ln -s "$(pwd)/run_movienight.bash" /usr/local/sbin/movienight
sudo ln -s "$(pwd)/movienight_logs.bash" /usr/local/sbin/movienight-logs

movienight
movienight-logs
```
