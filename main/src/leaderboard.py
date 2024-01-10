from menu import Menu
from button import Button
import pygame as pg

class Leaderboard(Menu):
    def __init__(self, game, level):
        Menu.__init__(self, game)

        self.level = level
        self.limit = 10

        self.play = Button(self.game.black, self.game.green, 585, 720, 500, 100, self.font_name, "PLAY")
        self.buttons = [self.back, self.play]

    def check_play(self):
        # If play button clicked
        if self.play.is_left_clicked():
            #player's current level = menu's level
            self.game.current_level = self.game.levels[self.level]
            # update 'map_level' field for player'
            """ REMOVED AS CURRENTLY ONLY 1 LEVEL 
            #self.game.database.update_player_table(self.game.current_level, 'map_level', self.game.player.player_id)]
            """
            # None case
            if self.game.player.current_level != None:
                # Display player's current level
                self.game.player.current_level.display_level()
                 # Stop displaying leaderboard
                self.run_display = False
            else:
                pass
   
        # List containing top_x players for this level
        self.top_x = {}

    def get_top_x(self):
        """ 
        Get a list of top x players for that level
        Parameters:
            level (int) --> current level
            limt  (int) --> number of players to display on leaderboard
        """
        # Recieving leaderboard list from database
        top_x_list = self.game.database.get_top_x(self.level, self.limit)
        # Converting the list into a dictionary
        top_x_dict = {display_name: score for display_name, score in top_x_list}
        self.top_x = top_x_dict

    def draw_player_text(self):
        self.get_top_x()
        for i, (display_name,score) in enumerate(self.top_x.items()):
            # Draw player's display_name and score at specific Y offset intervals
            # Starting from just below " TERRABYTE LEADERBOARD 
            offset_y = (self.game.mid_y -200) + (i *50)
            # Set player text depending on positon
            # Set colour dpednin
            if (i+1) == 1:
                colour = self.game.gold
            elif (i+1) == 2:
                colour = self.game.silver
            elif (i+1) == 3:
                colour = self.game.bronze
            else:
                # Not in top 3, no podium colour
                colour = self.game.white

            self.game.draw_text(f"{i+1}, {display_name} : {score}", colour, 30, self.game.mid_x, offset_y)

class TerrariumLeaderboard(Leaderboard):
    def __init__ (self, game):
        Leaderboard.__init__(self, game, 1)

    # get top 10 players for corropsonding level
    # Draw all text
    def draw_all_text(self):
        self.game.draw_text("TERRABYTE", self.game.green, 80, self.game.mid_x, self.game.mid_y - 420)
        self.game.draw_text("TERRARIUM LEADERBOARD" , self.game.white, 40, self.game.mid_x, self.game.mid_y - 360)
        self.draw_player_text()

    # Return to leaderboard menu if back is selected
    def check_back(self):
        if self.back.is_left_clicked():
            self.run_display = False
            self.game.leaderboard_menu.display_menu()

    def check_events(self): 
        event_list = pg.event.get()
        for event in event_list:
            self.check_quit(event.type)
            self.check_back()
            self.check_play()

