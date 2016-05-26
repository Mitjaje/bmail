#!/usr/bin/env python
import os
import jinja2
import webapp2

from datetime import time
from model import Sporocilo
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
     def get(self):
        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url, "user": user}

        return self.render_template("index.html", params)

     def post(self):

        user = users.get_current_user()
        tekst = self.request.get("tekst")
        sporocilo = Sporocilo(tekst=tekst, uporabnik=user.nickname())
        sporocilo.put()
        napaka = False
        parametri= {
            "sporocilo" : sporocilo,
            "napaka"    : napaka
        }

        return self.render_template("new.html", parametri)

class InboxHandler(BaseHandler):
    def get(self):
        params = {"sporocilo": "Tukaj sem tudi jaz, MainHandler"}
        self.render_template("inbox.html", params=params)

class SentHandler(BaseHandler):
    def get(self):
        self.render_template("sent.html")

class NewHandler(BaseHandler):
    def get(self):
        self.render_template("new.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/inbox', InboxHandler),
    webapp2.Route('/sent', SentHandler),
    webapp2.Route('/new', NewHandler),
 ], debug=True)
