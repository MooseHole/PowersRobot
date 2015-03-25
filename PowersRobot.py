""""
Powers Robot Program

Battle program for Powers
See https://github.com/MooseHole/PowersRobot
"""

import os
import time
import praw
import requests

class Unit:
	name = ''
	region = ''
	combatValue = ''

class Units:
	def __init__(self, unit, amount):
		self.unit = unit
		self.amount = amount
	def combatValue():
		return self.unit.combatValue * self.amount;

class Commander:
	def __init__(self, name):
		self.name = name

class User:
	def __init__(self, name):
		self.name = name

class Faction:
	users = []
	commanders = []
	units = []
	def __init__(self, name):
		self.name = name

class Environment:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name
	
class Battle:
	environment = ''
	factions = []
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name + " in " + environment + "\n\n"

r = praw.Reddit('python:moosehole.powersrobot:v0.0.1 (by /u/Moose_Hole)'
                'Url: https://github.com/MooseHole/PowersRobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

powerWords = ['[[battle '	: SetBattle, 
	      '[[environment'	: SetEnvironment,
	      '[[faction '	: SetFaction,
	      '[[commander '	: SetCommander,
	      '[[units '	: SetUnits,
	      '[[confirm'	: DoConfirm,
	      '[[delete'	: DoDelete]
r.send_message('Moose_Hole', 'HAY', 'SCRAEW YAEW')

battle = ''

def SetBattle(text):
	battle = Battle(text)

def SetEnvironment(text):
	if battle != '':
		battle.environment = Environment(text);

def SetFaction(text):
	if battle != '':
		battle.faction.append(Faction(text));

def SetCommander(text):
	return
		
def SetUnits(text):
	return
		
def DoConfirm(text):
	return
		
def DoDelete(text):
	return
		

while True:
	unread = r.get_unread(limit=None)
	for msg in unread:
		battle = ''
		op_text = msg.body.lower()
		for powerWord in powerWords.keys():
			position = op_text.find(powerWord)
			if position >= 0:
			        begin = text.find(' ', position)
				end = text.find(']]', position)
				if end > begin:
					powerWords[powerWord](op_text[begin:end])
		if battle != '':
			r.send_message('Moose_Hole', 'A Battle!', battle)
			msg.mark_as_read()
	time.sleep(30)
