import pygame as pg
from button import *
import sys
import sqlite3
from sets import banned_characters
from database import Database
from menu import *
from leaderboard import *
import hashlib

# Template for all pages, defines cololurs ect

class Page():
	def __init__(self, game):
		pg.init()

		#Colours
		self.game = game

		self.font_name = "Fonts/NexaTextDemo-Bold.ttf"
		self.font = pg.font.Font(self.font_name,32)
		self.clock = pg.time.Clock()

	def draw_text(self, text, colour, size, x, y):
		self.font = pg.font.Font("Fonts/NexaTextDemo-Bold.ttf",size)
		self.text = self.font.render(text, True, colour)
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (x,y)
		self.game.screen.blit(self.text, self.text_rect)




		# Display green background with blue template rectangle

	def display_template(self):
		self.game.screen.fill(self.game.green)
		pg.draw.rect(self.game.screen, self.game.blue, pg.Rect(450,140,800,700))


	# Check for quit

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run_display = False
				pg.quit()
				sys.exit()



# Main page displays Registration and login buttons
class MainPage(Page):
	def __init__(self, game):
		Page.__init__(self, game)

		self.game = game

		self.register = Button(self.game.navy, self.game.orange,  500, 600, 300, 200, self.font_name,  "Register")
		self.login = Button(self.game.navy, self.game.orange, 870, 600, 300, 200, self.font_name, "Login")
		self.clock = pg.time.Clock()



	# Draw all necessary text 
	def draw_all_text(self):
		self.draw_text("Welcome To Terrabyte!",self.game.white,64, 840, 200)
	
	# Draw all necessary buttons
	def draw_buttons(self):
		self.register.draw_button(self.game.screen)
		self.login.draw_button(self.game.screen)	

	# Check if register or login ubtton has been pressed
	def check_clicked(self): 
		if self.register.is_left_clicked():
			self.run_display = False
			self.game.current_page = self.game.registration_page
			self.game.registration_page.display_page()
			
		if self.login.is_left_clicked():
			self.run_display = False
			self.game.current_page = self.game.login_page
			self.game.login_page.display_page()

	# Loop to display main menu page			
	def display_page(self):
		self.run_display = True
		while self.run_display:
			self.check_events()
			self.display_template()
			self.draw_buttons()		
			self.draw_all_text()
			self.check_clicked()
			self.game.database.create_all_tables()
			self.clock.tick(60)
			pg.display.update()


class LoginRegistrationTemplate(Page):
	def __init__(self, game):
		Page.__init__(self, game)

		# Initialising database

		self.game = game

	
		# Initialise buttons , rectangles and inputs

		self.back = Button(self.game.navy, self.game.orange, 450,140,80,80, self.font_name,"Back")
		self.confirm = Button(self.game.navy, self.game.orange, 585, 720, 500, 100, self.font_name, "Confirm")
		self.username_text = ''
		self.password_text = ''
		self.password_box_rect = pg.Rect(460,600,770,50)
		self.username_box_rect = pg.Rect(460,340,770,50)
		self.username_active = False
		self.password_active = False
		self.user_surf = self.font.render(self.username_text, True, self.game.white)
		self.pass_surf = self.font.render(self.password_text, True, self.game.white)


		self.username_length = len(self.username_text)
		self.password_length = len(self.password_text)


		# Varaible to depend on whether the inputs are valid

		self.valid_username = True
		self.valid_password = True
		self.max_username = False
		self.max_password = False
		self.max_username_length = 12
		self.max_password_length = 21
		self.valid_registration = False

	def get_hash(self, string):
		hash_object = hashlib.sha256(string.encode())
		hex_dig = hash_object.hexdigest()
		return hex_dig

	def get_username(self):
		return self.username_text

	def get_password(self):
		return self.password_text

	def set_password(self, password):
		self.password_text = password

	def set_username(self, username):
		self.username_text = username

	def draw_boxes(self):
		pg.draw.rect(self.game.screen, self.game.white, self.username_box_rect, 2)
		pg.draw.rect(self.game.screen, self.game.white, self.password_box_rect, 2)

	def draw_buttons(self):
		self.back.draw_button(self.game.screen)
		self.confirm.draw_button(self.game.screen)

	def draw_all_text(self):
		self.draw_text("NAME", self.game.purple, 40, 840, 100)
		self.draw_text("Welcome To Terrabyte!", self.game.white, 40, 840, 200)
		self.draw_text("Enter Username Below", self.game.black, 34, 675, 300)
		self.draw_text("Enter Password Below", self.game.black, 34, 675, 550)


	# Update input surfaces with corrosponding user input
	def update_inputs(self):
		self.user_surf = self.font.render(self.username_text, True, self.game.white)
		self.game.screen.blit(self.user_surf, (475,340))
		self.pass_surf = self.font.render('*'* len(self.password_text), True, self.game.white)
		self.game.screen.blit(self.pass_surf, (475, 600))

	# Check if back button ahs been pressed
	def check_back(self):
		if self.back.is_left_clicked():
			self.run_display = False
			self.game.current_page = self.game.main_page
			self.game.main_page.display_page()

	## Methods to validate user inputs

	# Get length of input username

	def get_username_length(self):
		return len(self.username_text)

	def get_password_length(self):
		return len(self.password_text)

	# Validate length of username
	def check_username_length(self):
		if ((self.get_username_length() > 12) or (self.get_username_length() < 3)):
			self.valid_username = False
			self.draw_text("Invalid Username Character Amount", self.game.red, 30,830,430)
			if self.get_username_length() > self.max_username_length:
				self.max_username = True
		else:
			self.valid_username = True

	# Validate length of password 

	def check_password_length(self):
		if ((self.get_password_length() < 8) or (self.get_password_length() > self.max_password_length)):
			self.valid_password = False
			self.draw_text("Invalid Password Character Amount", self.game.red, 30, 830, 690)
			if self.get_password_length() > self.max_password_length:
				self.max_password = True
		else:
			self.valid_password = True

	# Check for banned characters
	def check_banned_characters(self, name, key):
		if key in banned_characters:
			return True
		else:
			return False


	# Perform all username sanitising procedures

	def sanitise_username(self):
		self.check_username_length()
	
	# Perform all pasword sanitising procedures
	def sanitise_password(self):
		self.check_password_length()

	# Set boolean flags to know when upper limits of inputs have been reached
	def check_upper_limits(self):
		if self.username_length < self.max_username_length:
			self.max_username = False
		if self.password_length < self.max_password_length:
			self.max_password = False
		
	def valid_inputs(self):
		if self.valid_username == True and self.valid_password == True:
			return True
		else:
			return False

	def check_events(self):
		for event in pg.event.get():

			if event.type == pg.QUIT:
				self.run_display = False
				pg.quit()
				sys.exit()
				# If mouse button is pressed then

			if event.type == pg.MOUSEBUTTONDOWN:
				# If player mouse overlaps with password box rectangle then
				if self.password_box_rect.collidepoint(event.pos):
					self.password_active = True
					self.username_active = False
				elif self.username_box_rect.collidepoint(event.pos):
					self.username_active = True
					self.password_active = False
				else:
					self.username_active = False
					self.password_active = False

			if event.type == pg.KEYDOWN:
				if self.password_active:
					if event.key == pg.K_BACKSPACE:
						self.set_password(self.password_text[:-1])
					# If max password limit reached, don't add new characters to password string
					elif self.max_password == False:			
						self.password_text += event.unicode
				if self.username_active:
					if self.check_banned_characters(self.username_text, event.key):
						self.draw_text("INVALID CHARACTER", self.game.red, 40, 800, 300)
		
					if event.key == pg.K_BACKSPACE:
						self.set_username(self.username_text[:-1])
						# If max password limit reached, don't add new characters to username string
					elif self.max_username == False:
						self.set_username(self.username_text + event.unicode)
		

	def display_page(self):
		self.run_display = True
		while self.run_display:
			self.display_template()
			self.game.screen.fill(self.game.green)
			pg.draw.rect(self.game.screen, self.game.blue, pg.Rect(450,140,800,700))
			self.draw_all_text()		
			self.draw_boxes()
			self.draw_buttons()	
			self.check_events()
			self.check_upper_limits()
			self.update_inputs()
			self.check_back()
			self.check_confirm()
			self.sanitise_username()
			self.sanitise_password()
			self.valid_inputs()
			#print("\nUsername : ", self.username_text)
			#print("Password : ", self.password_text)
			#print("Username Validity : ",self.valid_username)
			#print("Password Validity : ", self.valid_password)
			#print("Max Username Reached : ",self.max_username)
			#print("Max Password Reached : ",self.max_password)
			#print(self.get_hash(self.password_text))
			pg.display.update()

			

class RegistrationPage(LoginRegistrationTemplate):
	def __init__(self, game):
		LoginRegistrationTemplate.__init__(self, game)




	def draw_all_text(self):
		self.draw_text("Registration", self.game.purple, 40, 840, 100)
		self.draw_text("Welcome To Terrabyte!", self.game.white, 40, 840, 200)
		self.draw_text("Enter Username Below", self.game.black, 34, 675, 300)
		self.draw_text("Enter Password Below", self.game.black, 34, 675, 550)


	# Check if confirm button has been pressed
	# If confirm buton pressed, inputted values are inserted into database

	def check_confirm(self):
		# If confirm button is clicked and the inputs are validated
		if (self.confirm.is_left_clicked() and self.valid_inputs()):
			# SEND inputs to database backend for validations
			# CHECK IF USERNAME ALREADY IN DATABASE, IF SO, DISPLAY USERNAME HAS ALREADY BEEN SELECTED
			self.game.database.validate_registration(self.username_text, self.get_hash(self.password_text))

			if self.valid_registration == True:
		# IF VALID THEN

				# Display success pages
				self.game.current_page = self.game.registration_success_page
				self.game.registration_success_page.display_page()

				# Initialise menus
				self.game.control_menu = ControlMenu(self.game)
				self.game.volume_menu = VolumeMenu(self.game)
				self.game.credits_menu = CreditsMenu(self.game)
				self.game.settings_menu = SettingsMenu(self.game)
				self.game.after_life_menu = AfterLifeMenu(self.game)

				#Initialise leaderboards
				self.game.leaderboard_menu = LeaderboardMenu(self.game)

				self.game.terrarium_leaderboard = TerrariumLeaderboard(self.game)

				# Display introduction
				self.game.introduction.display_intro()
			else:
				self.draw_text("Username Already Taken", self.game.red, 34, 835, 700)
		# IF NOT VALID THAN RETURN USERNAME ALREADY EXISTS ERROR MESSAGE TO USER


	



class LoginPage(LoginRegistrationTemplate):
	def __init__(self, game):
		LoginRegistrationTemplate.__init__(self, game)

		self.valid_login = False

	def draw_all_text(self):
		self.draw_text("Login", self.game.purple, 40, 840, 100)
		self.draw_text("Welcome To Terrabyte!", self.game.white, 40, 840, 200)
		self.draw_text("Enter Username Below", self.game.black, 34, 675, 300)
		self.draw_text("Enter Password Below", self.game.black, 34, 675, 550)



	def check_confirm(self):
		""" Check if confirm button is pressed 
			Peform validation on username and password entered
			Initialise player object and menu objects
		"""

		# If confirm button is pressed and hte inputs are valid
		if (self.confirm.is_left_clicked() and self.valid_inputs()):

			#CHECK IF PASSWORD INPUTTED IS VALID WITH USERNAME IN DATABASE	
			user = self.get_username()
			pass_hash = self.get_hash(self.password_text)
			self.game.database.validate_login(user, pass_hash)

			# If username and password are correct
			if self.valid_login == True:
	
				# Load success page
				self.game.login_success_page.display_page()

				# Initialise menus
				self.game.control_menu = ControlMenu(self.game)
				self.game.volume_menu = VolumeMenu(self.game)
				self.game.credits_menu = CreditsMenu(self.game)
				self.game.settings_menu = SettingsMenu(self.game)
				self.game.after_life_menu = AfterLifeMenu(self.game)

				#Initialise leaderboards
				self.game.leaderboard_menu = LeaderboardMenu(self.game)
				self.game.terrarium_leaderboard = TerrariumLeaderboard(self.game)

				# Display main menu
				self.game.main_menu.display_menu()

				# Stop running display
				self.run_display = False
			else:
				# Raise invalid attempt
				self.draw_text("Invalid Login Attempt", self.game.red, 34, 835, 700)

	def display_page(self):
		self.run_display = True
		while self.run_display:
			self.display_template()
			self.game.screen.fill(self.game.green)
			pg.draw.rect(self.game.screen, self.game.blue, pg.Rect(450,140,800,700))
			self.draw_all_text()		
			self.draw_boxes()
			self.draw_buttons()	
			self.check_events()
			self.check_upper_limits()
			self.update_inputs()
			self.check_back()
			self.check_confirm()
			self.sanitise_username()
			self.sanitise_password()
			#self.game.player.display_player()
			self.valid_inputs()


			"""
			print("\nUsername : ", self.username_text)
			print("Password : ", self.password_text)
			print("Username Validity : ",self.valid_username)
			print("Password Validity : ", self.valid_password)
			print("Max Username Reached : ",self.max_username)
			print("Max Password Reached : ",self.max_password)
			"""
			pg.display.update()

class RegistrationSuccessPage(Page):
	def __init__ (self, game):
		Page.__init__(self, game)

	def count(self):
		pg.time.wait(2000)
		self.run_display = False
		self.current_page = self.game.main_page
		# After succesfful registration, display introduction


	def draw_all_text(self):
		self.draw_text("Welcome To Terrabyte!",self.game.white,64, 840, 200)
		self.draw_text("Success!", self.game.green, 64, 840, 400)
		self.draw_text("You have succesffuly registered :)", self.game.green, 34, 840, 500)

	def display_page(self):
		self.run_display = True
		while self.run_display:
			self.start_counting = True	
			self.check_events()
			self.display_template()
			self.draw_all_text()
			pg.display.update()
			self.count()



class LoginSuccessPage(Page):
	def __init__ (self, game):
		Page.__init__(self, game)

	def count(self):
		pg.time.wait(1000)
		self.run_display = False
		print("Introduction display")
		# Initiate introduction

	def display_all_text(self):
		self.draw_text("Welcome To Terrabyte!",self.game.white,64, 840, 200)
		self.draw_text("Success!", self.game.green, 64, 840, 400)
		self.draw_text("You have succesffuly logged in :)", self.game.green, 34, 840, 500)
		self.draw_text("Prepare yourself for the world of TERRABYTE!",self.game.red, 16, 840, 600 )


	def display_page(self):
		self.run_display = True
		while self.run_display:
			self.start_counting = True
			self.check_events()
			self.display_template()
			self.display_all_text()
			pg.display.update()
			self.count()
		

