import socket
import threading
import sys
from datetime import datetime
import os
import platform
import magic

HOST = "localhost"               # Symbolic name meaning all available interfaces
PORT = 8000              # Arbitrary non-privileged port

def create_TCP_socket():
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind this socket to a port
    server_socket.bind((HOST, PORT))
    
    #listen for X amount of connection
    server_socket.listen(5)

    print ("returning server socket")
    return server_socket


def client_thread(client_socket):
    pass
    #do something with this client socket

def retrieve_source(resource):
    file_array = resource.strip().split('/')
    print(file_array[1])
    if file_array[1] == "www":
        print("file exists")
        content = None
        resource = "." + resource
        with open(resource, 'r') as current_file:
            content = current_file.read()
        return content
    else:
        return None

def header_response_200(http_version, resource_path):
    response = ""
    # append http verison and 200 response
    response += (http_version + " 200 OK\r\n" )
    # add date and time
    date_str = datetime.now().strftime('Date: %a, %d %b %Y %H:%M:%S %Z')
    response += (date_str + "\r\n")
    # server name
    response += "Server: Forno/1.0 (Darwin)\n\r"
    # time last modified path
    resource_path = "." + resource_path.strip() # we want the current directory
    response += datetime.fromtimestamp(os.path.getmtime(resource_path)).strftime("Last-Modified: %a, %d %b %Y %H:%M:%S %Z\r\n")
    # get MIME type
    mime = magic.Magic(mime=True)
    response += "Content-Type: " + mime.from_file(resource_path) + "\r\n"
    # get file size
    response += "Content-Length: " + str(os.path.getsize(resource_path)) + "\r\n"
    print(response)
    return response
    
    
    

def get_bytes_response(http_version, resource):
    print("preparing response header...")
    response = header_response_200(http_version, resource)
    # blank line
    response += "\r\n"
    response += retrieve_source(resource)

    print("FINAL RESPONSE")
    print(response)

    #convert string to bytes
    bytes_response = str.encode(response)
    
    return bytes_response
        
    
    

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

    command, resource, http_version = request_array[0].split()

    print ("We are parsing the request...")
    print ("Command:", command, "// Resource:" , resource)

    if command == "GET":
        print("sending 200 response")
        return get_bytes_response(http_version, resource)
        
    else:
        print("we returned false")
        pass
        # send error code back to client    
    

if __name__ == "__main__":

    server_socket = create_TCP_socket()

    while True:

        print ("Server is running on", HOST, ":", PORT)
        
        # accepting a connection from the outside
        client_socket, clientadd = server_socket.accept()

        print ("We accepted a connection")

        request = client_socket.recv(4096)

        answer = parse_request(request)
        
        client_socket.sendall(answer)
        
        server_socket.close()
