'''
Created on Sep 4, 2010

@author: axa
'''
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
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


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/search', Search)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()