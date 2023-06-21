# project1-distributedSystems-UFABC
Python Project that uses sockets to simulate communication between N peers and one server. 


Socket programming is one of the most fundamental technologies of computer network programming. A socket is an endpoint of a two-way communication link between two programs running on the network.
Python has quite an easy way to start with the socket interface.

Thread: is a sequence of such instructions within a program that can be executed independently of other code.
Multithreaded program contains two or more parts that can run concurrently. Each part of such a program is called a thread, and each thread defines a separate path of execution.

**Multithreaded Socket Server** can communicate with more than one client at the same time in the same network.

In this example and project I decided to use threads because we need that one server communicates with more than one client(peer), N peers for exemple.
So using multithreaded socket server, we can accept more than one peer connection.


When the Python Client program starts , it will connect to the Python Server Socket Program and waiting input from client side. When you type the message it will send to the server and then you can see the reply messages from server side too.