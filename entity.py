import pygame as pg
from inventory import Inventory, Item
import random
from menu import AfterLifeMenu

class Entity():
	def __init__(self, game, x, y, display_name, max_health, scale, sprite_path):

		self.game = game

		self.display_name = display_name
		self.max_health = max_health
		self.scale = scale
		self.sprite_path = sprite_path
		self.health = max_health


		self.width = 32
		self.height = 32
		self.x = x  
		self.y = y
		self.dead = False
		self.run_display = True

		""" Sprite attributes """
		# Load spritesheet images
		self.sprite_sheet_image = pg.image.load(f"{self.sprite_path}").convert_alpha()
		self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
		self.frame = 0 
		self.cooldown = 150
		self.touching_wall = False

		self.motion = ""
		self.facing = ""

		self.speed = 2
		self.base_speed = 2



		self.animation_list = []


		self.last_update = pg.time.get_ticks()  # Get time of list initialisation
		self.clock = pg.time.Clock()
		self.rect = pg.Rect(self.x, self.y, self.width*self.scale, self.height*self.scale)



	def set_health(self, health):	
		self.health = health

	def get_health(self):
		return self.health

	def set_dead(self, dead):
		self.dead = dead

	def reset_health(self):
		self.health = self.max_health

	def screen_boundary_collision(self):
		""" Check if entity is colliding with boundary
			Returns descriptions of which part of the screen was hit 
				True        --> Boundary collision
				Fasle       --> No boundary collision
				self.facing --> Position entity was facing at the time of a boundary collision

		"""
		if (self.rect.x < 0) or (self.rect.x > (self.game.display_x - self.rect.width)) or (self.rect.y < 0) or (self.rect.y > (self.game.display_y - self.rect.height)):
			return (True, self.facing)
		return False


	""" Check for player touching border of screen """
	def check_boundaries(self):
		if (self.rect.y - self.speed <= 0): # If moving left causes rect to cross left border 
			self.rect.y += self.speed    # Keep rect within border

		if self.rect.y + self.speed >= (self.game.display_y - (self.height * self.scale)): # If moving down causes rect to cross bottom border
			self.rect.y -= self.speed    # Keep rect within border

		if self.rect.x - self.speed <= 0:	# If moving right causes rect to cross right border
			self.rect.x += self.speed    # Keep rect within border

		if self.rect.x + self.speed >= (self.game.display_x - (self.width * self.scale)):  # If moving right causes rect to cross right border
			self.rect.x -= self.speed    # Keep rect within border
	

	# Draw text to midtop
	def draw_text(self, text, colour, size, x, y):
		self.font = pg.font.Font(self.game.main_menu.font_name, size)
		self.text = self.font.render(text, True, colour)
		self.text_rect = self.text.get_rect()
		# Format text to appear above sprite
		self.text_rect.center = (x + self.width,y - 10)
		self.game.screen.blit(self.text, self.text_rect)


	# Take damage from an entity
	def take_damage(self, damage):
		if self.health == 0:
			return
		self.set_health(self.health - damage)

	def set_speed(self, speed):
		self.speed = speed 

	def get_speed(self):
		return self.speed

	def set_level(self, level):
		self.level = level 

	def get_facing(self):
		return self.facing

	def get_level(self):   
		return self.level

	def clear_animation_list(self):
		self.animation_list = []

	# Check if hp goes below 0 
	def check_health(self):
		if self.health <= 0:
			self.dead = True
			self.health = 0
		else:
			self.dead = False

	def get_animation_list(self):
		return self.animation_lists

	def set_attack_rect_x(self, x):
		self.attack_rect.x = x 

	def set_attack_rect_y(self, y):
		self.attack_rect.y = y

	def get_rect(self):     # Get rect object
		return self.rect

	def set_rect_x(self, x): # Set rectangle x coordinate
		self.rect.x = x 

	def get_rect_x(self):   # Get rectangle x coordinate
		return self.rect.x

	def set_rect_y(self, y): # Set rectangle y coordinate
		self.rect.y = y 

	def get_rect_y(self): # Get rectangle y coordinate 
		return self.rect.y

	def set_motion(self, motion):
		self.motion = motion 

	def get_motion(self):
		return self.motion

	def set_facing(self, facing):
		self.facing = facing 

	def get_facing(self):
		return self.facing


	def set_display_name(self, display_name):
		self.display_name = display_name

	def set_frame(self, frame):
		self.frame = frame


	def set_keybinds(self): 
		self.reset_keys()


	""" Draw health bar above entity """
	def draw_health_bar(self):
		# Don't display health bar if dead
		if self.dead:
			return
		# Get width of bar
		health_width = int(self.rect.width * (self.health/self.max_health))
		# Rects placed slightly above entity rect
		health_rect = pg.Rect(self.rect.x, self.rect.y-40, health_width, 10)
		border_rect = pg.Rect(self.rect.x, self.rect.y-40, health_width, 10)
		# Set health bar colour as green
		bar_colour = self.game.green

		# If health less than 70%, change colour to yellow
		if self.health < self.max_health * 0.7:
			bar_colour = self.game.yellow
		# If below 30% change colour to red
		if self.health < self.max_health * 0.3:
			bar_colour = self.game.red

		# Draw rects
		pg.draw.rect(self.game.screen, bar_colour, health_rect)
		pg.draw.rect(self.game.screen, self.game.white, border_rect, 2)

	""" Draw character to screen """
	def draw_to_screen(self, screen):
		self.draw_text(self.display_name, self.game.white, 20, self.rect.x, self.rect.y,)
		self.draw_health_bar()
		pg.draw.rect(self.game.screen, self.game.red, self.rect, 2)  # Hitbox
		self.get_animation(self.rect)  # Iterate through frames in current animation_list



	def set_animation_list(self , row, length, reverse): 
		""" 
		Change animation_list depending on type of animation 
		Parameters:
			row     (int) --> which row of sprite sheet 
			length  (int)  --> how many frames in animation
			reverse (int) --> should the display be flipped? e.g left frames flip to mimic right frames
		"""
		self.clear_animation_list()
		# Append wanted frames to animation list
		# Row index, length of animation in frames
		for i in range (length):
			self.animation_list.append(self.sprite_sheet.get_frame(row, i, self.width, self.height, self.scale, self.game.black, reverse))
			pg.time.delay(2)  # buffer
																								   



	""" Display and Iterate through animation_list """
	def get_animation(self, rect):	
		self.game.screen.blit(self.animation_list[self.frame], (self.rect.x,self.rect.y))   # Display frame to screen
		self.current_time = pg.time.get_ticks() 				   # Get current time
		if self.current_time - self.last_update >= self.cooldown:  # If 500ms have passed since last frame then
			self.frame += 1										   # Go to next frame
			self.last_update = self.current_time
		if self.frame >= len(self.animation_list):  			   # If the end of the animation frames is reached then
			self.set_frame(0)                                      # Return to first frame


	""" move rect """
	def movement(self, direction, speed):
		if direction == "Up":
			self.rect.y -= speed 	# Move character up

		if direction == "Down":
			self.rect.y += speed    # Move character down

		if direction == "Left":
				self.rect.x -= speed    # Move character left

		if direction == "Right":
			self.rect.x += speed    # Move character right


	""" Check if user quits """
	def check_quit(self, event_type):
		if event_type == pg.QUIT:
			self.run_display = False
			pg.quit()


"""Extract frames from spritesheet """
class SpriteSheet():
	def __init__(self,sheet_image):
		self.sheet_image = sheet_image

	""" Get pg surface for sprite """
	def get_frame(self, row, frame_number, width, height, scale, transparency, reverse = False):
		pg.init()
		
		frame = pg.Surface((width, height)) # Create frame surface for sprite
		
		frame.blit(self.sheet_image, (0,0), ((frame_number*width, row*height, width, height)))  # Blit spriteshseet onto frame surface at origin
																				 # 3rd argument specifies what area of the spritesheet to blit to frame
																				 # frame_number skips to correct animation frame within spritesheet
																				 # row specifies which row of sprtesheet
		frame = pg.transform.scale(frame, (width* scale, height*scale))	 # Multiply width and height px limits by scalar
		frame.set_colorkey(transparency) # Make 'transparency' colours invisible

		if reverse == False:   # If the frame isn't to be reversed
			return frame       # Simply return the frame
		else:
			frame = pg.transform.flip(frame, True, False)    # Else, reverse the frame
			return frame
			

class Player(Entity):
	def __init__ (self, game, username, display_name, max_health, score, scale, player_level, map_level, sprite_path, player_id=None, inventory_id=None):
		Entity.__init__(self, game, 0, 0, display_name, max_health, scale, sprite_path)

		# Load spritesheet images
		
		self.username = username
		self.player_level = player_level
		self.inventory_id = inventory_id
		self.map_level = map_level
		self.score = score
		self.player_id = player_id

		self.motion = "Idle Left"
		self.facing = "Right"   # Track which way character is facing


		self.current_level = self.game.levels[self.map_level]
		self.inventory = Inventory(self)

		self.time = 0

		# Creating attack extension hitbox
		self.extension = 40
		self.attack_rect = pg.Rect(self.x, self.y, (self.width * self.scale) + self.extension, (self.height * self.scale) + self.extension)
		# Centering attack_rect to player rect
		self.attack_rect.center = self.rect.center
		self.attacking = False

		self.initial_rect = self.rect 
		self.initial_attack_rect = self.attack_rect
		self.attack = 1   # This will be set to the current item held in inventory's attack power


	def add_score(self, score):
		self.score += score

	def reset_score(self):
		self.score = 0

	def get_score(self):
		return self.score 

	def get_attack(self):
		return self.attack 

	def set_attack(self, attack):
		self.attack = attack

	# Respawn at origin
	def spawn_at_origin(self):
		self.set_rect_x(0)
		self.set_rect_y(0)
		self.set_attack_rect_x(0)
		self.set_attack_rect_y(0)




	# Fix attack hitbox
	def centre_attack_rect(self):
		self.attack_rect.center = self.rect.center

	""" Check for player touching border of screen """
	def check_boundaries(self):
	
		if (self.rect.y - self.speed <= 0): # If moving left causes rect to cross left border 
			self.rect.y += self.speed    # Keep rect within border

		if self.rect.y + self.speed >= (self.game.display_y - (self.height * self.scale)): # If moving down causes rect to cross bottom border
			self.rect.y -= self.speed    # Keep rect within border

		if self.rect.x - self.speed <= 0:	# If moving right causes rect to cross right border
			self.rect.x += self.speed    # Keep rect within border

		if self.rect.x + self.speed >= (self.game.display_x - (self.width * self.scale)):  # If moving right causes rect to cross right border
			self.rect.x -= self.speed    # Keep rect within border

	def set_attacking(self, boolean):
		self.attacking = boolean

	def get_attacking(self):
		return self.attacking

	""" Draw character to screen """
	def draw_to_screen(self, screen):
		# Fix attack hitbox about the centre of player
		self.centre_attack_rect()
		self.draw_text(self.display_name, self.game.white, 20, self.rect.x, self.rect.y,)
		self.draw_health_bar()
		# draw hitbox and rect
		pg.draw.rect(self.game.screen, self.game.red, self.rect, 2)  
		pg.draw.rect(self.game.screen, self.game.blue, self.attack_rect, 2)	 # hitbox rect
		self.get_animation(self.rect)  # Iterate through frames in current animation_list

	def movement(self, direction, speed):
		""" move rect and attack hitbox """
		if direction == "Up":
			self.rect.y -= speed 	# Move character up
			self.attack_rect.y -= speed

		if direction == "Down":
			self.rect.y += speed    # Move character down
			self.attack_rect.y += speed

		if direction == "Left":
			self.rect.x -= speed    # Move character left
			self.attack_rect.x -= speed

		if direction == "Right":
			self.rect.x += speed    # Move character right
			self.attack_rect.x += speed

	""" Change animation_list depending on type of animation """
	def set_animation_list(self ,row, length, reverse): 
			
		
		for i in range (length):
			self.animation_list.append(self.sprite_sheet.get_frame(row, i, 32, 32, self.scale, self.game.black, reverse)) # Append wanted frames 
																								   # to animation list
		if (row == 0) and (self.sprite_path == 'Assets/Sprites/Player/HoodedProtagonist.png'):
			self.animation_list.append(self.sprite_sheet.get_frame(1, 0, 32, 32, self.scale, self.game.black, reverse))
			self.animation_list.append(self.sprite_sheet.get_frame(1, 1, 32, 32, self.scale, self.game.black, reverse))



	def set_username(self, username):
		self.username = username

	def get_username(self):
		return self.username 

		""" Set all keybinds 'pressed' bool to False """
	def reset_keys(self):
		for key in self.game.control_menu.keybinds:
			key.reset_key()

	

	""" Set animation list frames """
	def set_idle_right_animation(self):
		self.set_animation_list(0, 2, False)

	def set_idle_left_animation(self):
		self.set_animation_list(0, 2, True)

	def set_right_animation(self):
		self.set_animation_list(3, 8, False)

	def set_left_animation(self):
		self.set_animation_list(3, 8, True)

	def set_down_right_animation(self):
		self.set_animation_list(4, 6, False)

	def set_down_left_animation(self):
		self.set_animation_list(4, 6, True)

	def set_up_right_animation(self):
		self.set_animation_list(5, 8, False)

	def set_up_left_animation(self):
		self.set_animation_list(5, 8, True)

	def set_attack_left_animation(self):
		self.set_animation_list(8, 8, False)

	def set_attack_right_animation(self):
		self.set_animation_list(8, 8, True)

	def set_death_right_animation(self):
		self.set_animation_list(7, 8, False)

	def set_death_left_animation(self):
		self.set_animation_list(7, 8, True)

	""" Animation events """
	def idle_right_animation(self):	
		self.set_idle_right_animation()

	def idle_left_animation(self):
		self.set_idle_left_animation()
	
	def right_animation(self):
		self.set_right_animation()

	def left_animation(self):
		self.set_left_animation()

	def up_left_animation(self):
		self.set_up_left_animation()

	def up_right_animation(self):
		self.set_up_right_animation()

	def down_left_animation(self):
		self.set_down_left_animation()

	def down_right_animation(self):
		self.set_down_right_animation()

	def attack_animation(self):
		self.set_attack_animation()

	def death_animation(self):
		self.set_death_animation()

	""" Control which animations to set"""
	def control_animations(self):
		self.clear_animation_list()   # Empty animation list
		if self.get_motion() == "Idle Right":  # If character is idle
			self.idle_right_animation()        # Set animation list to idle frames

		if self.get_motion() == "Idle Left":
			self.idle_left_animation()

		if self.get_motion() == "Right": # If character is moving right
			self.right_animation()       # Set animation list to moving right frames

		if self.get_motion() == "Left": # If character is moving left
			self.left_animation()       #  Set animation list to moving left frames

		if self.get_motion() == "Down Right":  # If character is moving down while facing right
			self.down_right_animation()        # Set aniamation list to moving down while facing right

		if self.get_motion() == "Down Left":   # If character is moving down while facing left
			self.down_left_animation()		   # Set aniamation list to moving down while facing left

		if self.get_motion() == "Up Right":    # If character is moving up while facing right
			self.up_right_animation()		   # Set aniamation list to moving up while facing right

		if self.get_motion() == "Up Left":     # If character is moving ip while facing right
			self.up_left_animation()		   # Set aniamation list to moving up while facing left



	""" Handle movement events"""
	def check_movements(self):
		if self.touching_wall == False:    
			self.check_boundaries()
			self.control_animations()  # Set animation frames
			""" Carry out keybind function """
			if self.game.control_menu.up_keybind.get_pressed():    
				self.movement("Up",self.speed)

			if self.game.control_menu.down_keybind.get_pressed():
				self.movement("Down",self.speed)

			if self.game.control_menu.left_keybind.get_pressed():
				self.movement("Left",self.speed)

			if self.game.control_menu.right_keybind.get_pressed():
				self.movement("Right",self.speed)

		else:
			""" Displace character to valid area on the map """
			""" By moving rect in opposite direction to keybind """
			if self.game.control_menu.up_keybind.get_pressed():
				self.movement("Down",self.speed*2)

			if self.game.control_menu.down_keybind.get_pressed():
				self.movement("Up",self.speed*2)

			if self.game.control_menu.left_keybind.get_pressed():
				self.movement("Right",self.speed*2)

			if self.game.control_menu.right_keybind.get_pressed():
				self.movement("Left",self.speed*2)


	""" Check user events """
	def check_events(self):
		self.check_movements()

	""" Display player """
	def display_player(self):
		self.draw_to_screen(self.game.screen)
		self.check_events()
		self.check_health()


		#print(self.last_pos)
		"""
		print("\nUp : ", self.game.control_menu.up_keybind.get_pressed())
		print("Down : ", self.game.control_menu.down_keybind.get_pressed())
		print("Left : ", self.game.control_menu.left_keybind.get_pressed())
		print("Right : ", self.game.control_menu.right_keybind.get_pressed())
		print("Rect y : ", self.rect.y)
		print("Rect x : ", self.rect.x)
		print("Boundary x : 1600 | Boundary y : 960")	
		"""
class Enemy(Entity):
	def __init__ (self, game, x, y, display_name, attack, max_health, points, scale, sprite_path):
		Entity.__init__(self, game, x, y, display_name, max_health, scale, sprite_path)


		self.attack = attack
		self.points = points
		self.facing_list = ["Up","Left","Down","Right"]

	# FUTURE ME , add common enemy methods and attributes

class BrainMoleMonarch(Enemy):
	def __init__(self, game, x, y, display_name, attack, max_health, points, scale, sprite_path):
		Enemy.__init__(self, game, x, y, display_name, attack, max_health, points, scale, sprite_path)

		self.facing = "Left"
		# List of possible movements
		# Keep track of ticks
		self.move_count = 0
		
	""" Check/Sequence mob events """
	def check_events(self):
		self.check_movements()

	def reverse_movement(self, direction):
		""" 
		Reverse entity movement and move player 2px in reversed direction
		Parameters:
			direction --> direction in which entity was facing at the moment of screen collision
		"""
		if direction == "Left":
			self.set_facing("Right")
			self.rect.move_ip(2, 0)

		if direction == "Right":
			self.set_facing("Left")
			self.rect.move_ip(-2, 0)

		if direction == "Up":
			self.set_facing("Down")
			self.rect.move_ip(0, 2)

		if direction == "Down":
			self.set_facing("Up")
			self.rect.move_ip(0, -2)

	""" Control mob periodical movementes, animations and attacks """

	def check_movements(self):
		# Move mole according to direction it's facing
		self.check_collisions()

		self.move_count += 1
		if self.move_count >= 60:
			# Move enemy in random direction every 3sec
			if random.random() < 0.8: # 80% chance of random movement
				# Random movement
 				self.set_facing(self.facing_list[random.randint(0,3)])
			self.move_count = 0

		if self.get_facing() == "Right":
			self.movement("Right", self.speed) 
			self.set_animation_list(0, 4, False) 

		if self.get_facing() == "Left":
			self.movement("Left", self.speed)
			self.set_animation_list(0, 4, True)

		if self.get_facing() == "Up":
			self.movement("Up", self.speed)

		if self.get_facing() == "Down":
			self.movement("Down", self.speed)


		# If collision with screen
		#print("\nCollision : ", self.screen_boundary_collision())
		#print("Speed : ", self.speed)
		#print("Mole rect x coordinate : ", self.rect.x)
		if self.screen_boundary_collision():
			# Reverse movement
			self.reverse_movement(self.screen_boundary_collision()[1])



	def check_collisions(self):
		"""
		Handles collisions between stationary objects
		"""
		water_rects = self.game.get_current_level().water_rects
		wall_rects = self.game.get_current_level().wall_rects

		# If entity collides with any water tiles then
		if self.rect.collidelist(water_rects) != -1:
			# Reduce speed to a minimum
			self.set_speed(1)
		else:
			# Restore base speed
			self.set_speed(self.base_speed)

		# If entity collides with any wall rects then
		if self.rect.collidelist(wall_rects) != -1:
			# Reverse direction of entity
			self.reverse_movement(self.facing)
			self.set_speed(1)


		# If enemy colllides with player then

		if self.rect.colliderect(self.game.player.rect):
			self.game.player.take_damage(self.attack)
			# Deduct health points from player according to attack attribute

		# If enemy collides with attack hitbox and the player is attacking 
		if (self.rect.colliderect(self.game.player.attack_rect)) and (self.game.player.attacking):
			# take damage
			self.take_damage(self.game.player.attack)

	""" Main display loop """
	def display_enemy(self):
		self.check_events()
		self.check_health()
		self.draw_to_screen(self.game.screen)




