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
r = praw.Reddit('python:moosehole.powersrobo:v0.0.2 (by /u/Moose_Hole)'
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

def checkSub(sub):
	print ("Looking for battles at /r/" + sub)
	subreddit = r.get_subreddit(sub)
	for submission in subreddit.get_new():
		# Check to see if I replied yet
		skipSubmission = False;
		for comment in submission.comments:
			if comment.author == os.environ['REDDIT_USER']:
				skipSubmission = True
				break
		if skipSubmission:
			continue

		# Prepare Battle object for new battle
		battle.clear()
		orig_text = submission.selftext
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

		# If this is a real battle
		if battle.isValid():
			# Process battle output
			submission.reply(str(battle))
#			r.send_message('Moose_Hole', 'A Battle!', str(battle))
#			print (str(battle))

		

# Main loop
while True:
	# Check own subreddit
	settingsPrefix = "Settings /r/"
	queryString = "subreddit:'" + os.environ['REDDIT_USER'] + "' title:'" + settingsPrefix + "*'"
	print(queryString)
	unread = r.search(queryString)

	for setting in unread:
		if setting.title.find(settingsPrefix) == 0:
			subToCheck = setting.title[len(settingsPrefix):]
			checkSub(subToCheck)

	# Try again in this many seconds
	time.sleep(60)
