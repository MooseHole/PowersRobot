
# A single unit
class Unit:
	def __init__(self, name, combatValue, region=''):
		self.name = name	# What the unit is called
		self.region = region	# Where the unit was created (affects combatValue)
		self.combatValue = int(combatValue) # Strength of the unit

	def getName(self):
		return self.name

	def getRegion(self):
		return self.region

	def getCombatValue(self):
		return self.combatValue

	def __str__(self):
		return self.name + " from " + self.region + " CV: " + self.combatValue

# A group of one type of Unit
class Units:
	def __init__(self, unit, amount):
		self.unit = unit	# A Unit object
		self.amount = amount	# The amount of the Unit in this group

	# The strength of the group
	def getCombatValue(self):
		return self.unit.getCombatValue() * self.amount

	def getTableRow(self):
		return "|" + self.amount + "|" + self.unit.getRegion() + "|" + self.unit.getName() + "|" + str(self.unit.getCombatValue())

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

	def getName(self):
		return self.name

	# The strength of the entire Faction
	def getCombatValue(self):
		cv = 0

		for units in self.units:
			cv += units.getCombatValue()

		return cv

	def getUsers(self):
		return self.users

	def getCommanders(self):
		return self.commanders

	def getUnits(self):
		return self.units

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
		output = self.name + " in " + str(self.terrain) + "\n\n"
		numFactions = len(self.factions)
		numColumns = 1 + (numFactions * 4)

		output += "|**Factions**"
		for faction in self.factions:
			output += "|**" + faction.getName() + "**|**CV: " + str(faction.getCombatValue()) + "**||"
		output += "\n"

		# Column alignment
		for i in range (0, numColumns):
			output += ":--|"
		output += "\n"

		# find maximum number of users in factions
		maxUsers = 0
		maxCommanders = 0
		maxUnits = 0
		for faction in self.factions:
			numUsers = len(faction.getUsers())
			numCommanders = len(faction.getCommanders())
			numUnits = len(faction.getUnits())
			if maxUsers < numUsers:
				maxUsers = numUsers
			if maxCommanders < numCommanders:
				maxCommanders = numCommanders
			if maxUnits < numUnits:
				maxUnits = numUnits

		output += "|**Users**"
		for i in range(0, maxUsers):
			if i > 0:
				output += "|"

			for faction in self.factions:
				users = faction.getUsers()
				output += "|"

				if len(users) > i:
					output += users[i]

				output += "|||"

			output += "\n"
			
		output += "|**Commanders**"
		for i in range(0, maxCommanders):
			if i > 0:
				output += "|"

			for faction in self.factions:
				commanders = faction.getCommanders()
				output += "|"

				if len(commanders) > i:
					output += commanders[i]

				output += "|||"

			output += "\n"

		output += "|**Units**"
		for i in range (0, numFactions):
			output += "|**Amount**|**Region**|**Type**|**CV**"

		for i in range(0, maxUnits):
			output += "|"

			for faction in self.factions:
				units = faction.getUnits()
				output += "|"

				if len(units) > i:
					output += units[i].getTableRow()

			output += "\n"
			
		return output