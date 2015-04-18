
import os, sys, time
import ogg.vorbis, eyed3
from model import Song, MusicDir

def add_song(mlib, s):
	mlib.addSong(s)

def file_to_db(mlib, fn):
	if fn.lower().endswith("ogg"):
		vf = ogg.vorbis.VorbisFile(fn)
		d = vf.comment().as_dict()
		if 'GENRE' not in d:
			d['GENRE'] = [""]
		if 'DISCNUMBER' not in d:
			d['DISCNUMBER'] = ["1"]
		s = Song(d['TITLE'][0], d['ARTIST'][0], d['ALBUM'][0], d['TRACKNUMBER'][0], d['GENRE'][0],
			"ogg", "audio/ogg", int(vf.time_total(0)), d['DATE'][0].split(":")[0].split("-")[0], d['DISCNUMBER'][0], vf.info().bitrate_nominal/1000, None, fn)
		add_song(mlib, s)
	elif fn.lower().endswith("mp3"):
		m3 = eyed3.load(fn)
		if m3.tag.genre is None or m3.tag.genre.id is None:
			g = ""
		else:
			g = eyed3.id3.ID3_GENRES[m3.tag.genre.id]
		y = m3.tag.getBestDate()
		if y is None: y = 0
		else: y = y.year
		if m3.tag.disc_num[0]:
			discn = m3.tag.disc_num[0]
		else:
			discn = 1

		cover = None
		if len(m3.tag.images) > 0:
			cover = m3.tag.images[0].image_data

		aartist = m3.tag.album_artist
		if aartist is None: aartist = m3.tag.artist

		s = Song(m3.tag.title, aartist, m3.tag.album, m3.tag.track_num[0], 
			g, "mp3", "audio/mpeg", m3.info.time_secs, y, discn, m3.info.bit_rate[1], cover, fn)
		add_song(mlib, s)

def scan_folder(mlib, path):
	for elem in os.listdir(path):
		nf = os.path.join(path, elem)
		if os.path.isfile(nf):
			file_to_db(mlib, os.path.join(path, elem))
		elif os.path.isdir(nf):
			scan_folder(mlib, os.path.join(path, elem))

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

mlib = MusicDir(int(time.time()*1000), options.db)
scan_folder(mlib, options.indir)


