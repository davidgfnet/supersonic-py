
def XN(name, attrs, data = []):
	eattrs = " ".join([ '%s="%s"' % (k, attrs[k]) for k in attrs if attrs[k] ])
	edata = "\n".join(data)

	if len(data) == 0:
		return "<%s %s />" % (name, eattrs)
	else:
		return "<%s %s>\n%s\n</%s>" % (name, eattrs, edata, name)

def XML(d):
	d = "\n".join(d)
	d = d.replace("&","&amp;").replace('"',"&quot;")
	return '<?xml version="1.0" encoding="UTF-8"?>\n' \
	'<subsonic-response status="ok" version="1.4.0">\n' + d + '\n</subsonic-response>'


