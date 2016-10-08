import socket
import ssl

if __name__ == '__main__':
    print 'Host:'
    host = raw_input().strip()
    print 'Port:'
    try:
        port = int(raw_input().strip())
    except:
        port = 443
    print 'Method:'
    method = raw_input().strip()
    print 'Url:'
    url = raw_input().strip()
    print 'Headers:'
    headers = {}
    while True:
        try:
            header = raw_input().strip()
        except:
            break
        colon = header.find(':')
        key = header[0:colon]
        content = header[colon+1:]
        if key != '':
            headers[key] = content
    print 'Body:'
    body = ''
    while True:
        try:
            body += raw_input()
        except:
            break
    print ''
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host)
    ssl_socket.connect((host, port))
    request = "%s %s HTTP/1.1\r\nHost: %s\r\nConnection: Close\r\n" % (method, url, host)
    for header in headers:
        request += "%s: %s\r\n" % (header, headers[header])
    request += "\r\n" + body
    ssl_socket.sendall(request)
    while True:
        data = ssl_socket.recv(4096)
        if not data:
            break
        else:
            print data
    ssl_socket.close()
