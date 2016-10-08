import httplib
import sys

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
    conn.close()
