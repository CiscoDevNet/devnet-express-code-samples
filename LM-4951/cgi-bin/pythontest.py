#!/usr/local/bin/python3
print ("Content-type: text/html")
print ()
print ("<html><head><title>Situation snapshot</title></head><body><pre>")

import sys
sys.stderr = sys.stdout

import os
from cgi import escape
print ("<strong>Python %s</strong>" % sys.version)
keys = os.environ.keys(  )

for k in keys:
    print ("%s\t%s" % (escape(k), escape(os.environ[k])))
print ("</pre></body></html>")
