# cs457-cs557-pa1-cforno12

## How to compile

* Run `make` or `python3 http_server.py`
 
## Errors

* If an error pops up for the magic library, run `pip3 install python-magic`
 
## Implementation

* When you run the program, it prints out the IP address and the port number it is running on.
* The program creates a new thread for every request
* I made file access atomic. In other words, I put a lock when it accesses files.
* I put all the byte results into a queue.
* When all the threads join, I send all the bytes to the client until the queue is empty.
* This server also handles 404 error code and responds with a 400 error code if the command is not a GET command.


 
 
