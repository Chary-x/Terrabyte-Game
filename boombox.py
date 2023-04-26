import pygame as pg


# Music file class to control all audio
class Boombox():
	def __init__(self, game):

		# Filpaths

		# The only current song
		# Lunatric - lock & key https://www.youtube.com/watch?v=uMYJjSWaTag
		self.locknkey = "lock&key.wav"


	def play_audio(self, filepath):
		pg.mixer.music.load(filepath)
		pg.mixer.music.play()
	

	def stop_audio(self):
		pg.mixer.music.stop()

	def play_intro(self):
		self.play_audio(self.locknkey)

	def set_volume(self, volume):
		pg.mixer.music.set_volume(volume)

	def get_volume(self):
		pg.mixer.music.get_volume()

