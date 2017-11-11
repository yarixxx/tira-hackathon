#!/usr/bin/env python

import os
import urllib
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import course
import lesson


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



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/show_course', course.ShowCourse),
    ('/list_courses', course.ListCourses),
    ('/create_course', course.CreateCourse),
    ('/create_lesson', lesson.CreateLesson),
    ('/show_lesson', lesson.ShowLesson),
    ('/list_lessons', lesson.ListLessons),
], debug=True)
