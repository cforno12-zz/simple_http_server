import socket
import threading
import sys
from datetime import datetime
import os
import platform
import magic
from wsgiref.handlers import format_date_time
from time import mktime

HOST = socket.gethostname()
PORT = 0              # Arbitrary non-privileged port

def create_TCP_socket():
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind this socket to a port
    server_socket.bind((HOST, PORT))
    
    #listen for X amount of connection
    server_socket.listen(5)

    return server_socket


def client_thread(client_socket):
    pass
    #do something with this client socket

def retrieve_source(resource):
    file_array = resource.strip().split('/')
    if file_array[1] == "www":
        print("file exists")
        content = None
        resource = "." + resource
        with open(resource, 'r') as current_file:
            content = current_file.read()
        return content
    else:
        return None

def get_curr_date():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)

def modified_date_of_file(filename):
    stamp = os.path.getmtime(filename)
    date = datetime.fromtimestamp(stamp)
    return format_date_time(mktime(date.timetuple()))

def get_size_of_file(filename):
    return str(os.path.getsize(filename))
    

def header_response_200(http_version, resource_path):
    response = ""
    # append http verison and 200 response
    response += (http_version + " 200 OK\r\n" )
    # add date and time
    date_str = get_curr_date()
    response += (date_str + "\r\n")
    # server name
    response += "Server: Forno/1.0 (Darwin)\n\r"
    # time last modified path
    resource_path = "." + resource_path.strip() # we want the current directory
    response += modified_date_of_file(resource_path)
    response += "\r\n"
    # get MIME type
    mime = magic.Magic(mime=True)
    response += "Content-Type: " + mime.from_file(resource_path) + "\r\n"
    # get file size
    response += "Content-Length: " + get_size_of_file(resource_path) + "\r\n"
    print(response)
    return response
    
    
    

def get_bytes_response_200(http_version, resource):
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

#400 bad request
def get_bytes_response_400():
    response = ""
    # just 400 status code
    response += "400 Bad Request Error\r\n"
    response += get_curr_date() + "\r\n"
    return str.encode(response)

def does_file_exist(filepath):
    if filepath.startswith("."):
        return os.path.isfile(filepath)
    else:
        filepath = "." + filepath
        return os.path.isfile(filepath)

def get_bytes_response_404(http_version):
    response = ""
    response += "404 Not Found\r\n"
    response += get_curr_date() + "\r\n"
    return str.encode(response)

def get_response(request):
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
    if len(request_array[0].split()) != 3:
        return get_bytes_response_400("HTTP/1.1")

    command, resource, http_version = request_array[0].split()

    print ("We are parsing the request...")
    print ("Command:", command, "// Resource:" , resource)

    if command == "GET":
        #check if the file exists
        if does_file_exist(resource):
            print("sending 200 response")
            return get_bytes_response_200(http_version, resource)
        else:
            return get_bytes_response_404(http_version)
            #send 404 not found
    else:
        return get_bytes_response_400(http_verison)
    

if __name__ == "__main__":

    while True:

        server_socket = create_TCP_socket()

        print ("Server is running on", HOST, ":", server_socket.getsockname()[1])

        # accepting a connection from the outside

        client_socket, clientadd = server_socket.accept()

        request = client_socket.recv(4096)

        answer = get_response(request)
        
        client_socket.sendall(answer)
        
        server_socket.close()

