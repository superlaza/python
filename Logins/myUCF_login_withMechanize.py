import mechanize
import cookielib


f = open("outupt4.html", 'w')

username = 'd2448663'   # your username/email
password = 'moni8459'   # your password

br = mechanize.Browser()

# set cookies
cookies = cookielib.LWPCookieJar()
br.set_cookiejar(cookies)

# browser settings (used to emulate a browser)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(False)
br.set_debug_responses(False)
br.set_debug_redirects(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open('https://my.ucf.edu/index.html') # open my.ucf.edu

br.select_form(nr=2) # select the form

br["userid"] = username
br['pwd'] = password
br.submit() # submit the login data

#now that we're logged in, visit student self service
mainURL = 'https://my.ucf.edu/psp/PAPROD/EMPLOYEE/HEPROD/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'
URL_append = '?pt_fname=FX_STUDENT_SLFSRV_MENU_90&FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90&IsFolder=true&ICAction=DERIVED_SSS_SCT_SSS_TERM_LINK'
iframeURL = 'https://cs89.net.ucf.edu/psc/HEPROD/EMPLOYEE/HEPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL'
iframeURL_append = '?ICAction=DERIVED_SSS_SCT_SSS_TERM_LINK'
iframeURL_appendGO = '?ICAction=DERIVED_SSS_SCT_SSR_PB_GO'

#br.open(mainURL+URL_append)
br.open(iframeURL)
br.open(iframeURL+iframeURL_append)

br.select_form("win0")
for control in br.form.controls:
    print control
    print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])

br.form.set_value(['4'],name='SSR_DUMMY_RECV1$sels$0')
submit_response = br.submit()
br.open(iframeURL+iframeURL_appendGO)
# https://webcourses.ucf.edu 

out  = br.response().read()
#out = submit_response.read()

#print(out) # print the response

f.write(out)
