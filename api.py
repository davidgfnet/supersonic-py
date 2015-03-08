
def list_dir(_id):
	if _id in db:
		o = db[_id]
		if isinstance(o, Artist):
			return o._title, o
		elif isinstance(o, Album):
			return o._title, o
		elif isinstance(o, Song):
			return o._title, o
	else:
		raise Exception("ID not found!")

@http("/rest/getMusicFolders.view")
def list_folders():
	return XML(
		'musicFolders': {
			'musicFolder': [ {
				'id': '1',
				'name': 'Music'
			} ]
		}
	)

@http("/rest/getMusicDirectory.view")
def list_directory(_id):
	n, res_list = list_child(_id)

	return XML(
		'directory': {
			'id': _id,
			'name': n,
			'child': res_list
		}
	)

