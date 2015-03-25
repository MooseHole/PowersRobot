""""
Powers Robot Program

Tutorial program for PRAW:
See https://bitbucket.org/moosehole/powersrobot/
"""

import time
import praw

r = praw.Reddit('python:moosehole.powersrobot:v0.0.1 (by /u/Moose_Hole)'
                'Url: https://bitbucket.org/moosehole/powersrobot')
r.login()
already_done = []

prawWords = ['power']
while True:
    subreddit = r.get_subreddit('PowersRobot')
    for submission in subreddit.get_hot(limit=10):
        op_text = submission.selftext.lower()
        has_praw = any(string in op_text for string in prawWords)
        # Test if it contains a PRAW-related question
        if submission.id not in already_done and has_praw:
            msg = '[PRAW related thread](%s)' % submission.short_link
            r.send_message('Moose_Hole', 'PRAW Thread', msg)
            already_done.append(submission.id)
    time.sleep(1800)
