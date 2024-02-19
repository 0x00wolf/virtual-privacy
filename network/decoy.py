import socket

def create_http_response(content):
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: {}\r\n".format(len(content))
    response += "\r\n"
    response += content
    return response
