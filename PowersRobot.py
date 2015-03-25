""""
Powers Robot Program

Battle program for Powers
See https://bitbucket.org/moosehole/powersrobot/
"""

import os
import time
import praw
import requests

r = praw.Reddit('python:moosehole.powersrobot:v0.0.1 (by /u/Moose_Hole)'
                'Url: https://bitbucket.org/moosehole/powersrobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

powerWords = ['[[Battle ', '[[Environment', '[[Faction ', '[[Commander ', '[[Units ', '[[Confirm' ,'[[Delete']
while True:
	unread = r.get_unread(limit=None)
	for msg in unread:
		op_text = msg.body.lower()
		has_power = any(string in op_text for string in powerWords)
		if (has_power):
			outmsg = '[Powers related comment](%s)' % msg.body
			r.send_message('Moose_Hole', 'Powers Message', outmsg)
			msg.mark_as_read()
	time.sleep(1800)


"""
Parameters:
[[Battle BattleName]]
[[Faction FactionName /u/UserName]]
[[Commander FactionName CommanderName]]
[[Units FactionName Amount Kingdom|Type|CV]]
/u/BotName

Example:
[[Battle Test fight!]]
[[Environment Riverlands]]
[[Faction Good /u/Moose_Hole]]
[[Faction Ebil /u/moosehole]]
[[Commander Bucket Good]]
[[Commander Wignit Good]]
[[Commander Reaper Ebil]]
[[Units Good 1000 Riverlands]]
[[Units Ebil 1000 Light Infantry]]
[[Units Ebil 20 Ranged Infantry]]
[[Units Ebil 10 Heavy Cavalry]]
[[Units Ebil 5 100]]
/u/PowersRobot

Output:
Test fight! is ready to begin in Riverlands!
* Good:
    * Users:
        * /u/Moose_Hole
    * Commanders:
        * Bucket
        * Wignit
    * Units:  Total Combat Value 1705
        * 1000 Riverlands (CV 1705)
            * 400 Light Infantry (CV 400)
            * 100 Heavy Infantry (CV 200)
            * 250 Ranged Infantry (CV 475)
            * 150 Light Cavalry (CV 330)
            * 100 Heavy Cavalry (CV 300)
* Ebil
    * Users:
        * /u/moosehole
    * Commanders:
        * Reaper
    * Units: Total Combat Value 1568
        * 1000 Light Infantry (CV 1000)
        * 20 Ranged Infantry (CV 38)
        * 10 Heavy Cavalry (CV 30)
        * 5 Combat Value 100 (CV 500)

To begin battle:
/u/Moose_Hole respond [[Confirm]]
/u/moosehole respond [[Confirm]]
--OR--
moderator respond [[Confirm override]]

To delete battle:
moderator respond [[Delete]]
"""