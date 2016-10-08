import Cookie
import httplib
import sys

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
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, url, body, headers)
    res = conn.getresponse()
    if res.version == 10:
        print '\nHTTP/1.0', res.status, res.reason
    elif res.version == 11:
        print '\nHTTP/1.1', res.status, res.reason
    headers = res.getheaders()
    for header in headers:
        print "%s: %s" % (header[0], header[1])
    print "\n%s" % res.read()
    cookies.load(res.getheader('Set-Cookie'))
    f = open('cookie.txt', 'w')
    f.write(cookies.output())
    f.close()
    conn.close()
