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

	# unitsParameters: amount region|cv <<name>>
	unitsParameters = factionSplit[1].strip();
	space = unitsParameters.find(' ')
	amount = unitsParameters[:space]

	# unitsParameters: region|cv <<name>>
	unitsParameters = unitsParameters[space:].strip()
	space = unitsParameters.find(' ')

	if space < 0:
		region = unitsParameters.strip()
	else:
		region = unitsParameters[:space].strip()
		name = unitsParameters[space:].strip()

	# Use a direct combat value if region is a float
	try:
		cv = float(region)
		region = ''

		unit = Unit(name, cv)
		units = Units(unit, amount)
		faction.addUnits(units)
	except ValueError:
		# Use the regional values from setup
		if name == '':
			# Get the standard setup from the region
			unitArray = battle.getSetup().getAllUnits(region)
			for unit in unitArray:
				units = Units(unit, float(amount) * unit.getPercentage())
				faction.addUnits(units)
		else:
			unit = battle.getSetup().getUnit(region, name)
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
	
def SetSettingUnit(text, setup):
	# text: Region Name(Spaces OK) Percentage% CV
	token = text.strip().find(' ')
	region = text[:token]
	parameters = text[token:].strip()
	# parameters: Name(Spaces OK) Percentage% CV
	tokenPercent = parameters.find('%')
	token = parameters.rfind(" ", 0, tokenPercent)
	name = parameters[:token].strip()
	percent = parameters[token:tokenPercent].strip()
	cv = parameters[tokenPercent+1:].strip()
	setup.addUnit(name, cv, percent, region)

# Look for these tokens
beginTag = "[["
endTag = "]]"

settingWords = {
		beginTag + "unit "	: SetSettingUnit}

battleWords = {
		beginTag + "battle "	: SetBattle, 
		beginTag + "terrain "	: SetTerrain,
		beginTag + "faction "	: SetFaction,
		beginTag + "user "	: SetUser,
		beginTag + "commander "	: SetCommander,
		beginTag + "units "	: SetUnits,
		beginTag + "confirm"	: DoConfirm,
		beginTag + "delete"	: DoDelete}

def checkSubForNewBattles(subreddit, setupObject, conn):
	cursor = conn.cursor()
	for submission in subreddit.get_new(limit=100):
		# Does the database already have this battle?
		cursor.execute("SELECT \"SubmissionID\" FROM \"Battles\" WHERE \"SubmissionID\" = '" + submission.id + "' LIMIT 1")
		if cursor.rowcount > 0:
			continue

		orig_text = submission.selftext
		op_text = orig_text.lower()
		battleContent = ''

		# Check each token
		for battleWord in battleWords.keys():
			position = 0

			# Look for the token for as many times as it appears in the message
			while True:
				position = op_text.find(battleWord, position)
				if position < 0:
					break # Token not found
					
				# Isolate the elements
				element = orig_text[position:]
				end = element.find(endTag)
				element = element[:end+len(endTag)].strip()
				if end > 0:
					battleContent += element
				position = position + 1

		# If this could be a real battle
		if len(battleContent) > 0:
			cursor.execute("INSERT INTO \"Battles\" (\"Timestamp\", \"SubmissionID\", \"BattleTableID\", \"BattleContent\", \"SetupContent\") VALUES (%s, %s, %s, %s, %s)", (datetime.datetime.utcnow(), submission.id, battleTable.id, battleContent, setupObject.getContent()))
			conn.commit()
	cursor.close()
	
def postBattleSetups(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM \"Battles\" WHERE \"SetupPosted\" = false")

	for (BattleContent, SetupContent, SubmissionID) in cursor:
		# Prepare Battle object for new battle
		battle = Battle(parseSetup(SetupContent))
		orig_text = BattleContent
		op_text = orig_text.lower()

		# Check each token
		for battleWord in battleWords.keys():
			position = 0

			# Look for the token for as many times as it appears in the message
			while True:
				position = op_text.find(battleWord, position)
				if position < 0:
					break # Token not found

				# Isolate the parameters
				element = orig_text[position:]
				end = element.find(endTag)
				element = element[:end+len(endTag)].strip()
				beginParameters = element.find(' ')
				if beginParameters > 0 and end > beginParameters:
					parameters = element[beginParameters:end].strip()
					# Call the appropriate function for this token
					battleWords[battleWord](parameters, battle)
				position = position + 1

		# If this is a real battle
		if battle.isValid():
			# Process battle output
			submission = r.get_submission(submission_id = SubmissionID)
			battleTable = submission.add_comment(str(battle))
			cursor.execute("UPDATE \"Battles\" SET \"SetupPosted\" = %s WHERE \"SubmissionID\" = %s", (True, SubmissionID))
			conn.commit()
	cursor.close()

def parseSetup(orig_text):
	setupObject = Setup()
	setupObject.clear()

	op_text = orig_text.lower()

	# Check each token
	for settingWord in settingWords.keys():
		position = 0

		# Look for the token for as many times as it appears in the message
		while True:
			position = op_text.find(settingWord, position)
			if position < 0:
				break # Token not found

			# Isolate the parameters
			element = orig_text[position:]
			end = element.find(endTag)
			element = element[:end+len(endTag)].strip()
			beginParameters = element.find(' ')
			if beginParameters > 0 and end > beginParameters:
				setupObject.addContent(element)
				parameters = element[beginParameters:end].strip()
				# Call the appropriate function for this token
				settingWords[settingWord](parameters, setupObject)
			position = position + 1
	return setupObject

def getSetupSubreddit(setupSubmission):
	if setupSubmission.title.find(settingsPrefix) != 0:
		print ("Setup skipping due to malformed title: " + setupSubmission.title)
		return None

	subToCheck = setupSubmission.title[len(settingsPrefix):].strip()
	# Subs don't have spaces
	if (subToCheck.find(" ") >= 0):
		print ("Setup skipping due to spaces: /r/" + subToCheck)
		return None

	subreddit = r.get_subreddit(subToCheck)
	moderators = subreddit.get_moderators()
	if setupSubmission.author not in moderators:
		print ("Setup skipping due to nonmoderator /u/" + setupSubmission.author.user_name + " for /r/" + subToCheck)
		return None
	
	return subreddit
	
def getSettings(settingsPrefix):
	# Check own subreddit for settings
	queryString = "subreddit:'" + os.environ['REDDIT_USER'] + "' title:'" + settingsPrefix + "*'"
	return r.search(queryString)