import cookielib
import urllib
import urllib2

# set these to whatever your fb account is
usn = "superlaza7@gmail.com"
pwd = "moni6772"
f = open("outupt.html", 'w')

cj = cookielib.CookieJar()
opener = urllib2.build_opener(
    urllib2.HTTPRedirectHandler(),
    urllib2.HTTPHandler(debuglevel=0),
    urllib2.HTTPSHandler(debuglevel=0),
    urllib2.HTTPCookieProcessor(cj)
)
opener.addheaders = [
    ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                   'Windows NT 5.2; .NET CLR 1.1.4322)'))
]

"""
Handle login. This should populate our cookie jar.
"""
login_data = urllib.urlencode({
    'email' : usn,
    'pass' : pwd,
})
response = opener.open("https://login.facebook.com/login.php", login_data)
print response.read()

response = opener.open("https://login.facebook.com/login.php", login_data)
#print response.read()
f.write(response.read())
