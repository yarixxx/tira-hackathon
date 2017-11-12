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
        classes_list = """[{
          "classId": "class3",
          "title": "Kids Yoga",
          "date": "Today 4:45pm",
          "description": "10 min of intro and warm-up 20 min of running",
          "location":{
            "lat": 37.428893,
            "lon": -122.097782
          },
          "price": "10",
          "attendees":[
            {
              "image": "photo_1.jpg",
              "firstName": "Sergiy",
              "lastName": "Osypov"
            },
            {
              "image": "photo_2.jpg",
              "firstName": "Ihor",
              "lastName": "Lutskyy"
            },
            {
              "image": "photo_3.jpg",
              "firstName": "Stas",
              "lastName": "Makarenko"
            },
            {
              "image": "photo_4.jpg",
              "firstName": "Iaroslav",
              "lastName": "Karandashev"
            }
          ]
          
        },{
            "classId": "class1",
            "title": "Yoga class for beginners",
            "date": "Today 3:00pm",
            "description": "Group class for beginners. 20 min workout, 20 min yoga free time for chit-chat",
            "location":{
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "10",
            "attendees":[
              {
                "image": "photo_3.jpg",
                "firstName": "Ihor",
                "lastName": "Lutskyy"
              },{
                "image": "photo_2.jpg",
                "firstName": "Iaroslav",
                "lastName": "Karandashev"
              }
            ]
          },{
            "classId": "class2",
            "title": "Advanced Yoga Class",
            "date": "Tommorow 6:00pm",
            "description": "Advanced Yoga Group class. 10 min of intro and warm-up 30 min of running",
            "location": {
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "20",
            "attendees": [
              {
                "image": "photo.jpg",
                "firstName": "Stas",
                "lastName": "Makarenko"
              },{
                "image": "photo_1.jpg",
                "firstName": "Iaroslav",
                "lastName": "Karandashev"
              }
            ]
          },{
            "classId": "class3",
            "title": "Kids Yoga",
            "date": "Tommorow 6:00pm",
            "description": "",
            "location":{
              "lat": 37.428893,
              "lon": -122.097782
            },
            "price": "10",
            "attendees":[
              {
                "image": "photo_3.jpg",
                "firstName": "Sergiy",
                "lastName": "Osypov"
              },
              {
                "image": "photo_4.jpg",
                "firstName": "Ihor",
                "lastName": "Lutskyy"
              }
            ]
          }
        ]"""
        if class_id:
            one = next((x for x in json.loads(classes_list) if x.get('classId') == class_id), None)
            self.response.write(json.dumps({
                'class': one,
                'is_logged_in': True if user else False,
                'url': users.create_logout_url(self.request.uri) if user else users.create_login_url(self.request.uri)
            }))
        else:
            self.response.write(json.dumps({
                'classes_list': json.loads(classes_list),
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
        self.response.headers['Content-Type'] = 'text/html'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        nonce = self.request.POST.get('nonce', None)
        if nonce:
            result = square_pay.pay(nonce=nonce, amount=1000)
            self.response.write("<p>Success.</p>") 
        else:
           self.response.write("<p>Fail.</p>") 

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
