Title: Stuff About Ports and Sockets
Date: 2018-12-15
Category: Notes

Socket = {IP Address : Port}
Connection = {Local Socket + Remote Socket + Protocol}
Protocol = TCP, UDP, etc.
Listen = Look for client requests at a specific well-known port.

A server socket can serve multiple clients because the service just kinda keeps track of which requests are associated with which clients. Which I suppose makes complete sense without any thought.

[Stack Overflow](https://stackoverflow.com/questions/3329641/how-do-multiple-clients-connect-simultaneously-to-one-port-say-80-on-a-server): How to multiple clients connect simultaneously to one port?

When a client connects to a server, the client uses a random, unused, high-number port. That way multiple people with the same IP address (family, coworkers, etc.) can use the same service at the same time.

[Stack Overflow](https://stackoverflow.com/questions/1694144/can-two-applications-listen-to-the-same-port): Can two applications listen to the same port?

For TCP, no. That's the reason ports exist: to allow multiple applications to share the network without conflicts. Well, technically yes, but not without work.

[Wikipedia](https://en.wikipedia.org/wiki/Port_(computer_networking)):
>For TCP, only one process may bind to a specific IP address and port combination.
Common application failures, sometimes called port conflicts, occur when multiple programs attempt to use the same port number on the same IP address with the same protocol.

[Quora](https://www.quora.com/What-is-the-difference-between-HTTP-protocol-and-TCP-protocol): The differences between IP, TCP, HTTP, etc.


##Sockets

The answer given by Daniel Miller is quite good.
See also [Wikipedia](https://en.wikipedia.org/wiki/Internet_protocol_suite#Internet_layer).
>Application programmers are typically concerned only with interfaces in the application layer and often also in the transport layer, while the layers below are services provided by the TCP/IP stack in the operating system. Most IP implementations are accessible to programmers through sockets and APIs.

There are multiple, different definitions of "socket" depending on context. e.g. the [Berkeley socket](https://en.wikipedia.org/wiki/Berkeley_sockets), for which a socket is an abstract representation for the local endpoint of a network communication path. Incidentally, Berkeley sockets answers my questions about where IP and transport layer coding is stored / interacted with (a socket API).

And [Python sockets HOWTO](https://docs.python.org/3.7/howto/sockets.html)

Useful answer on [loopback](https://askubuntu.com/questions/247625/what-is-the-loopback-device-and-how-do-i-use-it)
[Berkeley sockets](https://docs.freebsd.org/44doc/psd/20.ipctut/paper.pdf)
