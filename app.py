#!/usr/bin/env python

from google.appengine.api import urlfetch
import urllib
import simple_square_report
import square_pay

import os
import json
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import send_sms

USER_TO_PHONE = dict({
    'user1': '16509963350',
    'user2': '12016877934',
    'user3': '16692546680'
})


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            message = 'logout url'
            url = users.create_logout_url(self.request.uri)
        else:
            message = 'login url'
            url = users.create_login_url(self.request.uri)
        main_page = {
            'user': user.email() if user else '',
            'message': message,
            'url': url,
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(main_page))

class ClassesList(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        user = users.get_current_user()
        class_id = self.request.get('classId', None)
        classes_list = [
          {
            "classId": "class1",
            "title": "Yoga class for beginners",
            "date": "1510520826",
            "description": "Group class for beginners",
            "location":{
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "10",
            "attendees":[
              {
                "customerId": "customerL",
                "firstName": "Ihor",
                "lastName": "Lutskyy",
              },
              {
                "customerId": "customerK",
                "firstName": "Iaroslav",
                "lastName": "Karandashev",
              }
            ]
          },
          {
            "classId": "class2",
            "title": "Advanced Yoga class",
            "date": "1510607226",
            "description": "Advanced Yoga Group class",
            "location":{
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "20",
            "attendees":[
              {
                "customerId": "customerM",
                "firstName": "Stas",
                "lastName": "Makarenko",
              },
              {
                "customerId": "customerK",
                "firstName": "Iaroslav",
                "lastName": "Karandashev",
              }
            ]
          },
          {
            "classId": "class3",
            "title": "Yoga class for beginners",
            "date": "1511125626",
            "description": "Group class for beginners",
            "location":{
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "10",
            "attendees":[
              {
                "customerId": "customerO",
                "firstName": "Sergiy",
                "lastName": "Osypov",
              },
              {
                "customerId": "customerL",
                "firstName": "Ihor",
                "lastName": "Lutskyy",
              }
            ]
          }
        ]
        if class_id:
            one = next((x for x in classes_list if x.get('classId') == class_id), None)
            self.response.write(json.dumps({
                'class': one,
                'is_logged_in': True if user else False,
                'url': users.create_logout_url(self.request.uri) if user else users.create_login_url(self.request.uri)
            }))
        else:
            self.response.write(json.dumps({
                'classes_list': classes_list,
                'is_logged_in': True if user else False,
                'url': users.create_logout_url(self.request.uri) if user else users.create_login_url(self.request.uri)
            }))

class Notify(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        message = self.request.POST.get('message', None)
        teacher = self.request.POST.get('teacher', None)
        student = self.request.POST.get('student', None)
        if not message or not teacher or not student:
            logging.exception('Check arguments, please: %s, %s, %s' % (message, teacher, student))
            self.response.write(json.dumps({'Check': 'parameters, please! %s, %s, %s' % (message, teacher, student)}))
        else:        
            send_sms.send_sms(
                from_phone='12016958217',
                to_phone=USER_TO_PHONE.get(student),
                message=message)
            self.response.write(json.dumps({'ok': True}))

class LastPayments(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps({'payments': simple_square_report.get_square_report()}))

class Pay(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        nonce = self.request.POST.get('nonce', None)
        if nonce:
            result = square_pay.pay(nonce=nonce)
            self.response.write(json.dumps({'message': result})) 
        else:
           self.response.write(json.dumps({'message': 'Where is noance?'})) 

class Process(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        # logging.info('Check arguments: ' + json.dumps(self.request.POST))
        self.response.write(json.dumps({'message': 'Thanks!'}))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/classes_list', ClassesList),
    ('/notify', Notify),
    ('/last_payments', LastPayments),
    ('/pay', Pay),
    ('/process', Process)
], debug=True)
