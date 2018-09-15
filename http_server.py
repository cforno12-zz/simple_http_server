import socket
import threading
import sys

HOST = "localhost"               # Symbolic name meaning all available interfaces
PORT = 8000              # Arbitrary non-privileged port

def create_TCP_socket():
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind this socket to a port
    server_socket.bind((socket.gethostname(), PORT))
    
    #listen for X amount of connection
    server_socket.listen(5)

    return server_socket

def is_GET_command(command):
    return command is "GET"

def client_thread(client_socket):
    pass
    #do something with this client socket

def retrieve_source(resource):
    folder, filename = resource.strip.split('/')
    if folder is "www":
        # do something here
        content = None
        with open(resource, 'r') as current_file:
            content = current_file.read()

        return content
        
    else:
        return
        # return an error 

def parse_request(request):
    request_str = request.decode("utf-8")
    request_array = request_str.splitlines()

    '''
    SAMPLE GET REQUEST
    GET /docs/index.html HTTP/1.1
    Host: www.nowhere123.com
    Accept: image/gif, image/jpeg, */*
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
    (blank line)
    '''
    # we only want the first line of the request

    command, resource, http_verison = request_array[0].split()

    if is_GET_command(command):
        retrieve_source(resource)
    else:
        # send error code back to client

    

    
    


if __name__ == "__main__":

    serversocket = create_TCP_socket()

    while True:

        print ("we are runnning...")
        
        # accepting a connection from the outside
        client_socket, clientadd = server_socket.accept()

        request = client_socket.recv(4096)

        parse_request(request)
        
        # handle this connection on a thread
        client_thread = client_thread(client_socket)

        
        
        server_socket.close()
        
        
