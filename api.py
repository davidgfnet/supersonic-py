
from xml import XML, XN
from model import getid
import random

callback_url = {}

def http(path):
	def http_decorator(fn):
		callback_url[path] = fn
		def wrapper(**kwargs):
			return fn()
		return wrapper
	return http_decorator

@http("/rest/getMusicFolders.view")
def list_folders(mlib, **kwargs):
	return XML([
		XN('musicFolders', {}, [
			XN('musicFolder', {
				'id': '1',
				'name': 'Music'
			}),
		])
	])

def list_songs(node, child, ids):
	return [ XN(node, {
		'id':x, 'title':child[x]._title, 'parent':child[x]._albumid,
		'album':child[x]._album, 'artist':child[x]._artist,
		'track':child[x]._tn, 'genre':child[x]._genre,
		'suffix':child[x]._ext, 'contentType':child[x]._fmt,
		'duration':child[x]._duration, 'year':child[x]._release,
		'bitRate': child[x]._bitrate, 'discNumber': child[x]._discn,
		'isDir':'false'
	}) for x in ids ]

@http("/rest/getMusicDirectory.view")
def list_directory(mlib, _id, **kwargs):

	artists = mlib.getArtists()
	if _id in artists.keys():
		n = artists[_id]
		child = mlib.getAlbums(_id)
		ids = sorted([ (child[x]._album, x) for x in child ])
		ids = [ x[1] for x in ids ]

		child = [ XN('child', {
			'id':x, 'title':child[x]._album, 'parent':_id, 'artist':n, 'isDir':'true'
		}) for x in ids ]

	albums = mlib.getAllAlbums()
	if _id in albums.keys():
		n = albums[_id]._album
		child = mlib.getSongs(_id)
		ids = sorted([ (int(child[x]._tn), x) for x in child ])
		ids = [ x[1] for x in ids ]

		child = list_songs('child', child, ids)

	return XML([
		XN('directory', {
			'id': _id,
			'name': n,
		},
		child
		)
	])

@http("/rest/getAlbumList.view")
def list_albums(mlib, **kwargs):
	if '_size' not in kwargs: size = 10
	else: size = int(kwargs['_size'])
	if '_offset' not in kwargs: offset = 10
	else: offset = int(kwargs['_offset'])

	child = mlib.getAllAlbums()
	ids = sorted([ (child[x]._album, x) for x in child ])
	ids = [ x[1] for x in ids ]

	child = [ XN('album', {
		'id':x, 'title':child[x]._album, 'artist':child[x]._artist, 'parent':child[x]._artistid, 'isDir':'true'
	}) for x in ids[offset:offset+size] ]

	return XML([
		XN('albumList', {},
		child
		)
	])

@http("/rest/getCoverArt.view")
def get_coverart(mlib, _id, **kwargs):
	return XML({
	})

@http("/rest/getLicense.view")
def get_license(mlib, **kwargs):
	return XML([
		XN('license', {
			'valid': 'true',
			'email': 'test@example.com',
			'key': 'ABC123DEF',
			'date': '2009-09-03T14:46:43',
		})
	])

@http("/rest/getIndexes.view")
def get_indexes(mlib, **kwargs):
	artists = mlib.getArtists()
	ids = sorted([ (artists[x], x) for x in artists ])
	ids = [ x[1] for x in ids ]

	artists = [ XN('artist', {'id':k, 'name':artists[k]})
		for k in ids ]
	return XML([
		XN('indexes', {
			'lastModified': str(mlib._modtime),
			'ignoredArticles':'The El La Los Las Le Les'
		},
		artists)
	])

@http("/rest/getRandomSongs.view")
def get_random(mlib, **kwargs):
	if '_size' not in kwargs: kwargs['_size'] = 10

	songs = mlib.getRandom(int(kwargs['_size']))
	return XML([
		XN('randomSongs', {},
		list_songs('song', songs, songs)
		)
	])

@http("/rest/getUser.view")
def get_user(mlib, **kwargs):
	return XML([
		XN('user', {
			'username': 'admin',
			'email': 'admin@example.com',
			'scrobblingEnabled': 'true',
			'adminRole': 'true',
			'settingsRole': 'true',
			'downloadRole': 'true',
			'uploadRole': 'false',
			'playlistRole': 'true',
			'coverArtRole': 'true',
			'commentRole': 'false',
			'podcastRole': 'false',
			'streamRole': 'false',
			'jukeboxRole': 'false',
			'shareRole': 'false',
		},
		[])
	])

@http("/rest/stream.view")
def get_stream(mlib, _id, **kwargs):
	f = mlib.getAllSongs()[_id]._file
	return open(f,"rb").read()


