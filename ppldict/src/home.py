# -*- coding: utf-8 -*-
'''
Created on Sep 4, 2010

@author: axa
'''
import db_entity
import os

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    def get(self):
        username = users.get_current_user()
        if username:
            users.create_logout_url(self.request.uri)
            show_username = username
            url_text = 'Logout'
        else:
            users.create_login_url(self.request.uri)
            show_username = username
            url_text = 'Login'
        
        template_dict = {'show_username':show_username, 'url_text':url_text,}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_dict))

class Search(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, It\'s search')
     
        
class Add(webapp.RequestHandler):
    @login_required
    def get(self):
        self.response.out.write(template.render('add.html',''))
        
    def post(self):
        #self.response.out.write('Hello World')
        login_user = users.get_current_user()
        if login_user:
            creator = login_user.nickname()
            word = self.request.get("word")
            define = self.request.get("define")
            example = self.request.get("example")
            tags = self.request.get("tag").split(',')
            new_tags = map(lambda x:x.strip(), tags)
            try:
                create_entity = db_entity.Words(key_name='w3',
                                                Creator=creator,
                                                Word=word,
                                                Define=define,
                                                Example=example,
                                                Tag=new_tags)
                create_entity.put()
                #response = {'status':'success', 'message':'新字增加好了'}
                response = {'status':'success', 'message':'wahaha'}
                self.response.out.write(simplejson.dumps(response))
            except ValueError:
                response = {'status':'error', 'message':'Oops爛了'}
                self.response.out.write(simplejson.dumps(response))
        else:
            self.redirect(users.create_login_url(self.request.uri))
                
                
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/search', Search),
                                      ('/add', Add)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()