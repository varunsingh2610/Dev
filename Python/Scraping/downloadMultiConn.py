#!/usr/bin/python3
def download(url,start):
    req = urllib2.Request('https://github.com/zaproxy/zaproxy/releases/download/v2.8.0/ZAP_2_8_0_unix.sh')
    req.headers['Range'] = 'bytes=%s-%s' % (start, start+chunk_size)
    f = urllib2.urlopen(req)
    parts[start] = f.read()

threads = []
parts = {}

# Initialize threads
for i in range(0,10):
    t = threading.Thread(target=download, i*chunk_size)
    t.start()
    threads.append(t)

# Join threads back (order doesn't matter, you just want them all)
for i in threads:
    i.join()

# Sort parts and you're done
result = ''.join(parts[i] for i in sorted(parts.keys()))
