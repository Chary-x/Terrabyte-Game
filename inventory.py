import pygame as pg
from button import Button, ItemButton



class Inventory():
	def __init__ (self, player):
		self.player = player
		self.run_display = False 
		self.font_name = "Fonts/DigitalDisco.ttf"

		#Buttons
		self.back = Button(self.player.game.black, self.player.game.red, 10, 10, 80,80, self.font_name, "BACK")
		self.item_buttons = []

		# Hold user items
		self.rows = 6
		self.columns = 6
		self.max_items = self.rows*self.columns


		#Holds location of next empty spot in array
		self.empty_spot = (0,1)

	
		self.offset_x = 410
		self.offset_y = 150

		""" Current item rectangle coordinates """
		self.current_item_rect  = pg.Rect(120 , 400 , 120, 120)
		self.current_item = None

		#2D array to store items
		self.inventory = [[None for _ in range(self.columns)] for _ in range(self.rows)]
		# Initialise inventory, load inventory data from database




	def load_inventory(self):
		""" 
		Load user inventory from database
		"""
		self.inventory = self.player.game.database.load_inventory()



	def draw_all_text(self):
		self.player.game.draw_text("INVENTORY", self.player.game.green, 80, self.player.game.mid_x, self.player.game.mid_y - 400)
		# draw current itemn's name in it's colour
		self.player.game.draw_text("RIGHT CLICK TO DELETE ITEM",self.player.game.red, 25, self.player.game.display_x - 230, 350)
		self.player.game.draw_text("BE CAREFUL", self.player.game.red, 23, 1410, 450)

	def check_back(self):
		# If user pressed back button
		if self.back.is_left_clicked():
			self.run_display = False    
			# Resume display of current level      
			self.player.game.player.current_level.display_level() 


	# Draw all buttons to screen
	def draw_all_buttons(self):
		self.back.draw_button(self.player.game.screen)
		for button in self.item_buttons:
			button.draw_button(self.player.game.screen)

	# Check icon events 
	def check_item_buttons(self):
		for button in self.item_buttons:
			button.check_events()
			button.draw_button(self.player.game.screen)
			# Set current item to button
			if button.is_left_clicked():
				print("LEFT CLICKED")
				# Refresh current_item display surface
				self.current_item = button.item
			# Remove item from inventory
			if button.is_right_clicked():
				print("RIGHT CLICKED")
				self.remove_item(button.item)


	# Check each 
	def check_events(self):
		event_list =  pg.event.get()
		key_list = pg.key.get_pressed()
		for event in event_list:
			self.check_item_buttons()
			self.player.game.main_menu.check_quit(event.type)
			self.check_back()

	""" Display current item icon """
	def display_current_item(self):
		if self.current_item != None:
			# Display current item rect
			colour = self.current_item.colours[self.current_item.rarity]
			pg.draw.rect(self.player.game.screen, colour, self.current_item_rect, 4)
			self.player.game.screen.blit(self.current_item.get_icon(), (self.current_item_rect.x,self.current_item_rect.y))
			self.draw_current_item_text(colour)

	def draw_current_item_text(self, colour):
		# Display current item text
			self.player.game.draw_text("LEFT CLICK TO SET CURRENT ITEM", colour, 25, 190, 300)
			self.player.game.draw_text("CURRENT ITEM", colour, 32, 180, 350)
			# Display item name
			self.player.game.draw_text(f"{self.current_item.name}", colour, 32, 190, 600)
			# Display item damage
			self.player.game.draw_text(f"RARITY : {self.current_item.rarity}", colour, 25, 190, 700)
			self.player.game.draw_text(f"Damage : {self.current_item.damage}", colour, 25, 190, 800)
			# Display total damage ( player + weapon )
			total_damage = int(self.player.attack + self.current_item.damage)
			self.player.game.draw_text(f"TOTAL DAMAGE : {total_damage}", colour, 20 , 190, 900)


	""" Draw all rectangles """
	def display_all_boxes(self):
		for row in range(self.rows):
			for column in range(self.columns):

				# Draw 6 by 6 grid with width 120px and border 2px
				pg.draw.rect(self.player.game.screen, self.player.game.white, ((column*120)+self.offset_x, (row*120)+self.offset_y, 120, 120), 2)

		# Draw container rect for current item
		pg.draw.rect(self.player.game.screen, self.player.game.white, self.current_item_rect, 2)


	""" Draw user items """
	def draw_inventory(self):
		# Load inventory 
		self.load_inventory()
		# Iterate through items
		for row in range(self.rows):
			for column in range (self.columns):
				item = self.inventory[row][column]
				# If inventory spot isn't empty
				if item is not None:
					# Getting item surface
					# Calculate x and y coordinates relateive to screen
					x = (column*120) + self.offset_x
					y = (row*120) + self.offset_y
					
					# Display icon surface at x,y cooridnates
					self.player.game.screen.blit(item.get_icon(), (x,y))
					pg.draw.rect(self.player.game.screen, item.colours[item.rarity], (x, y, item.width, item.height), 4)

					# Create button for each item in the inventory
					button  = ItemButton(self.player.game.black, self.player.game.silver, x, y, item.width, item.height, item)
					# Set button pos to positon in inventory
					button.set_pos((row,column))
					# Add item button to list of iterable item buttons
					self.item_buttons.append(button)
		self.display_current_item()

	# Add item to inventory
	def add_item(self, item):
		""" 
		Item handling 
		Add item to inventory table 
		Parameters:
		    item (object) --> Item to be added
		"""
		# If the item being added is already in the user's inventory then exit the method
		if (item in self.inventory) or (item == None):
			return
		# Insert item into inventory if it doesn't already exist
		self.game.database.insert_into_inventory_table(self.player.player_id, item.name)

	
	def remove_item(self, item):
		"""
		Remove item from inventory
		Parameters:
			item (object) --> item to be removed
		"""	
		# If invalid inventory size
		# Handle none case
		if self.inventory == None:
			return
		print(item.name)
		# Handle current item case
		if item == self.current_item:
			self.current_item = None
		self.player.game.database.delete_from_inventory_table(item.name)



  

    # Display inventory
	def display_inventory(self):
		# testing
		self.player.game.screen.fill(self.player.game.black)
		self.run_display = True
		while self.run_display:
			self.player.game.screen.fill(self.player.game.black)
			self.load_inventory()
			self.display_all_boxes()
			self.draw_inventory()
			self.draw_all_text()
			self.check_events()
			self.draw_all_buttons()
			self.player.clock.tick(60)
			pg.display.update()

class Item():
	def __init__ (self, game, name, rarity, item_type, damage, sprite_path):

		self.game = game

		self.offset_x = 410
		self.offset_y = 150


		self.name = name  
		self.rarity = rarity

		self.width = 120
		self.height = 120

		self.type = item_type 
		self.damage = damage

		self.sprite_path = sprite_path
		self.sprite_image = pg.image.load(f"{self.sprite_path}").convert_alpha()


		""" More intense colours than game colours """ 
		self.blue = (0, 255, 255)
		self.green = (156 ,255, 51)
		self.purple = (127, 0, 255)

		# Map rarity to rgb colours for icon border colour
		self.colours = {
			"Common"   : self.game.white,
			"Uncommon" : self.green,
			"Rare"     : self.blue,                # More intense blue
			"Epic"     : self.purple,
			"Legendary": self.game.gold
		}


	def get_icon(self):
		icon = pg.Surface((self.width, self.height))
		# Blit icon at x, y position <--- To be iterated through within introduction display loop
		icon.blit(self.sprite_image, (0,0))

		# Get rid of black sprite background
		icon.set_colorkey(self.game.black)
		return icon


	def set_position(self, column, row):
		self.x = self.offset_x + (column*120)
		self.y = self.offset_y + (row*120)










