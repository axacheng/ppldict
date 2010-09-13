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
            url_link = users.create_logout_url(self.request.path)
            url_text = '登出'
            login_status = True
        else:
            url_link = users.create_login_url(self.request.path)
            url_text = '先登入才能增加新字'
            login_status = None
        
        template_dict = {'url_link':url_link, 'url_text':url_text,
                         'login_status':login_status,}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        #self.response.out.write(template_dict)
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