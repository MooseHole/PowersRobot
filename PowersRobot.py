""""
Powers Robot Program

Battle program for Powers
See https://github.com/MooseHole/PowersRobot
"""

import os
import time
import praw
import requests
import psycopg2
import urlparse
from battleClasses import *
from battleHelpers import *

# Open DB
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["HEROKU_POSTGRESQL_AMBER_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

# Login
r = praw.Reddit('python:moosehole.powersrobo:v0.0.2 (by /u/Moose_Hole)'
                'Url: https://github.com/MooseHole/PowersRobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

# Look for these tokens
beginTag = "[["
endTag = "]]"

settingWords = {
		beginTag + "unit "	: SetSettingUnit}

battleWords = {
		beginTag + "battle "	: SetBattle, 
		beginTag + "terrain"	: SetTerrain,
		beginTag + "faction "	: SetFaction,
		beginTag + "user "	: SetUser,
		beginTag + "commander "	: SetCommander,
		beginTag + "units "	: SetUnits,
		beginTag + "confirm"	: DoConfirm,
		beginTag + "delete"	: DoDelete}

# Set up a single Battle object to work on
setup = Setup()
battle = Battle(setup)

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
				end = op_text.find(endTag, position)
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
			# Subs don't have spaces
			if (subToCheck.find(" ") >= 0):
				continue

			setup.clear()
			orig_text = setting.selftext
			op_text = orig_text.lower()

			# Check each token
			for settingWord in settingWords.keys():
				position = 0

				# Look for the token for as many times as it appears in the message
				while True:
					position = op_text.find(settingWord, position)
					if position < 0:
						break # Token not found

					# Isolate the parameters
					element = orig_text[position:]
					end = element.find(endTag)
					element = element[:end+len(endTag)].strip()
					beginParameters = element.find(' ', position)
					print ("element: " + element)
					print ("position: " + position)
					print ("beginParameters: " + str(beginParameters))
					print ("end: " + str(end))
					if beginParameters > 0 and end > beginParameters:
						parameters = element[beginParameters:end].strip()
						print ("parameters: " + parameters)
						# Call the appropriate function for this token
						settingWords[settingWord](parameters, setup)
					position = position + 1

			checkSub(subToCheck)

	# Try again in this many seconds
	time.sleep(60)
