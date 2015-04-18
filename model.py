
import os, hashlib, random, shelve
from PIL import Image
from StringIO import StringIO

try:
   import cPickle as pickle
except:
   import pickle 

def fhash(fn):
	return hashlib.sha1(open(fn, "rb").read()).hexdigest()
def getid(o):
	return hashlib.sha1(o.encode('utf-8')).hexdigest()[:8]

class AlbumCovers():
	def __init__(self, coverfile):
		self._covers = shelve.open(coverfile)
	def __del__(self):
		self._covers.close()
	def addCover(self,albumid,cover):
		self._covers[albumid.encode('utf8')] = cover
	def hasCover(self,albumid):
		return albumid.encode('utf8') in self._covers
	def getCover(self,albumid, size = None):
		k = albumid.encode('utf8')
		if k in self._covers:
			r = self._covers[k]
		else:
			r = ""
		self._covers.sync()

		try:
			if size:
				im = Image.open(StringIO(r))
				bigsize = max(im.size)
				if bigsize > size:
					ratio = size/float(bigsize)
					news = (int(im.size[0]*ratio), int(im.size[1]*ratio))
					output = StringIO()
					im = im.resize(news, Image.ANTIALIAS)
					im.save(output, format="JPEG")
					r = output.getvalue()
					output.close()
		except:
			# Just return whatever we got
			pass

		return r

class Song():
	def __init__(self, title, artist, album, tn, genre, ext, fmt, dur, rel, discn, bitr, cover, fn):
		self._id = getid(title+"_"+album+"_"+artist)
		self._albumid = getid(album+"_"+artist)
		self._artistid = getid(artist)
		self._title = title
		self._artist = artist
		self._album = album
		self._tn = tn
		self._cover = cover
		self._hascover = cover is not None
		self._ext = ext
		self._fmt = fmt
		self._duration = dur
		self._genre = genre
		self._release = rel
		self._bitrate = bitr
		self._discn = discn
		self._file = os.path.realpath(fn)
	def __str__(self):
		return "%s: %s - %s (%s)" % (self._id, self._title, self._album, self._artist)

class Album():
	def __init__(self, artist, album):
		self._id = getid(album+"_"+artist)
		self._artistid = getid(artist)
		self._album = album
		self._artist = artist
		self._songs = []

	def addSong(self, s):
		for song in self._songs:
			if s._title == song._title:
				return

		self._songs.append(s)

	def getSongs(self):
		return { a._id:a for a in self._songs }

	def getAllSongs(self):
		r = {}
		for song in self._songs:
			r.update({ s._id:s for s in self._songs })
		return r

	def getRandom(self):
		s = random.choice(self._songs)
		return { s._id:s }

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

	def getAlbums(self):
		return { a._id:a for a in self._albums }

	def getSongs(self, albid):
		for album in self._albums:
			if albid == album._id:
				return album.getSongs()
		return {}

	def getAllSongs(self):
		r = {}
		for album in self._albums:
			r.update( album.getAllSongs() )
		return r

	def getRandom(self):
		return random.choice(self._albums).getRandom()

class MusicDir():
	def __init__(self, modtime, outfile):
		self._artists = []
		self._outfile = outfile
		self._modtime = modtime
		if outfile:
			self._coverdb = AlbumCovers(outfile+".art")

	@staticmethod
	def load(f):
		r = pickle.load(open(f,"rb"))
		r._coverdb = AlbumCovers(f+".art")
		return r

	def __del__(self):
		self._coverdb = None
		if self._outfile:
			o = self._outfile
			self._outfile = None
			open(o, "wb").write(pickle.dumps(self))

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

		# Save cover, and remove art
		if s._cover:
			self._coverdb.addCover(s._albumid, s._cover)
			s._cover = None

	def getArtists(self):
		return { a._id:a._artist for a in self._artists }

	def getAllAlbums(self):
		r = {}
		for artist in self._artists:
			r.update( artist.getAlbums() )
		return r

	def getAllSongs(self):
		r = {}
		for artist in self._artists:
			r.update( artist.getAllSongs() )
		return r

	def getAlbums(self, art_id):
		for artist in self._artists:
			if art_id == artist._id:
				return artist.getAlbums()

	def getSongs(self, albid):
		r = {}
		for artist in self._artists:
			r.update(artist.getSongs(albid))
		return r

	def getRandom(self, n):
		r = {}
		for i in range(n):
			r.update(random.choice(self._artists).getRandom())
		return r

	def getCover(self,albumid, size = None):
		return self._coverdb.getCover(albumid, size)
	def hasCover(self,albumid):
		return self._coverdb.hasCover(albumid)


