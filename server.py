
import os, sys
from model import Song

try:
   import cPickle as pickle
except:
   import pickle

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--database", dest="db",
                  help="Database file to serve", metavar="DB")

(options, args) = parser.parse_args()

if not options.db:
	print "Specify an input database!\n"
	sys.exit(0)

db = load(open(options.db,"rb"))



