from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    tekst = ndb.StringProperty()
    uporabnik = ndb.StringProperty()
    cas = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)