""""
Powers Robot Program

Battle program for Powers
See https://github.com/MooseHole/PowersRobot
"""

import os
import time
import praw
import requests
from battleClasses import *
from battleHelpers import *

# Login
r = praw.Reddit('python:moosehole.powersrobot:v0.0.2 (by /u/Moose_Hole)'
                'Url: https://github.com/MooseHole/PowersRobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

# Look for these tokens
powerWords = {
		'[[battle '	: SetBattle, 
		'[[terrain'	: SetTerrain,
		'[[faction '	: SetFaction,
		'[[user '	: SetUser,
		'[[commander '	: SetCommander,
		'[[units '	: SetUnits,
		'[[confirm'	: DoConfirm,
		'[[delete'	: DoDelete}

# Set up a single Battle object to work on
battle = Battle()

# Main loop
while True:
	# Check own subreddit
	unread = r.search(subreddit:"'" + os.environ['REDDIT_USER'] + "'", title:'/r/* Settings')

	# Check unread messages
#	unread = r.get_unread(limit=None)
	for msg in unread:
		print ("vvvv")

		# Prepare Battle object for new battle
		battle.clear()
		orig_text = msg.body
		op_text = orig_text.lower()

		# Check each token
		for powerWord in powerWords.keys():
			position = 0
			end = 0

			# Look for the token for as many times as it appears in the message
			while True:
				position = op_text.find(powerWord, end)
				if position < 0:
					break # Token not found

				# Isolate the parameters
				begin = op_text.find(' ', position)
				end = op_text.find(']]', position)
				if end > begin:
					# Call the appropriate function for this token
					powerWords[powerWord](orig_text[begin:end].strip(), battle)

		print ("<<>>")

		# If this is a real battle
		if battle.isValid():
			# Process battle output
			r.send_message('Moose_Hole', 'A Battle!', str(battle))
			print (str(battle))

		# Don't read this message again
		msg.mark_as_read()
		print ("^^^^")

	# Try again in this many seconds
	time.sleep(30)
