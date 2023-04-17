import pygame as pg
from pygame import mixer
from pygame.locals import *
from sets import banned_characters
from button import Button
import string


class Introduction():
	def __init__(self, game):

		self.game = game
		self.run_display = False
		self.display_name = ""
		self.banned_characters = {pg.K_COLON, pg.K_SEMICOLON, pg.K_LESS, pg.K_EQUALS, pg.K_GREATER< pg.K_QUESTION, pg.K_AT, pg.K_LEFTBRACKET, pg.K_RIGHTBRACKET, pg.K_CARET, pg.K_UNDERSCORE, pg.K_BACKQUOTE}
		self.banned_unicode_characters = {ord(char) for char in map(chr, banned_characters)}
		self.font_name = "Fonts/DigitalDisco.ttf"
		self.max_length = 10
		self.min_length = 4
		self.banned_char = False
		self.valid_name = False

		self.allowed_characters = list(string.ascii_letters)
		self.is_valid = None
		self.reason = ""

		# Create confirm button
		self.confirm = Button(self.game.black, self.game.green, 585, 720, 500, 100, self.font_name, "Confirm")


	def get_display_name(self):
		return self.display_name 

	def draw_text(self, text, colour, size, x, y):
		self.font = pg.font.Font(self.font_name,size)
		self.text = self.font.render(text, True, colour)
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (x,y)
		self.game.screen.blit(self.text, self.text_rect)

	def draw_input_box(self):
		box = pg.Rect(self.game.display_x/4, self.game.mid_y, self.game.mid_x, 150)
		pg.draw.rect(self.game.screen, self.game.white, box, 4)

	def set_name(self, name):
		self.display_name = name
    
	def set_state(self, state):
		self.state = state

	# Check if max length reached
	def has_max_length(self):
		if (len(self.display_name)) >= 10:
			return True
		else:
			return False
			
			
	# Check if input is in banned character set
	def has_banned_characters(self):
		for character in self.display_name:
			if character not in self.allowed_characters:
				return True
			
		return False


	# Check validity of input
	def check_validity(self, name, next_char, key):
		"""
		Params:
			name      --> string of current name
			next_char --> next key input
			event key       --> current key input
			"""
		if key != pg.K_BACKSPACE:
			if len(name + next_char) < self.min_length:
				return (False, "Insufficient Characters")

			if len(name + next_char) > self.max_length:
				return (False, "Max Length")

			if next_char not in self.allowed_characters:
				return (False, "Invalid Character")

		return (True, None)
		

	# Display all buttons
	def draw_buttons(self):
		self.confirm.draw_button(self.game.screen)
	

    # Display input in text box
	def show_name(self):
		font = pg.font.Font("Fonts/DigitalDisco.ttf", 120)
		name_surf = font.render(self.display_name, True, self.game.white)
		name_rect = name_surf.get_rect()
		self.game.screen.blit(name_surf, (self.game.display_x/4 + 30, self.game.mid_y + 20))


	""" Check if the confirm button has been pressed """
	def check_confirm(self):
		# If confirm button has been pressed and user entry is valid
		if self.confirm.is_left_clicked() and self.is_valid:

			# Update player's display_name in database
			self.game.database.update_player_table("display_name", self.display_name, self.game.player.player_id)
			self.game.player.set_display_name(self.display_name)
			
			# Display main menu
			self.game.main_menu.display_menu()
			# Stop running introduction
			self.run_display = False
			






	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				self.run_display = False
				

			if event.type == pg.KEYDOWN:
				self.game.screen.fill(self.game.black)
				self.result = self.check_validity(self.display_name, event.unicode, event.key)
				print(event.unicode)
				self.is_valid = self.result[0]  # Is username valid
				self.reason =  self.result[1]   # If not valid, what error msg

				if event.key == pg.K_BACKSPACE:
					self.game.screen.fill(self.game.black)
					self.set_name(self.display_name[:-1])

				elif self.is_valid:
					self.game.screen.fill(self.game.black)
					self.set_name(self.display_name + event.unicode)
				else:
					self.game.screen.fill(self.game.black)
					if self.reason == "Max Length":
						self.draw_text("MAXIMUM CHARACTERS REACHED", self.game.red, 40, self.game.mid_x, self.game.mid_y + 200)
					if self.reason == "Invalid Character":
						self.draw_text("INVALID CHARACTER", self.game.red, 40, self.game.mid_x, self.game.mid_y + 200)
					if self.reason == "Insufficient Characters":
						self.draw_text("INSUFFICIENT CHARACTERS", self.game.red, 40, self.game.mid_x, self.game.mid_y + 200)
						self.set_name(self.display_name + event.unicode)
	



	def draw_all_text(self):
		self.draw_text("WELCOME TO TERRABYTE", self.game.white, 60,  self.game.mid_x, self.game.mid_y - 300)
		self.draw_text("ENTER YOUR DESIRED DISPLAY NAME", self.game.white, 40, self.game.mid_x, self.game.mid_y - 100)
		self.draw_text("CONFIRM", self.game.white, 40 , self.game.mid_x, self.game.mid_y + 300)


	def display_intro(self):
		self.run_display = True
		self.game.boombox.play_intro()
		self.game.screen.fill(self.game.black)
		while self.run_display:
			self.draw_input_box()
			self.check_events()
			self.check_confirm()
			self.show_name()  
			self.draw_all_text()
			self.draw_buttons()
			pg.display.update()


			
