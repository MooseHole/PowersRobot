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
                'Url: https://github.com/MooseHole/PowersRobot')
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
