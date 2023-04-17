import sqlite3
from entity import Player
import csv
import pygame as pg
from inventory import Item

class Database():
	def __init__(self, game):
		self.game = game

	# Open connection and cursor at the beginning of each command
	def start(self):
		self.connection = sqlite3.connect("terrabyte.db")
		self.cursor = self.connection.cursor()

	# Commit, close cursor and connection at the end of each command
	def finish(self):
		self.connection.commit()
		self.cursor.close()
		self.connection.close()


	# Create player table
	def create_player_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblPlayer (
							"player_id"	INTEGER NOT NULL,
							"username"	TEXT,
							"display_name" TEXT,
							"password_hash"	TEXT,
							"player_level" INTEGER,
							"map_level" INTEGER,
							"max_health" INTEGER,
							"sprite_path" TEXT,
							PRIMARY KEY("player_id" AUTOINCREMENT)
						);"""
		self.cursor.execute(self.query)
		self.finish()	


	""" Create inventory table """
	def create_inventory_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblInventory (
							"player_id" INTEGER TEXT,
							"item_name" TEXT,
							FOREIGN KEY("player_id") REFERENCES tblPlayer("player_id")
						);"""
		self.cursor.execute(self.query)
		self.finish()

	""" Create item table """
	def create_item_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblItem (
							"item_name" TEXT NOT NULL,
							"rarity" TEXT,
							"type" TEXT,
							"damage" INT,
							"sprite_path" TEXT,
							PRIMARY KEY("item_name")
						);"""
		self.cursor.execute(self.query)
		self.finish()
		# Insert all item data into tblItem if doesn't already exist 


	def insert_all_items(self):
		""" 
		Handle all initial item database insertion
		In the future, if i decide to add a wider variety of items, their csv files can be inserted from this method
		"""
		self.insert_items_from_csv('items.csv')


	""" Create table to store all level completions """
	def create_level_completion_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblLevelCompletion (
							"completion_id" INTEGER NOT NULL,
							"player_id" INTEGER NOT NULL,
							"level" INTEGER NOT NULL,
							"score" INTEGER NOT NULL,
							PRIMARY KEY("completion_id" AUTOINCREMENT)
							FOREIGN KEY("player_id") REFERENCES tblPlayer("player_id")
							FOREIGN KEY("level") REFERENCES tblMap("level")
						);"""
		self.cursor.execute(self.query)
		self.finish()
		

	"""Create map table"""
	def create_map_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblMap (
							"level" INTEGER NOT NULL,
							"map_name" TEXT,
							"time_limit" INT,
							"tmx_path" TEXT,
							PRIMARY KEY("level")
						);"""
		self.cursor.execute(self.query)
		self.finish()
		self.insert_into_map_table(1, 'Terrarium', 60, 'Maps/Levels/level1.tmx')

	""" Create enemy table """
	def create_enemy_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblEnemy (
							"display_name" TEXT NOT NULL,
							"attack" INT,
							"max_health" INT,
							"points" INT,
							"sprite_path" TEXT,
							PRIMARY KEY("display_name")
						);"""
		self.cursor.execute(self.query)
		self.finish()

		self.insert_into_enemy_table('Brain Mole Monarch', 1, 30, 100, 'Assets/Sprites/Mobs/BrainMoleMonarch.png')
		self.insert_into_enemy_table('Kobold Priest', 2, 40, 200, 'Assets/Sprites/Mobs/KoboldPriest.png')
		self.insert_into_enemy_table('Cacodaemon', 3, 50, 400, 'Assets/Sprites/Mobs/Cacodaemon.png')
		self.insert_into_enemy_table('Minotaur', 4, 60, 800, 'Assets/Sprites/Mobs/Minotaur.png')


	"""Create keybinds table"""
	def create_keybinds_table(self):
		self.start()
		self.query = """ CREATE TABLE IF NOT EXISTS tblKeybinds (
							"player_id" INTEGER NOT NULL,
							"up_key" TEXT,
							"left_key" TEXT,
							"down_key" TEXT,
							"right_key" TEXT,
							"attack_key" TEXT,
							"inventory_key" TEXT,
							FOREIGN KEY ("player_id") REFERENCES tblPlayer ("player_id")
						);"""
		self.cursor.execute(self.query)
		self.finish()



	""" Update level completion table"""
	def update_level_completion_score(self, player_id, level, score):
		""" 
		Update level completion table
		To only be called within insert_into_level_completion_table()
		Parameters:
			player_id (int)   --> primary key of player
			level     (int)   --> map level primary key
			score     (score) --> new high score
		"""

		self.query = ("UPDATE tblLevelCompletion SET score = ? WHERE player_id = ? AND level = ?")
		self.values = (score, self.player_id, level)
		self.cursor.execute(self.query, self.values)


	def insert_into_level_completion_table(self, level, score):
		""" 
		INSERT into level_complation table 
		Parameters:
			level     (int) --> level completed
			score     (int) --> score achieved by player at level completion
		"""
		self.start()
		self.query = ("SELECT score FROM tblLevelCompletion WHERE player_id = ? AND level = ?")
		self.values = (self.player_id, level)
		self.cursor.execute(self.query, self.values)
		self.answer = self.cursor.fetchone()

		# If player has not played that level yet, then
		if self.answer == None:
			# Insert record or update existing record if the new score is higher than the stored one
			self.query = ("INSERT INTO tblLevelCompletion (player_id, level, score) VALUES (?, ?, ?)")
			self.values = (self.player_id, level, score)
			self.cursor.execute(self.query, self.values)

		# If player's score is greater than previous high score
		elif score > self.answer[0]:
			# Update record
			self.update_level_completion_score(self.player_id, level, score)
		self.finish()


	def get_top_x(self, level, limit):
		"""
        Get a list of top x players for that level
        Parameters:
        level  (int) --> current level
        limit  (int) --> number of players to display on leaderboard
        """
		self.start()
		# Select names and scores of players for the given level
		self.query = (""" SELECT tblPlayer.display_name, tblLevelCompletion.score
						  FROM tblLevelCompletion
                          JOIN tblPlayer ON tblPlayer.player_id = tblLevelCompletion.player_id
                          WHERE tblLevelCompletion.level = ?
                          ORDER BY tblLevelCompletion.score DESC LIMIT ?
                       """);
		self.values = (level, limit)
		self.cursor.execute(self.query, self.values)
		self.answer = self.cursor.fetchall()
		self.finish()

		return self.answer



	def update_item_table(self, item_name , rarity, item_type, damage, sprite_path):
		""" 
		INSERT values into item table
		Parameters:
			item_name   (str) --> name of item (pk)
			rarity      (str) --> how rare the item is 
			item_type   (str) --> what type of item
			damage      (int) --> the attack that the item will give the player
			sprite_path (str) --> file path for item icon
		"""
		self.start()


	def insert_into_item_table(self, item_name, rarity, item_type, damage, sprite_path):
		""" 
		INSERT values into item table
		Parameters:
			item_name   (str) --> name of item (pk)
			rarity      (str) --> how rare the item is 
			item_type   (str) --> what type of item
			damage      (int) --> the attack that the item will give the player
			sprite_path (str) --> file path for item icon
		""" 
		self.start()
		self.query = ("INSERT OR IGNORE into tblItem (item_name, rarity, type, damage, sprite_path) values (?, ?, ?, ?, ?)")
		self.values = (item_name, rarity, item_type, damage, sprite_path)
		self.cursor.execute(self.query, self.values)
		self.finish()

	def insert_into_inventory_table(self, item_name):
		""" 
		INSERT player_id and item into inventory table occurs when user gets an item
		Parameters:
			item_name (str) --> primary key of item used as fk
		"""
		self.start()
		self.query = ("INSERT OR IGNORE into tblInventory (player_id, item_name) VALUES (? ,?)")
		self.values = (self.player_id, item_name)
		self.cursor.execute(self.query, self.values)
		self.finish()

	def delete_from_inventory_table(self, item_name):
		""" DELETE item from player's inventory
		Parameters:
			item_name (str) --> primary key of item to be removed
		"""
		self.start()
		self.query = ("DELETE FROM tblInventory WHERE player_id = ? AND item_name = ?")
		self.values = (self.player_id, item_name)
		self.cursor.execute(self.query, self.values)
		self.finish()

	""" INSERT values into map table"""
	def insert_into_map_table(self, level, map_name, time_limit, tmx_path):

		""" 
		INSERT values into map table
		Parameters:
			level      (int) --> level number to be used as primary key
			map_name   (str) --> name of map
			time_limit (int) --> maximum time allocated to player 
			tmx_path   (str) --> file path for map.tmx file 
		"""
		# Check if map is already in table
		self.start()
		# Only INSERT map if record doesn't already exist
		self.query = ("INSERT OR IGNORE INTO tblMap (level, map_name, time_limit, tmx_path) values (?, ?, ?, ?)")
		self.values = (level, map_name, time_limit, tmx_path)
		self.cursor.execute(self.query, (self.values))
		self.finish()


	def insert_into_player_table(self, username, password_hash, player_level, map_level, max_health, sprite_path):
		""" INSERT values into player table
		Only called within valid_registartion() so doesn't close connection at the end

		Paramaters:
			username      (str)	--> name user entered in registration
			password_hash (str) --> hashed password from registration
			player_level  (int) --> experience level of player, default set to 1 
			map_level     (int) --> map level of player, default set to 1
			max_health    (int) --> max health of player, default set to 50
			sprite_path   (str) --> file path to default player sprite sheet
		"""
		self.start()
		self.query = ("INSERT INTO tblPlayer (username, password_hash, player_level, map_level, max_health, sprite_path) values(?, ?, ?, ?, ?, ?)")
		# Set default values
		self.values = (username, password_hash, player_level, map_level, max_health, sprite_path)
		self.cursor.execute(self.query, self.values)

				
	def insert_into_enemy_table(self, display_name, attack, max_health, points, sprite_path):
		""" 
		INSERT default values into enemy table 
		Parameters:
			display_name (str) --> name of enemy
			attack       (int) --> damage enemy will do
			max_health   (int) --> maximum health of enemy
			points       (int) --> points that the player will gain for killing this enemy
			sprite_path  (str) --> file path for enemy sprite sheet
		"""
		self.start()
		self.query = ("INSERT OR IGNORE into tblEnemy (display_name, attack, max_health, points, sprite_path) values (?, ?, ?, ?, ?)")
		self.values = (display_name, attack, max_health, points, sprite_path)
		self.cursor.execute(self.query, self.values)
		self.finish()

	def insert_into_keybinds_table(self, player_id, up_key, left_key, down_key, right_key, attack_key, inventory_key):
		"""
		Insert default values into keybinds table
		Only called within valid_registartion() so doesn't close connection at the end

		Parameters:
			player_id     (int) --> primary key
			up_key        (str) --> up keybind
			left_key      (str) --> left keybind
			down_key  	  (str) --> down keybind
			right_key     (str) --> right keybind
			attack_key    (str) --> attack keybind
			inventory_key (str) --> inventory keybind
		"""
		self.query = ("INSERT INTO tblKeybinds (player_id, up_key, left_key, down_key, right_key, attack_key, inventory_key) values(?, ?, ?, ?, ?, ?, ?)")

		self.values = (player_id, up_key, left_key, down_key, right_key, attack_key, inventory_key)
		self.cursor.execute(self.query, self.values)


	def get_player_data(self, player_id):
		""" 
		Get data for given player FROM database 
		Parameters:
		player_id --> Primary key of player
		"""
		self.start()
		self.query = str("SELECT * FROM tblPlayer WHERE player_id = ?")
		self.values = player_id
		self.cursor.execute(self.query, (self.values,))
		self.answer = self.cursor.fetchone()
		self.finish()  
		
		return self.answer



	""" Get data for given level FROM database """
	def get_level_data(self, level):
		""" 
		Paramaters:
		level --> level (primary key) for which the data is to be extracted 
		"""
		self.start()
		# SELECT map_name, time_limit, tmx_fields FROM map table for the level given
		self.query = str("SELECT map_name, time_limit, tmx_path FROM tblMap WHERE level = ?")
		self.values = level
		self.cursor.execute(self.query, (self.values,))
		self.answer = self.cursor.fetchone() # Seperate data via comma for indexing purposes

		self.finish()

		return self.answer


	""" Get highest map level from database """
	def get_max_map_level(self):
		self.start()
		self.query = str(" SELECT * from tblMap ORDER BY level DESC")
		self.cursor.execute(self.query)
		self.answer = self.cursor.fetchone()
		return self.answer[0]

	""" Update fields in map table """
	def update_map_table(self, field, value, level):
		self.start()
		# Set field value to value of argument for the desired map
		self.query = str(" UPDATE tblMap set ? = ? WHERE level = ?")
		self.values = (field, value, level)
		self.cursor.execute(self.query, (self.values))
		self.finish()

	def insert_items_from_csv(self, csv_file):
		""" 
		Insert all items to the item table formatted as
		{item_name, rarity, type, damage, sprite_path}
		Iterate through csv file inserting values into tblItem
		Parameters:
			csv (str) --> csv file path containing all items
		"""
		# Open file in read mode
		file = open(csv_file, "r")
		reader = csv.reader(file)
		# Skip first row as this contains the columns
		next(reader)
		max_items = 0
		for row in reader:
			# Extract data
			item_name = row[0]
			rarity = row[1]
			item_type = row[2]
			damage = row[3]
			# Get file path for item
			sprite_path = (f"Assets/Icons/Items/{item_type}s/{rarity}/{item_name}.png")
			# Insert data into tblItems
			self.insert_into_item_table(item_name, rarity, item_type, damage, sprite_path)

			item = Item(self.game, item_name, rarity, item_type, damage, sprite_path)
			self.game.all_items.append(item)
			self.assign_item_list(item)
			max_items +1
		file.close()
		self.game.max_items = max_items


	def assign_item_list(self, item):
		""" 
		Appends to a specific list in the inventory object for further item handling
		Parameters:
			item (object) --> object containing item details
		"""
		if item.rarity == 'Common':
			self.game.common_items.append(item)
		elif item.rarity == 'Uncommon':
			self.game.uncommon_items.append(item)
		elif item.rarity == 'Rare':
			self.game.rare_items.append(item)
		elif item.rarity == 'Epic':
			self.game.epic_items.append(item)
		elif item.rarity == 'Legendary':
			self.game.legendary_items.append(item)
		# Catch invalid input, these are the only possible rarities as of now.
		else:
			print("Invalid rarity, manipulation with game files ")
			pg.quit()


	def load_inventory(self):
		"""
		Returns a 2d list of item objects corrosponding to the items that belong to the user's saved inventory in tblInventory
		Parameters:
			self.player_id (int) --> player id of object already initialised after login/registation
				If new player, only item in inventory should be Wooden Sword
		"""
		self.start()
		# Select all items within player's inventory
		self.query = ("""SELECT tblItem.item_name, tblItem.rarity, tblItem.type, tblItem.damage, tblItem.sprite_path 
						 FROM tblInventory 
						 JOIN tblItem ON tblInventory.item_name = tblItem.item_name
						 WHERE tblInventory.player_id = ?
						""");
		self.values = (self.player_id,)
		self.cursor.execute(self.query, self.values)
		items = self.cursor.fetchall()
		self.finish()
		# Handle none case
		if items != None:
			# For each item in the array of item tuples, create item object with those attributes

			rows = self.game.player.inventory.rows 
			columns = self.game.player.inventory.columns
			# Create empty 2d array with ^ dimensions
			inventory = [[None for _ in range(columns)] for _ in range(rows)]
			# Create item object for each item
			for i, item in enumerate(items):
				item_name 	= item[0]
				rarity 		= item[1] 
				item_type 	= item[2]
				damage 		= item[3]
				# Get file path for item 
				sprite_path = (f"Assets/Icons/Items/{item_type}s/{rarity}/{item_name}.png")

				# Create new item
				newItem = Item(self.game, item_name, rarity, item_type, damage, sprite_path)
				# Add item to inventory list

				# Add item to next position in the 2d list
				row = i // columns
				column = i % columns
				inventory[row][column] = newItem

			return inventory
			# Return all item objects in inventory
		else:
			# No items were retrieved from database
			print("Error, no items in inventory")




	def get_inventory_list(self):
		"""
		Returns a list of item names corrosponding to the items that belong to the user's saved inventory in tblInventory
		Parameters:
			self.player_id (int) --> player id of object already initialised after login/registation
			If new player, only item in inventory should be Wooden Sword
			Comparable with other item objects if name is used 
		"""
		self.start()
		# Select all items within player's inventory
		self.query = ("""SELECT tblItem.item_name, tblItem.rarity, tblItem.type, tblItem.damage, tblItem.sprite_path 
						 FROM tblInventory 
						 JOIN tblItem ON tblInventory.item_name = tblItem.item_name
						 WHERE tblInventory.player_id = ?
						""");
		self.values = (self.player_id,)
		self.cursor.execute(self.query, self.values)
		items = self.cursor.fetchall()
		names = []
		for i, item in enumerate(items):
			item_name 	= item[0]
			names.append(item_name)
		return names
		self.finish()

	def validate_registration(self, user, pass_hash):
		
		""" Recieve inputs FROM registeration form and INSERT into database
			Upon registering, make other values default 

		Parameters:
		user --> username entered in registration
		password_hash --> hashed pasword entered in registration

		"""
		self.start()
		self.query = str(""" SELECT username FROM tblPlayer WHERE username = ?""")
		self.values = (user,)
		self.cursor.execute(self.query, self.values)
		self.answer = self.cursor.fetchone()
		self.finish()


		#Check if username already exists within the database
		if self.answer != None:
			print("Username already taken")
			self.game.registration_page.valid_registration = False
		else:
			# Username is valid so insert data into table
			self.insert_into_player_table(user, pass_hash, 1, 1, 150, 'Assets/Sprites/Player/HoodedProtagonist.png')  # INSERT DEFAULT DATA HERE
			# Inserting default keybinds into keybinds table upon registration, initialise all items in database
			
			# Get player_id
			self.cursor.execute(""" SELECT last_insert_rowid()""")
			self.player_id = self.cursor.fetchone()[0]	
			self.insert_into_keybinds_table(self.player_id, 'w', 'a', 's', 'd','space','e')
			# Creating player object
			# Creating default player template with player_id
			self.game.player = Player(self.game, user, None, 100, 0 ,2, 1, 1, "Assets/Sprites/Player/HoodedProtagonist.png", self.player_id)
			self.game.registration_page.valid_registration = True
			self.finish()
			# Give player a wooden sword in their inventory, default weapon
			self.insert_into_inventory_table('Wooden Sword') # Finish conn
		




	# Pass username, hashed password FROM backend login into database object within game file
	def validate_login(self, user, pass_hash):
		""" 
		Parameters:
		user --> Username text entered in login 
		pass_hash --> hashed pasword text entered FROM login
		"""
		self.start()
		self.query = str(""" SELECT * FROM tblPlayer WHERE username = ? and password_hash = ?""")
		self.values = (user, pass_hash,)
		self.cursor.execute(self.query, self.values)
		# Display fields within seperate list indixes
		self.answer = self.cursor.fetchone()
		self.finish()

		if self.answer != None:
			print("Successful Login")
			# Generate success page
			self.game.login_page.valid_login = True

			# Get relevant fields from database
			self.player_id = self.answer[0]
			display_name = self.answer[2]
			player_level = self.answer[4]
			map_level = self.answer[5]
			max_health = self.answer[6]
			sprite_path = self.answer[7]

			# Set game.player to Player of user's attributes and insert gamedata to db
			self.game.player = Player(self.game, user, display_name, max_health, 0, 2, player_level, map_level, sprite_path, self.player_id)
			# Initialise all items
		else:
			# Generate error 
			print("Unsucessful Login")
			self.game.login_page.valid_login = False


	""" Update individual records in player table """
	def update_player_table(self, column, value, player_id):

		"""
		Parameters:

		column--> name of column to update
		value --> value to set column to
		player_id --> record to update

		"""
		self.start()
		self.query = f"UPDATE tblPlayer SET {column} = ? WHERE player_id = ?"
		self.values = (value, player_id)
		self.cursor.execute(self.query, self.values)
		self.finish()




	def is_returning_player(self):
		""" Check whether or not user is a returning player (already set their display_name)

		Paramaters:
		player_id --> user's player_id in player table
		"""
		self.start()
		self.query = ("SELECT display_name FROM tblPlayer WHERE player_id = ?")
		self.values = (self.player_id,)
		self.cursor.execute(self.query, self.values)
		self.result = self.cursor.fetchone()


		# If user has already entered a display_name before
		if self.result[0] != None:
			return True 
		else:
			return False



	# Return list of keybind keys from database
	def load_keys(self):
		self.start()
		self.query = ("SELECT up_key, left_key, down_key, right_key, attack_key, inventory_key from tblKeybinds where player_id = ?")
		self.values = (self.player_id,)
		self.cursor.execute(self.query, self.values)
		self.result = self.cursor.fetchall()
		return self.result[0]

	# Update keybinds in database
	def update_keys_table(self, keys):
		"""
	 	Update keybind keys in database 
		Parameters:
			keys[] --> list of keybinds where
				keys[0] --> up_key 
				keys[1] --> left_key
				keys[2] --> down_key
				keys[3] --> right_key
				keys[4] --> attack_key
				keys[5] --> inventory_key
		"""
		self.start()
		self.query = ("UPDATE tblKeybinds SET up_key = ?, left_key = ?, down_key = ?, right_key = ?, attack_key = ?, inventory_key = ? WHERE player_id = ?")
		# Add values
		self.values = (keys[0], keys[1], keys[2], keys[3] ,keys[4], keys[5], self.player_id)
		self.cursor.execute(self.query, self.values)
		self.finish()


	def get_enemy_data(self, display_name):
		""" 
		Get data for specific mob from database
		Parmeters:
			display_name --> name of mob to retrieve data from 
		"""

		self.start()
		# Get all enemy data
		self.query = ("SELECT * FROM tblEnemy WHERE display_name = ?")
		self.values = display_name
		self.cursor.execute(self.query, (self.values,))
		self.answer = self.cursor.fetchone()
		self.finish()

		return self.answer


	#Create all tables
	def create_all_tables(self):
		self.create_player_table()
		self.create_item_table()
		self.create_inventory_table()
		self.create_map_table()
		self.create_enemy_table()	
		self.create_level_completion_table()
		self.create_keybinds_table()
