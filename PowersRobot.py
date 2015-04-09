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
import datetime
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


# Main loop
while True:
	settings = getSettings("Settings /r/")
	for setting in settings:
		subreddit = getSetupSubreddit(setting)
		if subreddit is None:
			continue

		setup = parseSetup(setting.selftext)

		print ("Looking for battles at /r/" + subreddit.name)
		checkSubForNewBattles(subreddit, setup, conn)

	postBattleSetups(conn)

	# Try again in this many seconds
	time.sleep(60)

conn.close()