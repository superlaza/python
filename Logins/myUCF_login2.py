import cookielib
import urllib
import urllib2

# set these to whatever your fb account is
usn = "d2448663"
pwd = "moni8459"
f = open("outupt3.html", 'w')

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
    'userid' : usn,
    'pwd' : pwd,
})
response = opener.open("https://my.ucf.edu/index.html", login_data)
#print response.read()

response = opener.open("https://my.ucf.edu/psp/PAPROD/EMPLOYEE/EMPL/h/?tab=DEFAULT", login_data)
#print response.read()
#f.write(response.read())

#DERIVED_SSS_SCT_SSR_PB_GO
mainURL = 'https://my.ucf.edu/psp/PAPROD/EMPLOYEE/HEPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL'
search_data = {'SSR_DUMMY_RECV1$sels$0': '4'}
r = opener.open(urllib2.Request(mainURL+'?pt_fname=FX_STUDENT_SLFSRV_MENU_90&FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90&IsFolder=true&ICAction=DERIVED_SSS_SCT_SSR_PB_GO', urllib.urlencode(search_data)))
#request = urllib2.Request(mainURL+'?pt_fname=FX_STUDENT_SLFSRV_MENU_90&FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90&IsFolder=true&ICAction=DERIVED_SSS_SCT_SSR_PB_GO')
#response = opener.open(request)
#response = opener.open('https://my.ucf.edu/psp/PAPROD/EMPLOYEE/HEPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?pt_fname=FX_STUDENT_SLFSRV_MENU_90&FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90&IsFolder=true&ICAction=DERIVED_SSS_SCT_SSS_TERM_LINK')
html = r.read()
print html
f.write(html)
