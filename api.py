
from xml import XML, XN
from model import getid

callback_url = {}

def http(path):
	def http_decorator(fn):
		callback_url[path] = fn
		def wrapper(**kwargs):
			return fn()
		return wrapper
	return http_decorator

def list_dir(db, _id):
	artists = db.getArtists()
	if _id in artists.keys():
		return artists[_id], db.getAlbums(artists[_id])
	raise Exception("ID not found!")

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

@http("/rest/getMusicDirectory.view")
def list_directory(mlib, _id, **kwargs):

	artists = mlib.getArtists()
	if _id in artists.keys():
		n = artists[_id]
		child = mlib.getAlbums(artists[_id])
		ids = sorted([ (child[x], x) for x in child ])
		ids = [ x[1] for x in ids ]

		child = [ XN('child', {
			'id':x, 'title':child[x], 'parent':_id, 'artist':n, 'isDir':'true'
		}) for x in ids ]

	albums = mlib.getAllAlbums()
	if _id in albums.keys():
		n = albums[_id]
		child = mlib.getSongs(albums[_id])
		ids = sorted([ (int(child[x]._tn), x) for x in child ])
		ids = [ x[1] for x in ids ]

		child = [ XN('child', {
			'id':x, 'title':child[x]._title, 'parent':_id,
			'album':child[x]._album, 'artist':child[x]._artist,
			'track':child[x]._tn, 'genre':child[x]._genre,
			'suffix':child[x]._ext, 'contentType':child[x]._fmt,
			'duration':child[x]._duration, 'year':child[x]._release,
			'isDir':'false'
		}) for x in ids ]

	return XML([
		XN('directory', {
			'id': _id,
			'name': n,
		},
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
			'lastModified':'0',
			'ignoredArticles':'The El La Los Las Le Les'
		},
		artists)
	])

@http("/rest/getRandomSongs.view")
def get_indexes(mlib, **kwargs):
	return XML([])

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


