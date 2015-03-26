
# A single unit
class Unit:
	def __init__(self, name, combatValue, region=''):
		self.name = name	# What the unit is called
		self.region = region	# Where the unit was created (affects combatValue)
		self.combatValue = combatValue # Strength of the unit

	def __str__(self):
		return self.name + " from " + self.region + " CV: " + self.combatValue

# A group of one type of Unit
class Units:
	def __init__(self, unit, amount):
		self.unit = unit	# A Unit object
		self.amount = amount	# The amount of the Unit in this group

	# The strength of the group
	def combatValue():
		return self.unit.combatValue * self.amount;

	def __str__(self):
		return str(self.amount) + " " + str(self.unit) + "  CV: " + str(self.combatValue())

# A named character
class Commander:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.name

# A human player
class User:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.name

# One "side" of the fight.  A faction fights against all other factions but not against itself.
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

	# True if this Faction has the same name
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

# The local environment.  Affects bonuses.
class Terrain:
	def __init__(self, name=''):
		self.name = name

	def __str__(self):
		return self.name

# Main holder of the battle
class Battle:
	def __init__(self):
		self.clear()

	def addBattle(self, name):
		self.name = name

	# Returns the named Faction.  Creates a new Faction if necessary.
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

	# True if Battle has enough info to process
	def isValid(self):
		print ("Battle checking valid for " + self.name + " length " + str(len(self.name)))
		return len(self.name) > 0

	# Resets the Battle
	def clear(self):
		self.name = ''
		self.factions = []
		self.terrain = Terrain()

	def __str__(self):
		output = self.name + " in " + str(self.terrain)
		for faction in self.factions:
			output += "\n\n" + str(faction)
		return output