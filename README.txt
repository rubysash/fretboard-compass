
CHORD DUMPER

Summary: 

Takes a chord database, in xlsx and converts to various charts
scales, progressions, etc.

The idea is to show exactly what to play for both scales and progressions
for my favorite progressions (and all progressions), with a quick reference
for people like me who might know how to put fingers on a guitar, but
not know what to play together, or understand much about music theory, but
if given some chords and scales can have fun playing it.


Input Data:

requires 3 tabs on the input file:  chords, favs, scales.

chords format:
    VERIFIED	KEY	VARIANT	NAME	POSITION	DOTS
    1	X02220	0	A	1	[320,130,2],[340,130,1],[360,130,3]
    1	X03211	0	A	5	[320,160,4],[340,130,2],[360,100,1],[380,100,1]

favs format:
    VERIFIED	KEY	VARIANT	NAME	POSITION	DOTS
    1	I II III iii D	0	D	1	D E C# F#m
    1	I iii IV V Ballads C	0	C	1	C Em F G


scales format example:
    VERIFIED	KEY	VARIANT	NAME	POSITION	DOTS
    1	A	0	A	1	[0,2,4],[100,2,4],[0,2,4],[1,102,4],[0,2,3],[0,2,4]
    1	B	0	B	1	[0,2,4],[1,102,4],[1,2,4],[1,3,104],[100,2,4],[0,2,4]


Running the program:

Examples of how to run the program depending on what you want to generate:

(chorddumper) u@h:~/chorddumper$ python3 chorddump.7.py -i chords7.xlsx -f
  Writing Favs:  7.favs.html
(chorddumper) u@h:~/chorddumper$ python3 chorddump.7.py -i chords7.xlsx -s
Writing Scales:  7.scales.html
(chorddumper) u@h:~/chorddumper$ python3 chorddump.7.py -i chords7.xlsx -c
Writing Chords:  7.all.html
(chorddumper) u@h:~/chorddumper$ python3 chorddump.7.py -i chords7.xlsx -a
  Writing Favs:  7.favs.html
Writing Chords:  7.all.html
Writing Scales:  7.scales.html

Features:
    Prefers first position in database in the case of duplicate chords or voicings
    If "Verified" is 0, it will highlight the chord/scale in red so you can verify it
    If Verified is 1, it will print normal.
    Dumps list of scales in Database (Currently just Major and Minor)
    Dumps all chords in DB (Currently 102)
    Dumps all favorite progressions (34 currently), combining scales with progressions
    Attempts intelligent page breaks for easy printing

Todo:
    DONE: Move svg and html into container folders instead of in the root
    ONGOING: Add more data to the chord database (full scales, full progressions, etc)
    Automate dot position base don key, (not sure how to show finger placements though)
    Update database instead of using the lame offset hack
    DONE: Does not allow duplicate fingerings of different chords (D#m/Eb,Abm/G#m etc)
    DONE: Cannot print favorites until you first print out scales and chords, detect or force

Tested on:
    Debian 12
    Windows 10
