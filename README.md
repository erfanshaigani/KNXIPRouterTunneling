# KNXIPRouterTunneling
KNX bus monitoring from outside

KNX/IP router incorporates several interesting capabalities which enables us to communicate with the bus.
One of these is that we can establish a link to the router via ethernet and communicate with it at port 3671 over UDP.

By analyzing the communication between the router and ETS, I created my own BUS monitoring tool.
with this snippet of code I am able to send a tunneling request to the router, receive the response and also receive all the telegrams
on the bus.
