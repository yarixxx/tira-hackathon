from google.appengine.api import urlfetch
import urllib

API_KEY = '76d1b324'
API_SECRET = 'd4ace30618c703cd'

def send_sms(from_phone, to_phone, message): 
    try:
        form_data = urllib.urlencode({
            'from': from_phone,
            'to': to_phone,
            'text': message,
            'api_key': API_KEY,
            'api_secret': API_SECRET,
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        result = urlfetch.fetch(
            url='https://rest.nexmo.com/sms/json',
            payload=form_data,
            method=urlfetch.POST,
            headers=headers)
        return result.content
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')
