#! /usr/bin/python3

"""
Lab 2 - HTTP Server
NAME: Philo Decroos
STUDENT ID: 11752262
DESCRIPTION:
This python file is a simple HTTP server. It can recieve and send HTTP
messages through network sockets. It can process HTTP GET messages and respond
to the client with the requested content (HTML or images). It can also create
dynamic web content by using a CGI interface, executing scripts on the server
and pass their output to the client.
"""

import socket
from email.utils import formatdate
import subprocess


CRLF = "\r\n"
TYPE_STD = 'text/html'


def use_cgi(data, public_html, request_type, addr):
    """
    This function is called to execute a CGI script. We extract the URI and
    querystring from the received data and call the requested script in a
    subprocess, passing environment variables to it. We return the output of
    the CGI script.
    """

    url = data.split(' ')[1]
    if '?' in url:
        uri = url.split('?')[0]
        query = url.split('?')[1]
    else:
        uri = url
        query = ''

    my_vars = {'DOCUMENT_ROOT': public_html,
               'REQUEST_METHOD': request_type,
               'REQUEST_URI': uri,
               'QUERY_STRING': query,
               'PATH': os.environ['PATH'],
               'REMOTE_ADDR': addr[0]}

    p = subprocess.Popen(['python3', '.'+uri],
                         stdout=subprocess.PIPE, env=my_vars)
    return p.stdout.read().replace(str.encode('\n'), str.encode('<br>'))


def get_err_msg(code):
    """
    This function formats an error message depending on what error code is
    generated by the HTTP request. We wrap the error message in a HTML page
    so that it can be displayed by the client.
    """

    if code == '404':
        str = 'Page Not Found'
    else:
        str = 'Function Not Implemented'

    return ("<html>\n<head>\n" +
            "<title>" + code + ": " + str + "</title>\n" +
            "</head>\n<body>\n<center>" +
            "<h2>Error " + code + ": " + str + "</h2>" +
            "</center>\n</body>\n</html>\n")


def create_headers(code, type, length, conn):
    """
    This function creates the headers needed to send a correct HTTP response
    to the client. The content of the headers depends on the generated output
    code, the type and length of the content we send back and whether or not
    we close the TCP connection.
    """

    date = formatdate(timeval=None, localtime=False, usegmt=True)
    if code == '200':
        str = 'OK'
    elif code == '404':
        str = 'Not Found'
    elif code == '501':
        str = 'Not Implemented'

    msg = ("HTTP/1.1 " + code + str + CRLF +
           "Connection: " + conn + CRLF +
           "Content-Length: " + length + CRLF +
           "Date: " + date + CRLF +
           "Server: ServerName" + CRLF +
           "Content-Type: " + type + CRLF + CRLF)

    return msg


def serve(port, public_html, cgibin):
    """
    The entry point of the HTTP server.
    port: The port to listen on.
    public_html: The directory where all static files are stored.
    cgibin: The directory where all CGI scripts are stored.

    Here we create a socket and listen for HTTP requests, analyze them,
    call the correct fuctions to handle them and send generated responses.
    """

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        serverSocket.bind(('', port))
    except socket.error as msg:
        print('Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    while 1:
        serverSocket.listen(10)
        connectionSocket, addr = serverSocket.accept()

        while 1:
            data = connectionSocket.recv(1024)
            data = data.decode()
            if data:
                request_type = data.split()[0]

            if request_type != 'GET':
                err_msg = get_err_msg('501')
                size = str(len(err_msg))
                msg = create_headers('501', 'text/html', size, 'close')
                connectionSocket.send(str.encode(msg))
                connectionSocket.send(str.encode(err_msg))
                break

            path = data.split()[1]
            if path.startswith("/cgi-bin"):
                output = use_cgi(data, public_html, request_type, addr)
                size = str(len(output))
                msg = create_headers('200', 'text/html', size, 'keep-alive')
                connectionSocket.send(str.encode(msg))
                connectionSocket.send(output)
                continue

            if path == '/':
                path = '/index.html'
            if path.endswith('png'):
                c_type = 'image/png'
            else:
                c_type = TYPE_STD

            try:
                if c_type != 'image/png':
                    file = open(public_html + path, 'r')
                else:
                    file = open(public_html + path, 'rb')
            except IOError:
                err_msg = get_err_msg('404')
                size = str(len(err_msg))
                msg = create_headers('404', 'text/html', size, 'close')
                connectionSocket.send(str.encode(msg))
                connectionSocket.send(str.encode(err_msg))
                break

            filesize = str(os.stat(public_html+path).st_size)
            msg = create_headers('200', c_type, filesize, 'keep-alive')
            connectionSocket.send(str.encode(msg))

            if c_type != 'image/png':
                connectionSocket.send(str.encode(file.read()))
            else:
                connectionSocket.send(file.read())

    serverSocket.close()


# This the entry point of the script.
# Do not change this part.
if __name__ == '__main__':
    import os
    import sys
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--port', help='port to bind to', default=8080, type=int)
    p.add_argument('--public_html', help='home directory',
                   default='./public_html')
    p.add_argument('--cgibin', help='cgi-bin directory', default='./cgi-bin')
    args = p.parse_args(sys.argv[1:])
    public_html = os.path.abspath(args.public_html)
    cgibin = os.path.abspath(args.cgibin)
    serve(args.port, public_html, cgibin)
