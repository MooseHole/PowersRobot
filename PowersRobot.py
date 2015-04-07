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
settingWords = {
		'[[unit '	: SetSettingUnit}

battleWords = {
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
setup = Setup()

def checkSub(sub):
	print ("Looking for battles at /r/" + sub)
	subreddit = r.get_subreddit(sub)
	for submission in subreddit.get_new():
		# Check to see if I replied yet
		skipSubmission = False;
		for comment in submission.comments:
			print ("Comment author is " + comment.author.name + " and I am " + os.environ['REDDIT_USER'])

			if comment.author.name == os.environ['REDDIT_USER']:
				print ("Skipping this submission because I replied!")
				skipSubmission = True
				break
		if skipSubmission:
			continue

		print ("Checking for battle")

		# Prepare Battle object for new battle
		battle.clear()
		orig_text = submission.selftext
		op_text = orig_text.lower()

		# Check each token
		for battleWord in battleWords.keys():
			position = 0
			end = 0

			# Look for the token for as many times as it appears in the message
			while True:
				position = op_text.find(battleWord, end)
				if position < 0:
					break # Token not found

				# Isolate the parameters
				begin = op_text.find(' ', position)
				end = op_text.find(']]', position)
				if end > begin:
					# Call the appropriate function for this token
					battleWords[battleWord](orig_text[begin:end].strip(), battle)

		# If this is a real battle
		if battle.isValid():
			# Process battle output
			submission.add_comment(str(battle))
#			r.send_message('Moose_Hole', 'A Battle!', str(battle))
#			print (str(battle))

		

# Main loop
while True:
	# Check own subreddit
	settingsPrefix = "Settings /r/"
	queryString = "subreddit:'" + os.environ['REDDIT_USER'] + "' title:'" + settingsPrefix + "*'"
	print(queryString)
	settings = r.search(queryString)

	for setting in settings:
		if setting.title.find(settingsPrefix) == 0:
			subToCheck = setting.title[len(settingsPrefix):].strip()
			// Subs don't have spaces
			if (subToCheck.find(" ") >= 0):
				continue

			setup.clear()
			orig_text = setting.selftext
			op_text = orig_text.lower()

			# Check each token
			for settingWord in settingWords.keys():
				# Look for the token for as many times as it appears in the message
				while True:
					position = op_text.find(settingWord, end)
					if position < 0:
						break # Token not found

					# Isolate the parameters
					begin = op_text.find(' ', position)
					end = op_text.find(']]', position)
					if end > begin:
						# Call the appropriate function for this token
						settingWords[settingWord](orig_text[begin:end].strip(), setup)

			checkSub(subToCheck)

	# Try again in this many seconds
	time.sleep(60)
