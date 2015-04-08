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

cursor = conn.cursor()

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

def checkSubForNewBattles(sub):
	print ("Looking for battles at /r/" + sub)
	subreddit = r.get_subreddit(sub)
	for submission in subreddit.get_new(limit=100):
		# Check to see if I replied yet
		skipSubmission = False;

		# Does the database already have this battle?		
		cursor.execute("SELECT \"SubmissionID\" FROM \"Battles\" WHERE \"SubmissionID\" = '" + submission.id + "'")
		if cursor.rowcount > 0:
			continue

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
		elements = ''

		# Check each token
		for battleWord in battleWords.keys():
			position = 0

			# Look for the token for as many times as it appears in the message
			while True:
				position = op_text.find(battleWord, position)
				if position < 0:
					break # Token not found

				# Isolate the parameters
				element = orig_text[position:]
				end = element.find(endTag)
				element = element[:end+len(endTag)].strip()
				beginParameters = element.find(' ', position)
				if beginParameters > 0 and end > beginParameters:
					elements += element
					parameters = element[beginParameters:end].strip()
					# Call the appropriate function for this token
					battleWords[battleWord](parameters, battle)
				position = position + 1

		# If this is a real battle
		if battle.isValid():
			# Process battle output
			submission.add_comment(str(battle))
			battleTableId = ''
			for comment in submission.comments:
				if comment.author.name == os.environ['REDDIT_USER'] and comment.body == str(battle):
					battleTableId = comment.id
					break

			print (elements)
			print (battleTableId)
			print (submission.id)
#			cursor.execute("INSERT INTO \"Battles\
 (\"SubmissionID\", \"BattleTableID\", \"BattleContent\") VALUES (%s, %s)""", (submission.id, battleTableId, elements))
#			conn.commit()

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
					if beginParameters > 0 and end > beginParameters:
						parameters = element[beginParameters:end].strip()
						# Call the appropriate function for this token
						settingWords[settingWord](parameters, setup)
					position = position + 1

			checkSubForNewBattles(subToCheck)

	# Try again in this many seconds
	time.sleep(60)

cursor.close()
con.close()