# BUTTON CLASS INSPIRED BY CD CODES ON YOUTUBE 
import pygame as pg



class Button():
    pg.init()
    def __init__(self, colour, hov_colour, x, y, width, height, font=" ", text=" "):
        self.og_colour = colour
        self.hov_colour = hov_colour
        self.colour = colour
        self.x = x   
        self.y = y   
        self.top_rect = pg.Rect(x, y, width, height)
        self.width = width   
        self.height=  height  
        self.font = font
        self.text = text
        self.pressed = False
        self.max_value = 1
        self.value = 0


	# DRAW BUTTON
    def draw_button(self, screen):
        pg.draw.rect(screen, self.colour, self.top_rect)
        font = pg.font.Font(self.font, 32)
        text = font.render(self.text, 1, (255,255,255))
        # centre text in middle of button
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        self.check_events()

    def is_left_clicked(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                return True


    # Check if right mouse is clicked
    def is_right_clicked(self):
        mouse_pos = pg.mosuse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[2]:
                return True
    
    # Check if left mouse is clicked     
    def is_left_clicked(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                return True


    # Check if right mouse is clicked
    def is_right_clicked(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[2]:
                return True

	# CHECK IF HOVERING    
    def check_events(self):                
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):    # if mouse on button and left button clciked then
            self.colour = (self.hov_colour)  # orange
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.colour = self.og_colour


class Slider(Button):
    def __init__(self,colour, hov_colour, x, y, width, height, font, text, box_rect):
        self.box_rect = box_rect
        Button.__init__(self, colour, hov_colour, x, y, width, height, font, text="")
        self.offset_x = 0


        self.min_value = 0
        self.volume = 0
        self.max_value = 1


    def get_volume(self):
    	return self.volume 

    def set_volume(self, volume):
    	self.volume = volume

    def get_percentage(self):
        percentage = self.get_volume() * 100
        return int(percentage)

    def update_position(self, new_x):
        self.x = new_x
        self.top_rect.x = new_x

    # Input box_rect rect as arg # Checks whether slider boundaries are less than box_rect boundaries
    def check_boundary(self, box_rect):
        if self.top_rect.right <= box_rect.right and self.top_rect.left >= box_rect.left:
            return True
        return False
        
    def draw_button(self, screen):
        pg.draw.rect(screen, self.colour, self.top_rect)
        font = pg.font.Font(self.font, 32)
        text = font.render(self.text, 1, (255,255,255))
        #centre text
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        self.check_boundary(self.box_rect)


   

    def check_events(self, event_list):
        mouse_pos = pg.mouse.get_pos()
        new_x = self.x

        if self.top_rect.collidepoint(mouse_pos):
            self.colour = self.hov_colour
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                self.offset_x = mouse_pos[0] - self.x
            else:
                #Resetting pressed variable after one click
                if self.pressed == True:
                    self.pressed = False
        else:
            self.colour = self.og_colour
        # If slider is pressed, change x coordinate accordingly setting limits at each side of the box_rect.
        if self.pressed:
            for event in event_list:
                if event.type == pg.MOUSEBUTTONUP:
                    self.pressed = False
                if event.type == pg.MOUSEMOTION:
                    new_x = mouse_pos[0] - self.offset_x
                    if self.check_boundary(self.box_rect):
                        if new_x <= self.box_rect.left:
                            new_x = self.box_rect.left
                        elif new_x + self.width >= self.box_rect.right:
                            new_x = self.box_rect.right - self.width
                    self.update_position(new_x)

class Keybind(Button):
    def __init__(self, colour, hov_colour, x, y, width, height, keybind_name, keybind_key, game):
        self.keybind_key = keybind_key
        self.keybind_name = keybind_name
        self.key_code = pg.key.key_code(keybind_key)
        self.changing = False
        self.font_name = "Fonts/DigitalDisco.ttf"
        self.game = game

        self.pressed = False   # Is keybind pressed
        Button.__init__(self, colour, hov_colour, x, y, width, height, font = "", text="")


    def get_pressed(self):
        return self.pressed

    def set_pressed(self, boolean):
        self.pressed = boolean

    def reset_key(self):
        self.set_pressed(False)

    def set_keybind_key(self, keybind_key):
        self.keybind_key = keybind_key
        
    def get_keybind_key(self):
        return self.keybind_key

    def set_key_code(self, code):
        self.key_code = code 

    def get_key_code(self):
        return self.key_code


    """ Changes displayed keybind """
    def check_for_change(self, event_list, all_keybind_keys):
        for event in event_list:
            if event.type == pg.KEYDOWN:
                # Get the character for input
                keybind_character = pg.key.name(event.key)
                # If the keybind given is already an existing keybind then
                if (keybind_character in all_keybind_keys):

                    self.game.control_menu.invalid_keybind = True   # Invalid keybind given
                    self.changing = False
                else:
                    self.game.control_menu.invalid_keybind = False  #  Valid keybind given
                    self.set_keybind_key(keybind_character)         #  Set keybind key character to the one given
                    self.set_key_code(pg.key.key_code(keybind_character))  # Set keybind code identifier number to the one given

                    # Break selection in check_events()
                    self.changing = False


    """ Handle user inputs """
                
    def check_events(self, event_list, all_keybind_keys):
        mouse_pos = pg.mouse.get_pos()
        new_x = self.x

        # If mouse is hovering the button 
        if self.top_rect.collidepoint(mouse_pos):
            # Set the colour to a hovering colour

            self.colour = self.hov_colour
            # If the mouse is pressed

            if pg.mouse.get_pressed()[0]:
                # Signal the initiation of a keybind change
                self.pressed = True
                self.changing = True

            else:
                #Resetting pressed variable after one click
                if self.pressed == True:
                    pass
                    #print("clicked")

            # Clear keybind and recieve user input
            if self.changing:
                self.set_keybind_key("_")
                self.check_for_change(event_list, all_keybind_keys)
        else:
            # If mouse isn't hovering button, reset colour to original colour
            self.colour = self.og_colour
            self.pressed = False

    """ Draw button with keybind in the centre """
    def draw_button(self, screen):
        pg.draw.rect(screen, self.colour, self.top_rect)
        font = pg.font.Font(self.font_name, 32)
        # Capatlise keybind
        keybind = font.render(self.keybind_key.upper(), 1, (255,255,255))
        # Centre text
        screen.blit(keybind, (self.x + (self.width/2 - keybind.get_width()/2), self.y + (self.height/2 - keybind.get_height()/2)))


class ItemButton(Button):
    def __init__ (self, colour, hov_colour, x, y, width, height, item):
        Button.__init__(self, colour, hov_colour, x, y, width, height, font=" ", text=" ")


        self.item = item
        # Position in inventory (row, column)
        self.pos = None

    # Set row and column in inventory
    def set_pos(self, pos):
        self.pos = pos


    def draw_button(self, screen):
        # Draw transparent button behind item
        pg.draw.rect(screen, (0,0,0,0), self.top_rect, 1)






        

		
        
                        
          

        

