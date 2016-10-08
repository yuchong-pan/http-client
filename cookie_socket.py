import Cookie
import socket

def domain_match(cookie_domain, domain):
    return ('.'+domain).endswith(cookie_domain)

def path_match(cookie_path, path):
    if not cookie_path.endswith('/'):
        cookie_path += '/'
    return path.startswith(cookie_path)

if __name__ == '__main__':
    print 'Host:'
    host = raw_input().strip()
    print 'Port:'
    try:
        port = int(raw_input().strip())
    except:
        port = 80
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
    file_exist = True
    try:
        f = open('cookie.txt', 'r')
    except:
        file_exist = False
    cookies = Cookie.SimpleCookie()
    if file_exist:
        for cookie in f.readlines():
            cookies.load(cookie)
        f.close()
    for cookie_name in cookies:
        cookie = cookies[cookie_name]
        if domain_match(cookie['domain'], host) and path_match(cookie['path'], url):
            if 'Cookie' not in headers:
                headers['Cookie'] = cookie.output(header='').lstrip()
            else:
                headers['Cookie'] += ',%s' % cookie.output(header='')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    request = "%s %s HTTP/1.1\r\nHost: %s\r\nConnection: Close\r\n" % (method, url, host)
    for header in headers:
        request += "%s: %s\r\n" % (header, headers[header])
    request += "\r\n" + body
    s.sendall(request)
    recv_data = ''
    while True:
        data = s.recv(4096)
        recv_data += data
        if not data:
            break
    print recv_data
    end_header = recv_data.find('\r\n\r\n')
    search_start = 0
    while True:
        set_cookie = recv_data.find('Set-Cookie:', search_start, end_header)
        if set_cookie == -1:
            break
        end_cookie = recv_data.find('\r\n', set_cookie)
        cookies.load(recv_data[set_cookie:end_cookie])
        search_start = end_cookie
    f = open('cookie.txt', 'w')
    f.write(cookies.output())
    f.close()
    s.close()
