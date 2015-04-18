
# Using web.py backend

import os, sys, web
from api import callback_url
from model import Song, MusicDir

try:
   import cPickle as pickle
except:
   import pickle

if not 'DATABASE' in os.environ:
	print "Specify an input database through the DATABASE variable!\n"
	sys.exit(0)

dbname = os.environ['DATABASE']
dbtime = int(os.path.getmtime(dbname)*1000)
db = pickle.load(open(dbname,"rb"))
mlib = MusicDir(dbtime)
for artist in db:
	for album in db[artist]:
		for song in db[artist][album]:
			mlib.addSong(song)

class httpindex:
	def req(self, req, data):
		return callback_url[req](mlib, **data)

	def POST(self, req):
		args = { x:"" for x in ["id"] }
		data = web.input(**args)
		args = { "_"+x:data[x] for x in data }

		return self.req(req,args)

# Server
if __name__ == "__main__":
	urls = ("(.*)", "httpindex")
	app = web.application(urls, globals())
	app.run()


