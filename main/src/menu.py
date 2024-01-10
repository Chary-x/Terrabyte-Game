from button import *
from introduction import Introduction
import pygame as pg

# Menu classes

class Menu():
    def __init__(self, game):
        self.font_name = "Fonts/DigitalDisco.ttf"
        self.run_display = False
        self.offset_y = 100
        self.game = game

        self.back = Button(self.game.black, self.game.red, 10, 10, 80,80, self.font_name, "BACK")

        self.buttons = [self.back]

    def draw_all_buttons(self):
        for button in self.buttons:
            button.draw_button(self.game.screen)

    # Check if user quits
    def check_quit(self, event_type):
        if event_type == pg.QUIT:
            self.run_display = False
            pg.quit()

    # Respawn player
    def respawn_player(self):
        # Restore player 
        self.game.player.reset_health()
        # Set dead to Player.dead to false
        self.game.player.set_dead(False)
        # Set score to 0
        self.game.player.reset_score()
        # Spawn at origin
        self.game.player.spawn_at_origin()
        # Restore enemy health
        self.game.player.current_level.replenish_enemies()
            

    # If user clicks ' main menu ' display main menu
    def check_main_menu(self):
        if self.main_menu.is_left_clicked():
            self.respawn_player()
            self.run_display = False
            self.game.main_menu.display_menu()

    # Display menu
    def display_menu(self):  
        self.run_display = True
        while self.run_display:
            self.game.screen.fill(self.game.black)
            self.draw_all_text()
            self.draw_all_buttons()
            self.check_events()
            pg.display.update()
# MainMenu

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.offset_y = 100
        self.volume_count = 0

        # Buttons

        self.play = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y - self.offset_y, 500, 100, self.font_name, "PLAY")
        self.settings = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y, 500, 100, self.font_name, "SETTINGS")
        self.credits = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y + self.offset_y, 500, 100, self.font_name, "CREDITS")
        self.leaderboard = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y + self.offset_y*2, 500, 100, self.font_name, "LEADERBOARD")
        self.buttons = [self.play, self.settings, self.credits, self.leaderboard]

    # Draw all text to screen
    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.white, 80, self.game.mid_x, self.game.mid_y - 300)
        self.game.draw_text("MAIN MENU", self.game.green, 60, self.game.mid_x , self.game.mid_y - 200)


    # Check if settings button is pressed
    def check_settings(self):
        if self.settings.is_left_clicked():
            self.run_display = False
            self.game.settings_menu.display_menu()

    # Check if play button is pressed
    def check_play(self):
        if self.play.is_left_clicked():
            # Display player's map level
            self.game.levels[self.game.player.map_level].display_level()
            self.run_display = False

    # Check if credits button is pressed
    def check_credits(self):
        if self.credits.is_left_clicked():
            self.run_display = False
            self.game.screen.fill(self.game.black)
            self.game.credits_menu.display_menu()
    
    def check_events(self):
        for event in pg.event.get():
            self.check_quit(event.type)
            self.check_settings()
            self.check_leaderboard()
            self.check_credits()
            self.check_play()

    def check_leaderboard(self):
        if self.leaderboard.is_left_clicked():
            self.run_display = False
            self.game.leaderboard_menu.display_menu()

    # Let music initiate once while running        
    def play_music(self):
        if self.volume_count == 0:
            self.game.boombox.play_intro()
            self.volume_count =+ 1
            
    def display_menu(self):
        self.game.screen.fill(self.game.black)
        self.run_display = True
        self.play_music()
        self.game.database.insert_all_items()
        while self.run_display:
            self.draw_all_text()
            self.draw_all_buttons()
            self.check_events()
            pg.display.update()

class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.volume = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y - self.offset_y, 500, 100, self.font_name, "VOLUME")
        self.controls = Button(self.game.black, self.game.brown, self.game.mid_x - (self.game.mid_x/3.3), self.game.mid_y + self.offset_y, 500, 100, self.font_name, "CONTROLS")
        self.back = Button(self.game.black, self.game.red, 10, 10, 80,80, self.font_name, "BACK")      
        
        self.buttons = [self.volume, self.controls, self.back] 


    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.white, 80, self.game.mid_x, self.game.mid_y - 300)
        self.game.draw_text("SETTINGS", self.game.green, 60, self.game.mid_x , self.game.mid_y - 200)

    # If back button pressed, go back to main menu
    def check_back(self):
        if self.back.is_left_clicked():
             self.run_display = False
             self.game.main_menu.display_menu()

    def check_volume(self):
        if self.volume.is_left_clicked():
            self.run_display = False
            self.game.volume_menu.display_menu()

    def check_controls(self):
        if self.controls.is_left_clicked():
            self.run_dispLAY = False
            self.game.control_menu.display_menu()

    def check_events(self):
        for event in pg.event.get():
            self.check_quit(event.type)
            self.check_back()
            self.check_volume()
            self.check_controls()


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.back = Button(self.game.black, self.game.red, 10, 10, 80,80, self.font_name, "BACK")
        self.box_rect = pg.Rect(self.game.display_x/4, self.game.mid_y, self.game.mid_x, 150)
        self.slider = Slider(self.game.brown, self.game.green,self.game.display_x/4, self.game.mid_y, 100, 150, self.font_name, "| | ", self.box_rect)
        self.buttons = [self.back, self.slider]

    def update_position(self, new_x):
        self.slider.update_position(new_x)
        # Update volume based on slider position
        self.volume = self.slider.get_volume()

    def draw_volume(self):
        self.box_surf = pg.Surface((self.box_rect.width, self.box_rect.h))
        self.volume_rect = pg.Rect(0, 0, self.slider.top_rect.left - self.box_rect.left, self.box_rect.h)
        pg.draw.rect(self.box_surf, self.game.red, (self.volume_rect))
        self.game.screen.blit(self.box_surf, self.box_rect)

     # Recieve current red volume width from volume object       
    def update_volume(self):
        temp = (self.volume_rect.width / (self.box_rect.width - self.slider.top_rect.width))
        self.slider.set_volume(temp)
        self.game.boombox.set_volume(temp)

    # Draw all boxes to screen
    def draw_all_boxes(self):
        pg.draw.rect(self.game.screen, self.game.brown, self.box_rect, 4)  
        self.draw_volume()  

    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.white, 80, self.game.mid_x, self.game.mid_y - 300)
        self.game.draw_text("VOLUME", self.game.green, 60, self.game.mid_x , self.game.mid_y - 200)
        self.game.draw_text("MOVE THE SLIDER TO CHANGE THE VOLUME", self.game.white, 40, self.game.mid_x , self.game.mid_y - 100)
        self.game.draw_text("Volume : " + str(self.slider.get_percentage()) + " % ", self.game.white, 40, self.game.mid_x , self.game.mid_y + 250)

    # If back button pressed, go back to main menu
    def check_back(self):
        if self.back.is_left_clicked():
             self.run_display = False
             self.game.main_menu.display_menu()

    def check_events(self):
        event_list = pg.event.get()
        mouse_pos = pg.mouse.get_pos()
        self.check_back()
        for event in event_list:
            self.check_quit(event.type)
            self.slider.check_events(event_list)
            #Update volume based on slider position
            if event.type == pg.MOUSEBUTTONUP and self.slider.is_left_clicked():
                self.volume = self.slider.get_volume()

    def display_menu(self):
        self.game.screen.fill(self.game.black)
        self.run_display = True
        while self.run_display:
            self.game.screen.fill(self.game.black)
            self.draw_all_text()
            self.draw_all_boxes()
            self.draw_all_buttons()
            self.check_events()
            self.update_volume()
            pg.display.update()


class ControlMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        self.back = Button(self.game.black, self.game.red, 10, 10, 80,80, self.font_name, "BACK")

        self.changing = False
        self.changed = False
        self.invalid_keybind = False

        # Get list of keybind keys for player from database
        self.keybind_keys = self.game.database.load_keys()    
    
        # Create keybind objects for keybinds
        # Spaced 120 y pixels apart
        self.up_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y - 260, 120, 120 ,"UP", self.keybind_keys[0], self.game) 
        self.left_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y - 140, 120, 120 ,"LEFT", self.keybind_keys[1], self.game) 
        self.down_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y - 20, 120, 120,"DOWN", self.keybind_keys[2], self.game) 
        self.right_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y + 100, 120, 120,"RIGHT", self.keybind_keys[3], self.game)
        self.attack_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y + 220, 120, 120, "ATTACK", self.keybind_keys[4], self.game)
        self.inventory_keybind = Keybind(self.game.green, self.game.brown, self.game.mid_x + 100, self.game.mid_y + 340, 120, 120,"INVENTORY",self.keybind_keys[5], self.game) 

        # List of keybind objects
        self.keybinds = [self.up_keybind, self.left_keybind, self.down_keybind, self.right_keybind, self.attack_keybind, self.inventory_keybind]     
        
    # Draw keybind text

    def draw_keybind_text(self):
        # Space 120 y pixels apart
        self.game.draw_text("MOVE UP", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y - 190)
        self.game.draw_text("MOVE LEFT", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y - 70)
        self.game.draw_text("MOVE DOWN", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y + 50)
        self.game.draw_text("MOVE RIGHT", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y + 170)
        self.game.draw_text("ATTACK", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y + 290)
        self.game.draw_text("INVENTORY", self.game.white, 50, self.game.mid_x - 100, self.game.mid_y + 410)

    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.white, 80, self.game.mid_x, self.game.mid_y - 400)
        self.game.draw_text("CONTROLS", self.game.green, 60, self.game.mid_x , self.game.mid_y - 300)
        self.draw_keybind_text()
        
        if self.changing:
            self.game.draw_text("ENTER NEW KEYBIND", self.game.red, 40, self.game.mid_x , self.game.mid_y- 230)
        if self.invalid_keybind:
            self.game.draw_text("KEYBIND ALREADY TAKEN", self.game.red, 40, self.game.mid_x , self.game.mid_y- 230)

        
    # When back button is pressed, return to settings and load keybind changes to database
    def check_back(self):
        if self.back.is_left_clicked():
            # Update any keybind changes in database
            self.game.database.update_keys_table(self.get_update_data())
            # Switch menus
            self.game.settings_menu.display_menu()
            self.run_display = False

    """ Check each keybind event """
    def check_keybind_events(self, event_list, all_keybind_keys):
        for keybind in self.keybinds:
            keybind.check_events(event_list, all_keybind_keys)

    """ Check all events """
    def check_events(self):
        all_keybind_keys = self.get_all_keybind_keys()
        event_list = pg.event.get()
        self.check_back()
        self.check_keybind_events(event_list, all_keybind_keys)
        for event in event_list:
            self.check_quit(event.type)
    
    """ Get list of all keybind keys """
    def get_all_keybind_keys(self):
        keys = []
        last = len(self.keybinds) 
        for i in range (0, last):
            keys.append(self.keybinds[i].keybind_key)
        return keys

    """ Get current keybinds before exiting control menu """
    def get_update_data(self):
        keys = []
        for keybind in self.keybinds:
            keys.append(keybind.keybind_key)
        return keys
        
    """ Draw all keybinds to screen """
    def draw_all_keybinds(self):
        for keybind in self.keybinds:
            keybind.draw_button(self.game.screen)

    def draw_all_buttons(self):
        self.back.draw_button(self.game.screen)
        self.draw_all_keybinds()
        
    def display_menu(self):  
        self.run_display = True
        while self.run_display:
            self.game.screen.fill(self.game.black)
            self.draw_all_text()
            self.draw_all_buttons()
            self.check_events()
            pg.display.update()

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.back = Button(self.game.black, self.game.red, 10, 10, 80,80, self.font_name, "BACK") 

    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.white, 80, self.game.mid_x, self.game.mid_y - 300)
        self.game.draw_text("CREDITS", self.game.green, 60, self.game.mid_x , self.game.mid_y - 200)
        self.game.draw_text("TERRABYTE NEA by Chary aka Ignatius", self.game.gold, 50, self.game.mid_x, self.game.mid_y - 100)
        self.game.draw_text("Current music soundtrack : Intervals - Lock & Key", self.game.white, 30, self.game.mid_x, self.game.mid_y)
        self.game.draw_text("Menu Template by CDCodes on youtube", self.game.white, 30, self.game.mid_x, self.game.mid_y + 100)
        self.game.draw_text("Entity sprites : Penzilla.itch.io", self.game.white, 30, self.game.mid_x, self.game.mid_y + 200)
        self.game.draw_text("Initial button class : Tech With Tim on youtube", self.game.white, 30, self.game.mid_x, self.game.mid_y + 300)
        self.game.draw_text("Weapon assets : Flaticon.com and disven.itch.io", self.game.white, 30, self.game.mid_x, self.game.mid_y + 400 )
        
    def draw_all_buttons(self):
        self.back.draw_button(self.game.screen)


    def check_back(self):
        if self.back.is_left_clicked():
            self.run_display = False
            self.game.main_menu.display_menu()
            
    def check_events(self):
        event_list = pg.event.get()
        mouse_pos = pg.mouse.get_pos()
        for event in event_list:
            self.check_quit(event.type)
            self.check_back()

    def display_menu(self):
        self.game.screen.fill(self.game.black)
        self.run_display = True
        while self.run_display:
            self.check_events()   
            self.draw_all_buttons()
            self.draw_all_text()
            pg.display.update()
        
    
    
class AfterLifeMenu(Menu):
    def __init__ (self, game):
        """
        These params are set within levels file upon a death/ level completion. not passed as an arg
        score --> score of player at the time of level completion or death
        dead  --> boolean, true if player died, false if player simply completed the level
        """
        Menu.__init__(self, game)

        self.score = None
        self.dead = None

        # Initialise buttonss
        self.main_menu = Button(self.game.black, self.game.brown, self.game.mid_x - 700 , self.game.mid_y + self.offset_y, 400, 100, self.font_name, "MAIN MENU")
        self.play_again = Button(self.game.black, self.game.brown, self.game.mid_x -200, self.game.mid_y + self.offset_y, 400, 100, self.font_name, "PLAY AGAIN")
        self.leaderboard = Button(self.game.black, self.game.brown, self.game.mid_x + 300, self.game.mid_y + self.offset_y, 400, 100, self.font_name, "LEADERBOARD")
        self.buttons = [self.main_menu, self.play_again, self.leaderboard]

    def draw_all_text(self):
        # If player died
        if self.dead:
            self.game.draw_text("YOU DIED", self.game.red, 80, self.game.mid_x, self.game.mid_y - 300)
        else:
            self.game.draw_text("CONGRATULATIONS", self.game.green, 80, self.game.mid_x, self.game.mid_y - 300)
        self.game.draw_text(f"You managed to score {self.score} points!", self.game.white, 60, self.game.mid_x , self.game.mid_y - 200)

    # Draw all buttons to screen
    def draw_all_buttons(self):
        for button in self.buttons:
            button.draw_button(self.game.screen)

    # If user clicks ' Play again ', restart level
    def check_play_again(self):
        if self.play_again.is_left_clicked():

            # Replay level
            self.respawn_player()
            self.game.levels[self.game.player.map_level].display_level()
            # Stop displaying afterlife menu
            self.run_display = False

    # If user clicks 'Leaderboard', show leaderboard
    def check_leaderboard(self):
        if self.leaderboard.is_left_clicked():
            self.run_display = False
            self.game.leaderboard_menu.display_menu()

    # Check all user events
    def check_events(self):
        event_list = pg.event.get()
        for event in event_list:
            self.game.main_menu.check_quit(event.type)
            self.check_play_again()
            self.check_leaderboard()
            self.check_main_menu()

    # Display menu 
    def display_menu(self):
        self.game.screen.fill(self.game.black)
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.draw_all_buttons()
            self.draw_all_text()
            pg.display.update()


class LeaderboardMenu(Menu):
    def __init__ (self, game):

        Menu.__init__(self, game)

        self.offset = 350 

        #Initialise buttons
        self.terrarium = Button(self.game.black, self.game.brown, 50, 350, 400, 100, self.font_name, "TERRARIUM")
        self.level2 = Button(self.game.black, self.game.brown, self.game.display_x - 450, 350, 400, 100, self.font_name, "N/A")
        self.level3 = Button(self.game.black, self.game.brown, 50, 350 + self.offset, 400, 100, self.font_name, "N/A")
        self.level4 = Button(self.game.black, self.game.brown, self.game.display_x - 450, 350 + self.offset, 400, 100, self.font_name, "N/A")
        self.main_menu = Button(self.game.black, self.game.brown, self.game.mid_x - 200, self.game.mid_y + 350, 400, 100, self.font_name, "MAIN MENU")

        self.buttons = [self.terrarium, self.level2, self.level3, self.level4, self.main_menu]
        self.load_map_icons()

        # TODO - draw map icons on top of maps HERE

    def check_terrarium(self):
        if self.terrarium.is_left_clicked():
            self.run_display = False
            self.game.terrarium_leaderboard.display_menu()
 
    def check_level2(self):
        if self.level2.is_left_clicked():
            pass 
            # rundisplay = false
            # load level 2 sub-leaderboard

    def check_level3(self):
        if self.level3.is_left_clicked():
            pass 
            # run display = false 
            # load level 3 sub-leaderboard

    def load_map_icons(self):
        """
        Load all level map icons here
        """
        self.terrarium_icon = pg.image.load('Maps/Level Icons/Terrarium.png')
        # Scaling down icon to set px limit
        self.terrarium_icon = pg.transform.scale(self.terrarium_icon, (400, 300))
        # Insert future level icons

    def draw_all_icons(self):
        """ 
        Draw all icons above corrosponding buttons
        """
        # Formatting icon above button
        terrarium_icon_x = self.terrarium.top_rect.x + self.terrarium.top_rect.width/2 - self.terrarium_icon.get_width()/2
        terrarium_icon_y = self.terrarium.top_rect.y - self.terrarium_icon.get_height() - 10
        self.game.screen.blit(self.terrarium_icon, (terrarium_icon_x, terrarium_icon_y))

        # Do same for future icons here

    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.green, 80, self.game.mid_x, self.game.mid_y - 420)
        self.game.draw_text("LEADERBOARDS", self.game.white, 40, self.game.mid_x, self.game.mid_y - 360)

    # Check all user events
    def check_events(self):
        event_list = pg.event.get()
        for event in event_list:
            self.check_quit(event.type)
            self.check_terrarium()
            self.check_level2()
            self.check_level3()
            self.check_main_menu()

     # Display menu
    def display_menu(self):  
        self.run_display = True
        while self.run_display:
            self.game.screen.fill(self.game.black)
            self.draw_all_text()
            self.draw_all_buttons()
            self.draw_all_icons()
            self.check_events()
            pg.display.update()







