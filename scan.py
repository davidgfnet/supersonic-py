
import os, sys
import ogg.vorbis, eyed3
from model import Song

try:
   import cPickle as pickle
except:
   import pickle

def add_song(db, s):
	if s._artist not in db:
		db[s._artist] = {}
	if s._album not in db[s._artist]:
		db[s._artist][s._album] = []

	db[s._artist][s._album].append(s)

def file_to_db(db, fn):
	if fn.lower().endswith("ogg"):
		vf = ogg.vorbis.VorbisFile(fn)
		d = vf.comment().as_dict()
		s = Song(d['TITLE'][0], d['ARTIST'][0], d['ALBUM'][0], d['TRACKNUMBER'][0], d['GENRE'][0],
			"ogg", "audio/ogg", int(vf.time_total(0)), d['DATE'][0].split(":")[0].split("-")[0], fn)
		add_song(db, s)
	elif fn.lower().endswith("mp3"):
		m3 = eyed3.load(fn)
		g = "" if m3.tag.genre.id is None else eyed3.id3.ID3_GENRES[m3.tag.genre.id]
		s = Song(m3.tag.title, m3.tag.artist, m3.tag.album, m3.tag.track_num[0], 
			g, "mp3", "audio/mpeg", m3.info.time_secs, m3.tag.getBestDate().year, fn)
		add_song(db, s)

def scan_folder(db, path):
	for elem in os.listdir(path):
		nf = os.path.join(path, elem)
		if os.path.isfile(nf):
			file_to_db(db, os.path.join(path, elem))
		elif os.path.isdir(nf):
			scan_folder(db, os.path.join(path, elem))

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d", "--dir", dest="indir",
                  help="Music library path", metavar="DIR")
parser.add_option("-f", "--database", dest="db",
                  help="Database file to output", metavar="DB")

(options, args) = parser.parse_args()

if not options.indir:
	print "Specify an input dir!\n"
	sys.exit(0)
if not options.db:
	options.db = "out.db"

db = {}
scan_folder(db, options.indir)

open(options.db, "wb").write(pickle.dumps(db))


