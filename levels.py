import pygame as pg
import pytmx
from pytmx.util_pygame import load_pygame
from entity import BrainMoleMonarch
import random
import time


class ImpactTile():
	def __init__(self, name, x, y, width, height, surface):

		self.name = name 
		self.x = x 
		self.y = y 
		self.width = width
		self.height = height 
		self.surface = surface
		self.rect = self.surface.get_rect(topleft=(x,y))    # Converiting tile surface to rectangle



class Level():
	def __init__(self, game, level, map_name, time_limit, tmx_path):


		self.game = game
		self.level = level 
		self.map_name = map_name 
		self.tmx_path = tmx_path
		self.time_limit = time_limit

		self.run_display = False
		# Load the tiled map data
		self.tmx_data = load_pygame(self.tmx_path)
		self.origin = [0,0]
		self.font_name = "Fonts/DigitalDisco.ttf"
		self.clock = pg.time.Clock()

		self.count = 0

		self.item_obtained = None


		# Get layers for walls and water in the tiled map
		self.wall_layer = self.tmx_data.get_layer_by_name('Walls')
		self.water_layer = self.tmx_data.get_layer_by_name('Water')

		self.wall_rects = []   # list of all wall rectangles
		self.wall_objects = [] # wall_object[i] can return individual wall tile object

		self.water_rects = []   # list of all water rectangles
		self.water_objects = []   # list of all water objects

		self.max_moles = 2   # Set max number of moles to be spawned
		self.mole_rects = []
		self.mole_objects = []

		# List of all rects on screen
		# List of all objects
		self.enemy_objects = []
		self.enemy_rects = []

		# Initialise enemy data from database
		self.initialise_enemy_data()
		""" Initialise level constants """
		self.initialise_walls(32, 32)
		self.initialise_water(32, 32)

		self.loot_start_time = 0
		self.time_elapsed = None

	def initialise_enemy_data(self):
		self.brain_mole_monarch_data = self.game.database.get_enemy_data('Brain Mole Monarch')
		self.kobold_priest_data = self.game.database.get_enemy_data('Kobold Priest')
		self.cacodaemon_data = self.game.database.get_enemy_data('Cacodaemon')
		self.minotaur_data = self.game.database.get_enemy_data('Minotaur')


	# Create ImpactTile objects for all the tiles in the wall layer
	def initialise_walls(self, height, width):

		for tile in self.wall_layer.tiles():  
			# Create a new ImpactTile object for each wall tile
			wallTile = ImpactTile('Wall', tile[0]*width, tile[1]*height, width, height,  tile[2])

			# Draw the tile surface as a rectangle on the screen
			pg.draw.rect(self.game.screen, self.game.white, wallTile.rect)

			# Append new impact tile to wall_objects and it's rect to wall_rects
			self.wall_objects.append(wallTile)    
			self.wall_rects.append(wallTile.rect)



	# Create ImpactTile objects for all the tiles in the water layer
	def initialise_water(self, height, width):

		for tile in self.water_layer.tiles():
			# Create a new ImpactTile object for each water tile
			waterTile = ImpactTile('Water', tile[0]*width, tile[1]*height, width, height, tile[2]) 

			# Draw the tile surface as a rectangle on the screen
			pg.draw.rect(self.game.screen, self.game.white, waterTile.rect)    

			# Append new impact tile to water_objects and it's rect to wall_rects
			self.water_objects.append(waterTile)    
			self.water_rects.append(waterTile.rect)


	""" Iterate through wall rects comparing their rectangles with user's rectangle """
	def check_wall_collisions(self):
		collision = self.game.player.rect.collidelist(self.wall_rects)   # Returns -1 if there's a collision with any wall rect
		if collision == -1:         # If there's no collision with any of the wall rects               
			self.game.player.touching_wall = False # Player isn't touching a wall
		else:
			self.game.player.touching_wall = True   # Player is touching a wall


	""" Iterate through water rects comparing their rectangles with user's rectangle """
	def check_water_collisions(self):
		collision = self.game.player.rect.collidelist(self.water_rects)
		if collision == -1:
			self.game.player.touching_water = False
			self.game.player.set_speed(self.game.player.base_speed) # No collision so set base speed
		else: 
			self.game.player.touching_water = True
			self.game.player.set_speed(1)           # Collision so slow user down


	""" Set health of enemies to max """
	def replenish_enemies(self):
		for enemy in self.enemy_objects:
			enemy.reset_health()

	def check_collisions(self):
		self.check_wall_collisions()
		self.check_water_collisions()


	""" Iterate through all layers and print to screen """
	def display_map(self, screen, tmx_data, width, height):
		for layer in tmx_data.visible_layers:

			for tile in layer.tiles():
				x = tile[0] * width	
				y = tile[1] * height
				self.game.screen.blit(tile[2], (x,y))

	def check_movement(self, keys, event_type):
		if event_type == pg.KEYDOWN:
			if keys[self.game.control_menu.up_keybind.get_key_code()]:    # If keycode is pressed
				self.game.control_menu.up_keybind.set_pressed(True)  # Set player key pressed to True
				if self.game.player.facing == "Right":
					self.game.player.set_motion("Up Right")
				else:
					self.game.player.set_motion("Up Left")

			if keys[self.game.control_menu.down_keybind.get_key_code()]:
				self.game.control_menu.down_keybind.set_pressed(True)
				if self.game.player.facing == "Right":
					self.game.player.set_motion("Down Right")
				else:
					self.game.player.set_motion("Down Left")

			if keys[self.game.control_menu.left_keybind.get_key_code()]:
				self.game.control_menu.left_keybind.set_pressed(True)
				self.game.player.set_motion("Left")
				self.game.player.set_facing("Left")

			if keys[self.game.control_menu.right_keybind.get_key_code()]:
				self.game.control_menu.right_keybind.set_pressed(True)
				self.game.player.set_motion("Right")
				self.game.player.set_facing("Right")

			if keys[self.game.control_menu.attack_keybind.get_key_code()]:
				self.game.control_menu.attack_keybind.set_pressed(True)
				self.game.player.set_attacking(True)


			if keys[self.game.control_menu.inventory_keybind.get_key_code()]:
				self.game.control_menu.inventory_keybind.set_pressed(True)
				self.run_display = False
				self.game.player.inventory.display_inventory()



		if event_type == pg.KEYUP:
			""" If keybind isn't pressed, set keybind 'pressed' to False to stop movement."""
			if not keys[self.game.control_menu.up_keybind.get_key_code()]:    
				self.game.control_menu.up_keybind.reset_key() 				  

			if not keys[self.game.control_menu.down_keybind.get_key_code()]:
				self.game.control_menu.down_keybind.reset_key()

			if not keys[self.game.control_menu.left_keybind.get_key_code()]:
				self.game.control_menu.left_keybind.reset_key()
				if self.game.control_menu.right_keybind.get_pressed():
					self.game.player.set_motion("Right")
					self.game.player.set_facing("Right")

			if not keys[self.game.control_menu.right_keybind.get_key_code()]:
				self.game.control_menu.right_keybind.reset_key()
				if self.game.control_menu.right_keybind.get_pressed():
					self.game.player.set_motion("Left")
					self.game.player.set_facing("Left")

			if not keys[self.game.control_menu.attack_keybind.get_key_code()]:
				self.game.control_menu.attack_keybind.reset_key()
				self.game.player.set_attacking(False)


	def check_pause(self, key):
		if key == pg.K_ESCAPE:
			self.run_display = False
			self.game.main_menu.display_menu()

	
	def get_number_of_moles(self):
		""" 
		Get number of current moles 
		Iterate through current enemy objects, counting the number of moles
		"""
		num = 0
		for enemy in self.enemy_objects:
			if enemy.display_name == 'Brain Mole Monarch':
				num += 1
		return num

	def spawn_moles(self, number):
		""" Display moles to screen
			Parameters:
				number(int) --> number of moles that can be spawned
			# spawn new mobs with this logic
		"""

		# While the length of moles storing mole objects is less than max moles
		if self.get_number_of_moles() != self.max_moles: 

			# Generate mole Coordinates
			x = random.randint(500, 1000)  
			y = random.randint(600, 900)

			# Get mole data
			data = self.brain_mole_monarch_data
			attack = data[1]
			max_health = data[2]
			points = data[3]
			sprite_path = data[4]

			# Create new  mole 
			newMole = BrainMoleMonarch(self.game, x, y, 'Brain Mole Monarch', attack, max_health, points, 2, sprite_path)

			# If newly created mole rectangle doesn't collide with a wall
			if (newMole.rect.collidelist(self.wall_rects)) == -1: 

				# Append object and rectangle to their respective lists   
				self.mole_objects.append(newMole)    
				self.enemy_objects.append(newMole)
			else:
				# Re-iterate
				pass



	

	def check_enemy_deaths(self):
		""" 
		Handle enemy deaths 
		Handle player item assignment
		"""
		# Check each currently enemy
		for enemy in self.enemy_objects:
			# If enemy health drops to 0
			if enemy.get_health() == 0:
				# Pop enemy from list 
				self.enemy_objects.pop(self.enemy_objects.index(enemy))
				# Add score to player
				self.game.player.add_score(enemy.points)
				# Check enemy loot drops
				self.check_enemy_item_drop()

	def check_enemy_item_drop(self):
		""" 
		Handle enemy loot drops respective to item rarity
		  FUTURE IMPLEMENTATION - could add another enemy attribute that can boost 'luck'
		  but said mobs will be harder to eliminate with higher health points
		"""
		# Check player's luck with rarities
		item_rarity = None
		luck = random.random()
		if luck < float(self.game.drop_rates['Legendary']):
			item_rarity = 'Legendary'
		elif luck < float(self.game.drop_rates['Epic']):
			item_rarity = 'Epic'
		elif luck < float(self.game.drop_rates['Rare']):
			item_rarity = 'Rare'
		elif luck < float(self.game.drop_rates['Uncommon']):
			item_rarity = 'Uncommon'
		elif luck < float(self.game.drop_rates['Common']):
			item_rarity = 'Common'
		else:
			item_rarity = None
		
		# If player obtained an item, get a randomitem from a list corrosponding to it's rarity
		if item_rarity:
			item = random.choice(self.game.get_rarity_list(item_rarity))
			print("\nLuck : ", luck)
			print("Item : ", item.name)
			# If inventory is not full, then add item to inventory
			if (self.game.player.inventory != self.game.player.inventory.max_items) and (item.name not in self.game.database.get_inventory_list()):
				# INSERT OR IGNORE FOR NO DUPLICATIONS
				self.game.database.insert_into_inventory_table(item.name)
				self.item_obtained = True
			else:
				# Break out of loop, player gets nothing!
				pass


	""" Handle player death events """
	def check_player_death(self):
		# If player dies
		if self.game.player.dead:
			# Stop displaying current level
			self.run_display = False
			# Switch to death screen
			self.game.after_life_menu.score = self.game.player.score 
			self.game.after_life_menu.dead = self.game.player.dead
			self.game.after_life_menu.display_menu()

	""" Handles all entity death events """
	def check_entity_deaths(self):
		self.check_enemy_deaths()
		self.check_player_death()


	""" Iterate through moles, displaying each one """
	def display_enemies(self):
		for enemy in self.enemy_objects:
			enemy.display_enemy()

	""" Display entities to screen """ # add new entities here
	def display_entities(self):
		self.game.player.display_player()
		self.display_enemies()

	def check_events(self):
		event_list = pg.event.get()
		key_list = pg.key.get_pressed()
		self.game.player.check_events()
		self.check_entity_deaths()
		self.check_wall_collisions()
		for event in event_list: 

			self.game.main_menu.check_quit(event.type)
			""" User events """
			self.check_movement(key_list, event.type)  # Name of the key but in lowercase
			if event.type == pg.KEYDOWN:
				# Check for user pausing, return to main menu
				self.check_pause(event.key)

	def clear_start_time(self):
		self.start_time = 0



	def draw_timer(self, remaining_time):
		""" 
		Display timer on screen 
		Parameters:
			remaining_time (int) --> Remaining time until level ends by default
		"""
		self.game.draw_text(str(remaining_time), self.game.white, 50, self.game.mid_x, self.game.mid_y - 450)


	""" Method to handle successful level completions """
	def check_time_limit(self, start_time):
		""" 
		Count until the time limit for the level is reached, then send player to after life page
			start_time (int) --> The time at which display_level() was called
		"""
		# Capture time elapsed since starting level in
		self.time_elapsed = (pg.time.get_ticks() - self.start_time) / 1000   # Convert from ms to seconds
		remaining_time = self.time_limit - self.time_elapsed  # Get time remaining
		self.draw_timer(int(remaining_time))  # Convert to string, display remaining time
		# If player has finished the level then
		if self.time_elapsed > self.time_limit: 
			self.run_display = False
			# Insert data into completion table
			if self.game.player.score != 0:
				self.game.database.insert_into_level_completion_table(self.level, self.game.player.score)
			# Pass relevant details to after life menu
			self.game.after_life_menu.score = self.game.player.score 
			self.game.after_life_menu.dead = self.game.player.dead
			self.game.after_life_menu.display_menu()

	""" Handle spawning of enemies """
	def spawn_enemies(self):
		self.spawn_moles(self.max_moles)

	""" Main loop """
	def display_level(self):
		self.run_display = True
		# Set score to 0
		self.game.player.score = 0
		self.start_time = pg.time.get_ticks()
		while self.run_display: 
			# Set start time
			level_start_time = self.start_time 
			self.game.screen.fill(self.game.black)
			#print("Level one")
			self.spawn_enemies()
			self.check_events()       # Check all events
			self.check_collisions()   # Check for collisions
			self.display_map(self.game.screen, self.tmx_data, 32, 32)  # Display map
			self.display_entities()
           # Set to 60fps
			"""
			print("\nPlayer rect x : ", self.game.player.rect.x)
			print("Player rect y : ", self.game.player.rect.y)
			print("First wall x : ", self.wall_objects[0].x)
			print("First wall y : ", self.wall_objects[0].y)
			"""	
			self.clock.tick(60)	
			self.check_time_limit(level_start_time)
			pg.display.update()


