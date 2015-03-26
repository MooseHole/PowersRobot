from battleClasses import *

# Input: Parameters after the command token
# Output: A Faction object and the rest of the parameters
def GetFactionFromText(text, battle):
	space = text.find(' ')
	faction = battle.getFaction(text[:space])
	return [faction, text[space:]]

# Set up the Battle name
def SetBattle(text, battle):
	battle.addBattle(text)

# Set up the Terrain of the Battle
def SetTerrain(text, battle):
	battle.addTerrain(Terrain(text))

# Set a Faction of the Battle
def SetFaction(text, battle):
	battle.getFaction(text)

# Set a User of the Battle in the correct Faction
def SetUser(text, battle):
	factionSplit = GetFactionFromText(text, battle)
	factionSplit[0].addUser(factionSplit[1])
	
# Set a Commander of the Battle in the correct Faction
def SetCommander(text, battle):
	factionSplit = GetFactionFromText(text, battle)
	factionSplit[0].addCommander(factionSplit[1])
		
# Set a Units of the Battle in the correct Faction
def SetUnits(text, battle):
	name = ''
	cv = 0
	region = ''
	amount = 0

	factionSplit = GetFactionFromText(text, battle)
	faction = factionSplit[0]
	unitsParameters = factionSplit[1];
	space = unitsParameters.find(' ')
	amount = unitsParameters[:space]
	unitsParameters = unitsParameters[space:]
	space = unitsParameters.find(' ')

	if space < 0:
		region = unitsParameters
	else:
		region = unitsParameters[:space]
		name = unitsParameters[space:]

	if region.isdigit():
		cv = region
		region = ''

	unit = Unit(name, cv, region)
	units = Units(unit, amount)
	faction.addUnits(units)

# Process a confirmation
def DoConfirm(text, battle):
	print ("Found a Confirm: " + text)
	return

# Process a deletion
def DoDelete(text, battle):
	print ("Found a Delete: " + text)
	return