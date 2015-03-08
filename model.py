
import os
import hashlib

def fhash(fn):
	return hashlib.sha1(open(fn, "rb").read()).hexdigest()
def getid(o):
	return hashlib.sha1(o).hexdigest()[:8]

class Song():
	def __init__(self, title, artist, album, fn):
		self._id = getid(title+"_"+album+"_"+artist)
		self._title = title
		self._artist = artist
		self._album = album
		self._file = os.path.realpath(fn)
		self._hash = fhash(fn)

class Album():
	def __init__(self, artist, album):
		self._id = getid(album+"_"+artist)
		self._album = album
		self._artist = artist
		self._songs = []

	def addSong(self, s):
		for song in self._songs:
			if s._title == song._title:
				return

		self._songs.append(s)

class Artist():
	def __init__(self, artist):
		self._id = getid(artist)
		self._artist = artist
		self._albums = []

	def addSong(self, s):
		al = None
		for album in self._albums:
			if s._album == album._album:
				al = album
				break
		if not al:
			al = Album(s._artist, s._album)
			self._albums.append(al)

		al.addSong(s)

class MusicDir():
	def __init__(self):
		self._artists = []

	def addSong(self, s):
		ar = None
		for artist in self._artists:
			if s._artist == artist._artist:
				ar = artist
				break
		if not ar:
			ar = Artist(s._artist)
			self._artists.append(ar)

		ar.addSong(s)


