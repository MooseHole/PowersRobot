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