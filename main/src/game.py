import pygame as pg
from button import *
import sys
from login import *
from database import Database
from introduction import *
from boombox import *

from menu import *
from leaderboard import *

from levels import Level
from entity import Player
from inventory import Inventory

class Game():
	def __init__(self):

		pg.display.set_caption("Terrabyte")
		# Colours	
		self.clock = pg.time.Clock()
		self.black = (0, 0, 0)
		self.purple = (135, 56, 199)
		self.green = (125, 180, 108)
		self.beige = (222, 175, 33)
		self.pink = (245, 190, 219)
		self.navy = (0, 62, 123)
		self.orange = (234, 89, 42)
		self.blue = (171, 214, 223)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.brown = (59,29,0)
		self.yellow = (255, 239, 0)

		self.gold = (255,215,0)
		self.silver = (192,192,192)
		self.bronze = (205, 127, 50)

		self.display_x = 1600
		self.display_y = 960
		self.mid_x = self.display_x // 2
		self.mid_y = self.display_y // 2
		self.screen = pg.display.set_mode((self.display_x,self.display_y))

		#Fonts
		self.pixel_font_name = "Fonts/DigitalDisco.ttf"

		#Objects
		self.main_page = MainPage(self)
		self.current_page = self.main_page
		self.registration_page = RegistrationPage(self)
		self.login_page = LoginPage(self)
		self.login_success_page = LoginSuccessPage(self)
		self.registration_success_page = RegistrationSuccessPage(self)
		self.database = Database(self)
		self.database.create_all_tables()
		self.introduction = Introduction(self)
		self.boombox = Boombox(self)

		# Menu objects 
		self.main_menu = MainMenu(self)
		self.control_menu = None
		self.volume_menu = None
		self.credits_menu = None
		self.settings_menu = None

		self.after_life_menu = None
		self.leaderboard_menu = None
		self.terrarium_leaderboard = None


		self.levels = {}
		self.current_level = None
		self.player = None
		self.load_levels()


		# All items
		self.all_items = []
		self.max_items = None

		# Items split by rarity
		self.common_items = []
		self.uncommon_items = []
		self.rare_items = []
		self.epic_items = []
		self.legendary_items = []

		# Assign drop rates to weapons (dr*10)%
		self.drop_rates = {
			"Common"   : 0.5, #
			"Uncommon" : 0.1, 
			"Rare"     : 0.07, 
			"Epic"     : 0.03,
			"Legendary": 0.005 
		}

		# Map rarity to rgb colours for icon border colour
		self.rarity = ["Common","Uncommon","Rare","Epic","Legendary"]


	def get_rarity_list(self, rarity):
		""" 
		Get item list corrosponding to rarity
		Parameters:
			rarity (str) --> rarity of item
		"""
		if rarity == "Common":
			return self.common_items
		if rarity == "Uncommon":
			return self.uncommon_items
		if rarity == "Rare":
			return self.rare_items
		if rarity == "Epic":
			return self.epic_items 
		if rarity == "Legendary":
			return self.legendary_items

	
	""" Initialise level objects in dictioanry levels{} """
	def load_levels(self):
		max_level = self.database.get_max_map_level()

		for i in range (1, max_level+1):   ## Number of levels (only 1 currently)
			# Get data for level
			data = self.database.get_level_data(i)
			if data != None:
				# Extract data from database
				map_name = data[0]
				time_limit = data[1]
				tmx_path = data[2]
				level_object = Level(self, i, map_name, time_limit, tmx_path)
				# Add level to dictionary
				self.levels[i] = level_object
			else:
				return

	""" Get level data for given map """
	def get_level_data(self, level):
		""" *
		level --> level (primary key) for which the data is to be extracted 
		"""
		data = self.database.get_level_data(level)
		# If map data for that level number exists then
		if data != None:
			# Extract data 
			map_name = data[0]
			time_limit = data[1]
			tmx_path = data[2]
			# Create new level with data
			level_object = Level(self, level, map_name, time_limit, tmx_path)
			# Return object
			return level_object	





	def set_current_level(self, current_level):
		self.current_level = current_level

	def get_current_level(self):
		return self.levels[self.player.map_level]

	# Draw text top screen
	def draw_text(self, text, colour, size, x, y):
		self.font = pg.font.Font(self.pixel_font_name,size)
		self.text = self.font.render(text, True, colour)
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (x,y)
		self.screen.blit(self.text, self.text_rect)

	
	def play_audio(self, filename):
		pg.mixer.music.load(filename)
		pg.mixer.music.play()
		pass

	def stop_audio(self):
		pg.mixer.music.stop()
