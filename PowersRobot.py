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
	def __init__(self, name=''):
		self.name = name
	def __str__(self):
		return self.name
	
class Battle:
	def __init__(self, name=''):
		self.name = name
		self.factions = []
		self.environment = Environment()
	def addFaction(self, faction):
		if faction not in self.factions:
			self.factions.append(faction)
	def addEnvironment(self, environment):
		self.environment = environment
	def isValid(self):
		print ("Battle checking valid for " + self.name + " length " + str(len(self.name)))
		return len(self.name) > 0
	def __str__(self):
		return self.name + " in " + str(self.environment) + "\n\n"

r = praw.Reddit('python:moosehole.powersrobot:v0.0.1 (by /u/Moose_Hole)'
                'Url: https://github.com/MooseHole/PowersRobot')
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

def SetBattle(text, battle):
	print ("Found a Battle: " + text)
	battle = Battle(text)
	print ("This is the battle text: " + str(battle))

def SetEnvironment(text, battle):
	print ("Found an Environment: " + text)
	if battle != '':
		battle.addEnvironment(Environment(text))

def SetFaction(text, battle):
	print ("Found a Faction: " + text)
	if battle != '':
		battle.addFaction(Faction(text))

def SetCommander(text, battle):
	print ("Found a Commander: " + text)
	return
		
def SetUnits(text, battle):
	print ("Found a Units: " + text)
	return
		
def DoConfirm(text, battle):
	print ("Found a Confirm: " + text)
	return
		
def DoDelete(text, battle):
	print ("Found a Delete: " + text)
	return
		

powerWords = {	'[[battle '	: SetBattle, 
		'[[environment'	: SetEnvironment,
		'[[faction '	: SetFaction,
		'[[commander '	: SetCommander,
		'[[units '	: SetUnits,
		'[[confirm'	: DoConfirm,
		'[[delete'	: DoDelete}

battle = Battle()

while True:
	unread = r.get_unread(limit=None)
	for msg in unread:
		print ("vvvv")
		battle = Battle()
		op_text = msg.body.lower()
		for powerWord in powerWords.keys():
			position = op_text.find(powerWord)
			if position >= 0:
				begin = op_text.find(' ', position)
				end = op_text.find(']]', position)
				print ("Found " + powerWord + " at " + str(position) + " Begin " + str(begin) + " End: " + str(end))
				if end > begin:
					powerWords[powerWord](op_text[begin:end], battle)
		print ("<<>>")
		if battle.isValid():
			r.send_message('Moose_Hole', 'A Battle!', str(battle))
			msg.mark_as_read()
		print ("^^^^")

	time.sleep(30)
