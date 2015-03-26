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
	def __init__(self, unit, combatValue, region=''):
		self.unit = unit
		self.region = region
		self.combatValue = combatValue
	def __str__(self):
		return self.name + " from " + self.region + " CV: " + self.combatValue

class Units:
	def __init__(self, unit, amount):
		self.unit = unit
		self.amount = amount
	def combatValue():
		return self.unit.combatValue * self.amount;
	def __str__(self):
		return str(self.amount) + " " + str(self.unit) + "  CV: " + str(self.combatValue())

class Commander:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name

class User:
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name

class Faction:
	def __init__(self, name):
		self.name = name
		self.users = []
		self.commanders = []
		self.units = []
	def addUser(self, user):
		self.users.append(user)
	def addCommander(self, commander):
		self.commanders.append(commander)
	def addUnits(self, units):
		self.units.append(units)
	def isFaction(self, factionName):
		return self.name == factionName
	def __str__(self):
		output = self.name
		for user in self.users:
			output += "\n\nUser: " + str(user)
		for commander in self.commanders:
			output += "\n\nCommander: " + str(commander)
		for units in self.units:
			output += "\n\nUnits: " + str(units)
		return output

class Terrain:
	def __init__(self, name=''):
		self.name = name
	def __str__(self):
		return self.name
	
class Battle:
	def __init__(self):
		self.clear()
	def addBattle(self, name):
		self.name = name
	def getFaction(self, factionName):
		# Check if existing
		for faction in self.factions:
			if faction.isFaction(factionName):
				return faction

		# Create new
		faction = Faction(factionName)
		self.factions.append(faction)
		return faction
	def addTerrain(self, terrain):
		self.terrain = terrain
	def isValid(self):
		print ("Battle checking valid for " + self.name + " length " + str(len(self.name)))
		return len(self.name) > 0
	def clear(self):
		self.name = ''
		self.factions = []
		self.terrain = Terrain()
	def __str__(self):
		output = self.name + " in " + str(self.terrain)
		for faction in self.factions:
			output += "\n\n" + str(faction)
		return output

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
		

powerWords = {	'[[battle '	: SetBattle, 
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
			position = op_text.find(powerWord)
			if position >= 0:
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
