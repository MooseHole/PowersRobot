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