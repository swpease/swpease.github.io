Title: Setting up Gunicorn with systemd on Ubuntu
Date: 2019-01-25
Category: Notes
Tags: computer, backend, howto

# Background
Gunicorn provides [a number of ways](http://docs.gunicorn.org/en/stable/deploy.html) for you to handle running it in deployment. You need a supervisor, which is just a process that monitors and manages some other process. So you can tell it things like, 'start gunicorn when someone first requests a webpage' and 'reload gunicorn when it crashes'.

In skimming over the options that Gunicorn listed, I initially thought of using Supervisor, probably because I had seen it mentioned before. I am wary of my disposition to trusting things just because I've heard of them, but decided to look into it anyway. I saw that I would need to install Python 2 to use it, and put my foot down.
I decided to try out systemd because it was a built-in tool, and I am suspicious of taking on dependencies for what seem to be minimal tasks. It also seemed the most generalizable thing to learn.

# Research
The best basic introduction I found was on [Digital Ocean](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files#anatomy-of-a-unit-file).
The systemd creators have their documentation as well: [systemd](https://www.freedesktop.org/software/systemd/man/systemd.service.html#), [systemctl](https://www.freedesktop.org/software/systemd/man/systemctl.html).
More advanced topics, such as security and setting up your own software to handle systemd socket stuff, are covered in this dude Pid Eins's [blog](http://0pointer.de/blog/projects/security.html), though it's not spectacularly organized.
For implementing systemd for Gunicorn, I referenced mostly [Gunicorn](http://docs.gunicorn.org/en/stable/deploy.html), but also [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-a-gunicorn-systemd-service-file).
I might need a systemd service file for [nginx](https://www.nginx.com/resources/wiki/start/topics/examples/initscripts/).

# Execution
Gunicorn recommends setting up a socket, which is always listening, which starts up Gunicorn proper via a corresponding "service". Per Eins's blog, this can be a more efficient way to use resources. For instance, if you have a bunch of rarely-accessed websites on the same server, you could activate / deactivate them as needed. I wonder if this is how Heroku manages its hobby-tier apps.

The gunicorn.socket file is super simple:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn/socket

[Install]
WantedBy=sockets.target
```
It basically specifies an address to listen on for a stream socket. systemd appears to create this socket as part of this gunicorn.socket file's existence -- this socket is the only contents of /run/gunicorn when you navigate to it upon starting up the server.

The gunicorn.service is a bit more complex:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=vagrant
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/vagrant/mysite
ExecStart=/home/vagrant/.local/share/virtualenvs/vagrant-gKDsaKU3/bin/gunicorn --pid /run/gunicorn/pid --bind unix:/run/gunicorn/socket mysite.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
This is more complex. An annotation (NB: I do not know what all of these mean) goes something like:

`Requires=gunicorn.socket` says that gunicorn.service is dependent upon gunicorn.socket.

`PIDFile=/run/gunicorn/pid` I'm unsure why Gunicorn's docs have this in here. Look at the systemd docs for more info on it.

`User` and `Group` per Digital Ocean,
> We will give our regular user account ownership of the process since it owns all of the relevant files. We'll give group ownership to the www-data group so that Nginx can communicate easily with Gunicorn.

I am still a bit unclear about what user and group will be needed.

`RuntimeDirectory=gunicorn` The [docs](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#) indicate that the directory's lifetime will be bound to the daemon's. Upon running `sudo systemctl stop gunicorn.service`, which calls the `ExecStop` command, /run/gunicorn is empty, i.e. the socket is gone. It looks like this declaration supersedes the Gunicorn docs's suggestion of having /etc/tmpfiles.d/gunicorn.conf (systemd says tmpfiles.d is for complex cases).
Removing this line yields the following error when trying to connect:
>curl: (56) Recv failure: Connection reset by peer

And it appears that /run/gunicorn and its parent dirs are owned by root with permissions 755. Conversely, when RuntimeDirectory is specified, /run/gunicorn has User and Group equal to what they were specified as in the gunicorn.service file (vagrant and www-data in this case).
When the service has been halted, then, per RuntimeDirectory's behavior, /run/gunicorn will be deleted. As such, to restart things, you need to restart gunicorn.socket with `sudo systemctl restart gunicorn.socket`. This will recreate the /run/gunicorn directory with the socket in it.

`WorkingDirectory` sets the directory for any executed commands (e.g. ExecStart).

`ExecStart` and company are just commands to execute at the relevant lifecycle events. For my purposes, because I have Gunicorn installed via a virtual environment, I have to provide the path to its actual install. I think I could alternatively use other lifecycle hooks to start and stop the virtual environment, the just call 'gunicorn' in my ExecStart.

`PrivateTmp` is described as a security feature (see also Eins's blog)

# Problems I Encountered
I made some edits to my gunicorn.service file, and I was not getting my curl test to work (`curl --unix-socket /run/gunicorn/socket http://localhost:8000` *mind the port*). Upon restarting the VM, it worked. I believe I needed to run `sudo systemctl daemon-restart`.
