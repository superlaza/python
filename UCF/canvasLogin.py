#-i'd like to further automate the process of getting the course id's
#separate calendar and canvas logic

import urlparse
import BaseHTTPServer
import cookielib
import urllib
import urllib2
import json
from datetime import datetime
from datetime import timedelta
import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

#globals
#david's calendar
#calendarName = 'superlaza7@gmail.com'
#chelsie's calendar
calendarName = 'chelskolberg@gmail.com'

#setup http handlers globally
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

#creds for google api
flow = OAuth2WebServerFlow(client_id='348501136255.apps.googleusercontent.com',
                           client_secret='ko56eVmpP4rHbxzzBXPn2yJj',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://localhost')

def get_code():
    auth_uri = flow.step1_get_authorize_url()
    response = opener.open(auth_uri)
    open('grant_access_page.html', 'w').write(response.read())

def get_access_to_calendar():

    '''
    To create the credentials argument from scratch you need a code, which is used
    as [credentials = flow.step2_exchange(code)]. The code comes from the part of
    the OAuth flow where the authorization server redirects to the client's server
    with a code in the url representing the client's access code. I got the code
    using the chrome browser, then stored the resulting credentials for future use
    so i woulnd't have to get a new code every time. For reference on the OAuth flow,
    see https://developers.google.com/api-client-library/python/guide/aaa_oauth
    '''

    #code = '<insert code here>'
    #credentials = flow.step2_exchange(code)

    #get stored credentials from file
    storage = Storage('credentialsChelsie')
    #storage = Storage('credentials')
    credentials = storage.get()

    #storage.put(credentials)

    #add creds gained from OAuth flow to the http requests
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('calendar', 'v3', http=http)
    return service

def add_events(service):
    urlMain = 'https://canvas.instructure.com'

    #canvas access token added as query to url
    '''david's token'''
    #token  = '?access_token=13~As2jetN5ol5hpZRKptVdxioD0OMoePRFB3SXfJiOzyU8VtOuFoAfa56JH2Ir51bT'
    '''chelsie's token'''
    token = '?access_token=13~nLr69NsIXwAdhosyPJJdk8k5HmZY6qvHMlYzmcnb5DDzFi3AshYOOIgYI9XC8BlU'
    
    debug = False
    #list events
    event_list = list(set(list_events(service).values()))
    print 'finally'

    courseList = json.loads(opener.open(urlMain+'/api/v1/courses/'+token).read())
    
    #i could keep a local store of events already posted to minimize API calls,
    #but I am lazy
    for course in courseList:
        #get assignment list for each course
        response = opener.open(urlMain+courseURL(course['id'])+token)
        hwList = json.loads(response.read())
        if debug == True:
            print json.dumps(hwList,indent=4, separators=(',', ': '))
            print '=============='+course['course_code'][:3]+"=============\n"
        for hw in hwList:
            if hw['due_at'] is not None and hw['name'] not in event_list:
                event = createEvent(hw['name'], course['course_code'][:3], hw['due_at'])
                created_event = service.events().insert(calendarId=calendarName, body=event).execute()
                event_details = "{}, {}\n".format(hw['name'].encode('utf-8'), course['course_code'][:3])
                if created_event is not None:
                    print "added event: "+event_details
                else:
                    print "failed to add event: "+event_details
                if debug == True:
                    print hw['name'], hw['due_at']
                    print datetime.strptime(hw['due_at'][:-6], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")
        if debug == True:
            print '\n\n'

def delete_all(service):
    event_list = list_events(service)
    count = 0
    for eventId, eventSummary in event_list.iteritems():
        service.events().delete(calendarId=calendarName, eventId=str(eventId)).execute();
        count += 1
    print "deleted "+str(count)+" events."

def delete_duplicates(service):
    event_list = list_events(service)
    count = 0
    ref =[]
    for eventId, eventSummary in event_list.iteritems():
        print eventId+', '+eventSummary
        #ref collects novel events
        if eventSummary not in ref:
            ref.append(eventSummary)
        #if event is in the reference, it's a duplicate
        else:
            service.events().delete(calendarId=calendarName, eventId=str(eventId)).execute();
            count += 1
    print "deleted "+str(count)+" duplicates."

#lists all the events created by this script
def list_events(service):
    event_list = {}
    count = 0
    page_token = None
    while True:
        events = service.events().list(calendarId=calendarName, pageToken=page_token).execute()
        if events['items']:
            for event in events['items']:
                #if event has summary attribute
                if 'description' in event:
                    if 'summary' in event and event['description']=='Canvas':
                        print event['summary']
                        event_list[str(event['id'])] = str(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return event_list

#returns event dict
def createEvent(assignment, class_name,  due_date):
    #calculate half hour before due_date using datetime arithmetic
    due_date_minus = datetime.strptime(due_date[:-6], "%Y-%m-%dT%H:%M:%S")-timedelta(hours=1)
    event =  {
    "summary": assignment,
    "description": 'Canvas', #marker to identify events added by this script
    "location": class_name,
    "start": {
        "dateTime": due_date_minus.isoformat()+"-04:00"
    },
    "end": {
        "dateTime": due_date
    }, 
    "reminders": {
        "overrides": [
            {
                "minutes": 60, 
                "method": "popup"
            },
            {
                "minutes": 180, 
                "method": "popup"
            },
            {
                "minutes": 720, 
                "method": "popup"
            }
        ], 
        "useDefault": "false"
    }
    }

    return event

def courseURL(course):
        url = '/api/v1/courses/'+str(course)+'/assignments'
        print url
        return url

#get_code()
service = get_access_to_calendar()
#delete_duplicates2(service)
add_events(service)
