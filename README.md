# supersonic
Music server implementing the Subsonic API

Warning!
--------

This project is deprecated and no longer maintained! Please check other projects such as:

 * https://github.com/davidgfnet/supersonic-cpp
 * https://github.com/sentriz/gonic

What
----

supersonic is a small python implementation of a music server. It implements the SubSonic API (http://www.subsonic.org/pages/api.jsp) which is used by many clients (desktop, phone...) and works on top of the HTTP protocol. It uses web.py as server and depends on python imaging library for cover art and ogg.vorbis and eyed3 libraries for music tag reading.

Why
---

There are many music servers out there (even an official one) but most of them are big in terms of memory and CPU consumption (Java!). As I wanted to run my server on a small box (small ARM SoC) most of the software wasn't suitable, or just ran too slow.

How
---

Use scan.py to create a database. It will generate two files: music index (artists albums and songs) and a cover art database. Building may take some time, since covers are preprocessed to create thumbnails (so clients can request smaller thumbnails at no CPU cost for the server).

Use server.py to start the server. Set DATABASE in your envirornment to point to your database file. Argv[1] can be used to specify the listening port for the server.

There is no username & password! This is still WIP.
