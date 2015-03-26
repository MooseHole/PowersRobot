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

r = praw.Reddit('python:moosehole.powersrobot:v0.0.2 (by /u/Moose_Hole)'
                'Url: https://github.com/MooseHole/PowersRobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

def GetFactionFromText(text, battle):
	space = text.find(' ')
	faction = battle.getFaction(text[:space])
	return [faction, text[space:]]
	
def SetBattle(text, battle):
	print ("Found a Battle: " + text)
	battle.addBattle(text)
	print ("This is the battle text: " + str(battle))

def SetTerrain(text, battle):
	print ("Found a Terrain: " + text)
	if battle != '':
		battle.addTerrain(Terrain(text))

def SetFaction(text, battle):
	print ("Found a Faction: " + text)
	if battle != '':
		battle.getFaction(text)

def SetUser(text, battle):
	print ("Found a User: " + text)
	factionSplit = GetFactionFromText(text, battle)
	factionSplit[0].addUser(factionSplit[1])
	
def SetCommander(text, battle):
	print ("Found a Commander: " + text)
	factionSplit = GetFactionFromText(text, battle)
	factionSplit[0].addCommander(factionSplit[1])
		
def SetUnits(text, battle):
	print ("Found a Units: " + text)
	return

def DoConfirm(text, battle):
	print ("Found a Confirm: " + text)
	return
		
def DoDelete(text, battle):
	print ("Found a Delete: " + text)
	return
		

powerWords = {
		'[[battle '	: SetBattle, 
		'[[terrain'	: SetTerrain,
		'[[faction '	: SetFaction,
		'[[user '	: SetUser,
		'[[commander '	: SetCommander,
		'[[units '	: SetUnits,
		'[[confirm'	: DoConfirm,
		'[[delete'	: DoDelete}

battle = Battle()

while True:
	unread = r.get_unread(limit=None)
	for msg in unread:
		print ("vvvv")
		battle.clear()
		op_text = msg.body.lower()
		for powerWord in powerWords.keys():
			position = 0
			end = 0
			while True:
				position = op_text.find(powerWord, end)
				if position < 0:
					break
				begin = op_text.find(' ', position)
				end = op_text.find(']]', position)
				if end > begin:
					powerWords[powerWord](op_text[begin:end].strip(), battle)
		print ("<<>>")
		if battle.isValid():
			r.send_message('Moose_Hole', 'A Battle!', str(battle))

		msg.mark_as_read()
		print ("^^^^")

	time.sleep(30)
