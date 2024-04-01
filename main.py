import math
import os
import random
import sys
import time

import pyglet
from pyglet.gl import *
#from pyglet import resource
from pyglet.window import key
from pyglet import font
from pyglet import media
from pyglet.font import ttf
from pyglet.sprite import Sprite

import text_input
import load_resources

#-----------------------------------------------------------
# VARIABLES
#-----------------------------------------------------------

#print(load_resources.x)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

MAX_DIFFICULTY = 2
MAX_CHARACTER = 14

in_game = False
in_main_menu = True

obstacleSpawnWidth = [50,350]
obstacles = []
clocks = [pyglet.clock.Clock()]
difficulty = 3 #changes depending on selection
keys = key.KeyStateHandler()

stats_multiplier = [1, 1.1, 1.2, 1.3, 1.5,
					1, 1.75, 2, 1.75, 2.3,
					2.5, 2.3, 2.7, 3]

animals_names = ['SISIW', 'DAGA', 'PALAKA', 'UNGGOY', 'BAKA',
				'PUSA', 'ASO', 'USO', 'LOBO', 'OSO',
				'KOALA', 'PANDA', 'TIGRE', 'LEON']
animals_price_list = [0, 100, 200, 300, 500, 700, 900, 1200, 1500, 1800, 2200, 2600, 3000, 4000]

animals = []

animals.append(load_resources.sisiw_01)
animals.append(load_resources.daga_02)
animals.append(load_resources.palaka_03)
animals.append(load_resources.unggoy_04)
animals.append(load_resources.baka_05)
animals.append(load_resources.pusa_06)
animals.append(load_resources.aso_07)
animals.append(load_resources.uso_08)
animals.append(load_resources.lobo_09)
animals.append(load_resources.oso_10)
animals.append(load_resources.koala_11)
animals.append(load_resources.panda_12)
animals.append(load_resources.tigre_13)
animals.append(load_resources.leon_14)

#-----------------------------------------------------------
# GAME OBJECTS
#-----------------------------------------------------------

# for center-anchoring of images
def center_anchor(img):
	img.anchor_x = img.width // 2
	img.anchor_y = img.height // 2


# for sprites
class GameObject():

	def __init__(self, posx, posy, sprite = None):
		self.posx = posx
		self.posy = posy
		self.velx = 0
		self.vely = 0
		if sprite is not None:
			self.sprite = sprite
			self.sprite.x = self.posx
			self.sprite.y = self.posy

	def draw(self):
		self.sprite.draw()

	def update(self, dt):
		self.posx += self.velx*dt
		self.posy += self.vely*dt
		self.sprite.x = self.posx
		self.sprite.y = self.posy

#-----------------------------------------------------------
# SCREEN OVERLAYS
#-----------------------------------------------------------

# game window + infinite scrolling bg
class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bg_img = load_resources.main_menu_bg
		self.bg_list = []
		
		for i in range(2):
			self.bg_list.append(GameObject(i*1200, 0, Sprite(self.bg_img)))

		for bg in load_resources.bg_list:
			bg.velx = -50

	def draw(self):
		self.clear()
		for bg in self.bg_list:
			bg.draw()


	def update_bg(self, dt):
		for bg in self.bg_list:
			bg.update(dt)
			if bg.posx <= -1300:
				self.bg_list.remove(bg)
				self.bg_list.append(GameObject(1100, 0, Sprite(self.bg_img)))
			bg.velx = -50


	def update(self, dt):
		global in_game

		self.update_bg(dt)

# Overlay - scene-changing class	
class Overlay(object):
	def update(self, dt):
		pass

	def draw(self):
		pass

# Menu
class Menu(Overlay):
	def __init__(self, x, y, title):
		self.x = x
		self.y = y
		self.items = []
		self.title_text = GameObject(x, y, Sprite(title))
		
	def reset(self):
		self.selected_index = 0
		self.items[self.selected_index].selected = True

	# put on_key_press and on_key_release under classes
	def on_key_press(self, symbol, modifiers):
		if symbol == key.DOWN:
			self.selected_index += 1
		elif symbol == key.UP:
			self.selected_index -= 1
		self.selected_index = min(max(self.selected_index, 0), len(self.items) - 1)

		if symbol in (key.DOWN, key.UP) and enable_sound:
			load_resources.button_sound.play()

	def on_key_release(self, symbol, modifiers):
		self.items[self.selected_index].on_key_release(symbol, modifiers)

	def draw(self):
		self.title_text.draw()
		for i, item in enumerate(self.items):
			item.draw(i == self.selected_index)

# Menu items (non-toggle)
class MenuItem(object):
	pointer_color = (1, 1, 1)
	inverted_pointers = False

	def __init__(self, img, y, activate_func):
		center_anchor(img)
		self.y = y
		self.x = WINDOW_WIDTH//2
		self.img = img
		self.text = GameObject(self.x, self.y, Sprite(img))
		self.activate_func = activate_func

	def draw_pointer(self, x, y, color, flip=False):
		# color the pointer image to a color

		glPushAttrib(GL_CURRENT_BIT)
		glColor3f(*color)

		if flip:
			load_resources.pointer_image_flip.blit(x, y)
		else:
			load_resources.pointer_image.blit(x, y)

		glPopAttrib()

	def draw(self, selected):
		self.text.draw()

		if selected:
			if self.img == load_resources.maglaro_btn:
				self.img = load_resources.maglaro_btn_pressed
			elif self.img == load_resources.paano_btn:
				self.img = load_resources.paano_btn_pressed
			elif self.img == load_resources.baguhin_btn:
				self.img = load_resources.baguhin_btn_pressed
			elif self.img == load_resources.leaderboard_btn:
				self.img = load_resources.leaderboard_btn_pressed
			elif self.img == load_resources.umalis_btn:
				self.img = load_resources.umalis_btn_pressed
			elif self.img == load_resources.OK_btn:
				self.img = load_resources.OK_btn_pressed
			elif self.img == load_resources.back_btn:
				self.img = load_resources.back_btn_pressed

			center_anchor(self.img)
			self.text = GameObject(self.x, self.y, Sprite(self.img))
			self.text.draw()

			if self.inverted_pointers == True:
				self.draw_pointer(
					self.text.posx - self.img.width//2 - 40, self.y, self.pointer_color, self.inverted_pointers)
				self.draw_pointer(
					self.text.posx + self.img.width//2 + 40, self.y, self.pointer_color, not self.inverted_pointers)
			
		else:
			if self.img == load_resources.maglaro_btn_pressed:
				self.img = load_resources.maglaro_btn
			elif self.img == load_resources.paano_btn_pressed:
				self.img = load_resources.paano_btn
			elif self.img == load_resources.baguhin_btn_pressed:
				self.img = load_resources.baguhin_btn
			elif self.img == load_resources.leaderboard_btn_pressed:
				self.img = load_resources.leaderboard_btn
			elif self.img == load_resources.umalis_btn_pressed:
				self.img = load_resources.umalis_btn
			elif self.img == load_resources.OK_btn_pressed:
				self.img = load_resources.OK_btn
			elif self.img == load_resources.back_btn_pressed:
				self.img = load_resources.back_btn

			center_anchor(self.img)
			self.text = GameObject(self.x, self.y, Sprite(self.img))
			self.text.draw()

	def on_key_release(self, symbol, modifiers):
		# to "press" on the object
		if symbol == key.ENTER and self.activate_func:
			self.activate_func()
			if enable_sound:
				load_resources.button_sound.play()

# "Baguhin ang Laro" menu item (toggling menu item)
class ChangeDifficultyLevel(MenuItem):
	pointer_color = (1, 1, 1)
	inverted_pointers = True

	def __init__(self, y):
		super(ChangeDifficultyLevel, self).__init__(self.get_img(), y, None)

	def get_img(self):
		if difficulty == 0:
			return load_resources.lebel_1
		elif difficulty == 1:
			return load_resources.lebel_2
		elif difficulty == 2:
			return load_resources.lebel_3

	def on_key_release(self, symbol, modifiers):
		global difficulty
		if symbol == key.LEFT:
			difficulty -= 1
		elif symbol == key.RIGHT:
			difficulty += 1
		difficulty = min(max(difficulty, 0), MAX_DIFFICULTY)
		self.img = self.get_img()

		if symbol in (key.LEFT, key.RIGHT) and enable_sound:
			load_resources.button_sound.play()

# "Baguhin ang Laro" menu item (toggling menu item)
class ChangeSound(MenuItem):
	pointer_color = (1, 1, 1)
	inverted_pointers = True

	def __init__(self, y):
		#calls parent class
		super(ChangeSound, self).__init__(self.get_img(), y, None)

	def get_img(self):
		if enable_sound == True:
			return (load_resources.sound_on)
			
		elif enable_sound == False:
			return (load_resources.sound_off)
			

	def on_key_release(self, symbol, modifiers):
		global enable_sound
		if symbol == key.LEFT:
			enable_sound = True
			music.play()
		elif symbol == key.RIGHT:
			enable_sound = False
			music.pause()
		#difficulty = min(max(difficulty, 0), 1)
		self.img = self.get_img()

		if symbol in (key.LEFT, key.RIGHT) and enable_sound:
			load_resources.button_sound.play() 

# "Baguhin ang Laro" menu item (toggling menu Item)
class ChangeFPS(MenuItem):
	pointer_color = (1, 1, 1)
	inverted_pointers = True

	def __init__(self, y):
		#calls parent class
		super(ChangeFPS, self).__init__(self.get_img(), y, None)

	def get_img(self):
		if show_fps == True:
			return (load_resources.fps_on)
		elif show_fps == False:
			return (load_resources.fps_off)

	def on_key_release(self, symbol, modifiers):
		global show_fps
		if symbol == key.LEFT or symbol == key.RIGHT:
			show_fps = not show_fps
			#show_fps = min(max(1, 0), 1)
			self.img = self.get_img()
			#self.toggle_func(show_fps)

		if symbol in (key.LEFT, key.RIGHT) and enable_sound:
			load_resources.button_sound.play()	

# "Main Menu" scene
class MainMenu(Menu):
	def __init__(self):
		# calling parent class "Menu"
		global in_game
		in_game = False
		super(MainMenu, self).__init__(0, 420, load_resources.pybilisan)

		# def __init__(self, label, y, activate_func)
		self.items.append(MenuItem(load_resources.maglaro_btn, 380, main_characters))
		self.items.append(MenuItem(load_resources.paano_btn, 320, main_paano_maglaro))
		self.items.append(MenuItem(load_resources.baguhin_btn, 260, main_baguhin_ang_laro))
		self.items.append(MenuItem(load_resources.leaderboard_btn, 200, main_leaderboard))
		self.items.append(MenuItem(load_resources.umalis_btn, 140, sys.exit))
		self.reset()

# "Paano Maglaro" scene
class Paano_Maglaro(Menu):
	def __init__(self):
		global in_game
		in_game = False

		super(Paano_Maglaro, self).__init__(0, 530, load_resources.paano_title)

		self.instructions = GameObject(WINDOW_WIDTH/8, 120, Sprite(load_resources.directions))
		self.items.append(MenuItem(load_resources.OK_btn, 80, main_menu))
		self.reset()

		
	def draw(self):
		super(Paano_Maglaro, self).draw()
		self.instructions.draw()

# "Baguhin ang Laro" scene
class Baguhin_Ang_Laro(Menu):
	def __init__(self):
		global in_game
		in_game = False

		super(Baguhin_Ang_Laro, self).__init__(0, 530, load_resources.baguhin_title)

		self.items.append(ChangeDifficultyLevel(380))
		self.items.append(ChangeSound(320))
		self.items.append(ChangeFPS(260))
		self.items.append(MenuItem(load_resources.OK_btn, 200, main_menu))

		self.reset()

# "Ranggo ng Iskor" scene
class Ranggo_Ng_Iskor(Menu):
	def __init__(self):
		super(Ranggo_Ng_Iskor, self).__init__(0, 530, load_resources.leaderboard_title)

		self.items.append(MenuItem(load_resources.OK_btn, 140, main_menu))

		center_anchor(load_resources.box)
		center_anchor(load_resources.box_small)

		self.box = GameObject(WINDOW_WIDTH/2, 300, Sprite(load_resources.box))
		self.box_small = GameObject(WINDOW_WIDTH/2, 300, Sprite(load_resources.box_small))

		self.reset()

	def draw(self):
		global leaderboard_names
		global leaderboard_scores

		super(Ranggo_Ng_Iskor, self).draw()

		leaderboard_pairs = []
		max_leaderboard = 5

		if len(leaderboard_names) > 0 and len(leaderboard_scores) > 0:
			for i in range(len(leaderboard_names)):
				leaderboard_pairs.append([leaderboard_names[i], leaderboard_scores[i]])

			by_score = lambda x: (int(x[1]), x[0])
			leaderboard_pairs.sort(key=by_score, reverse=True)

			self.name_title = pyglet.text.Label("PANGALAN", font_name='Point Soft DEMO Semi Bold', font_size=20, x=50, y = 465, anchor_x='left', anchor_y='center', bold=True, color = (104, 104, 104, 255))
			self.score_title = pyglet.text.Label("ISKOR", font_name='Point Soft DEMO Semi Bold', font_size=20, x=350, y = 465, anchor_x='right', anchor_y='center', bold=True, color = (104, 104, 104, 255))

			self.box.draw()
			self.name_title.draw()
			self.score_title.draw()

			self.label_y = 405

			for pair in leaderboard_pairs:
				self.name_label = pyglet.text.Label(pair[0], font_name='Point Soft DEMO Semi Bold', font_size=20, x=50, y = self.label_y, anchor_x='left', anchor_y='center', bold=True)
				pair1 = str(pair[1])
				pair1.replace(' ', '')
				self.score_label = pyglet.text.Label(pair1, font_name='Point Soft DEMO Semi Bold', font_size=20, x=350, y = self.label_y, anchor_x='right', anchor_y='center', bold=True)
				self.name_label.draw()
				self.score_label.draw()
				self.label_y -= 40
		else:
			self.no_scores = pyglet.text.Label("Maglaro ka muna!", font_name='Point Soft DEMO Semi Bold', font_size=20, x=WINDOW_WIDTH/2, y = 300, anchor_x='center', anchor_y='center', bold=True)

			self.box_small.draw()
			self.no_scores.draw()

		
# Coins balance display
class Coins(object):
	def __init__(self):
		global coins
		money = open('money.txt', 'r')
		coins = money.read()
		if coins == '':
			coins = 100
		coins = int(coins)
		money.close()

	def draw(self):
		global coins
		coins_text = pyglet.text.Label(str(coins), font_name='Point Soft DEMO Semi Bold', font_size=25, x=380, y = 36, anchor_x='right', anchor_y='center', bold=True)

		center_anchor(load_resources.coins_icon)
		coins_sprite = GameObject(coins_text.x - coins_text.content_width - 35, coins_text.y - 2, Sprite(load_resources.coins_icon))

		coins_sprite.draw()
		coins_text.draw()

		if in_game == True and show_countdown == False:
			coins_text.draw()

# "Pumili ng Hayop" scene
class CharacterSelect(Menu):
	def __init__(self):
		global in_game
		in_game = False

		super(CharacterSelect, self).__init__(0, 530, load_resources.character_select_title)

		self.items.append(ChangeCharacters(320))
		self.items.append(MenuItem(load_resources.back_btn, 140, main_menu))
		center_anchor(load_resources.blank_light_grey_btn)
		center_anchor(load_resources.blank_grey_btn)
		center_anchor(load_resources.blank_yellow_btn)
		center_anchor(load_resources.blank_red_btn)
		center_anchor(load_resources.blank_light_btn)
		center_anchor(load_resources.blank_btn)
		center_anchor(load_resources.stats)
		
		self.blank_light_grey_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_light_grey_btn))
		self.blank_grey_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_grey_btn))
		self.blank_yellow_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_yellow_btn))
		self.blank_red_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_red_btn))
		self.blank_light_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_light_btn))
		self.blank_btn = GameObject(WINDOW_WIDTH/2, 200, Sprite(load_resources.blank_btn))
		self.stats = GameObject(WINDOW_WIDTH/2, 440, Sprite(load_resources.stats))

		self.reset()

	def draw(self):
		global character
		global characters_list
		global animals_price_list
		global animals_names
		global stats_multiplier

		char_read_file = open('characters.txt','r')
		char_read = char_read_file.readlines()
		char_list = []

		for char in char_read:
			char_list.append(char.replace('\n', ''))

		char_read_file.close()

		super(CharacterSelect, self).draw()

		if self.selected_index == 0:
			self.stats.draw()
			self.ako_si = pyglet.text.Label("Ako si...", font_name='Point Soft DEMO Semi Bold', font_size=15, x=125, y = 470, anchor_x='center', anchor_y='center', bold=True, color = (104, 104, 104, 255))
			self.character_name = pyglet.text.Label(animals_names[character-1] + "!", font_name='Point Soft DEMO Semi Bold', font_size=20, x=125, y = 445, anchor_x='center', anchor_y='center', bold=True, color = (104, 104, 104, 255))
			self.stats_details_multiplier = pyglet.text.Label(str(float(stats_multiplier[character-1])) + "x iskor multiplier", font_name='Point Soft DEMO Semi Bold', font_size=9.5, x=345, y = 460, anchor_x='right', anchor_y='center', bold=True)
			self.ako_si.draw()
			self.character_name.draw()
			self.stats_details_multiplier.draw()

		if animals_names[character-1] in char_list:
			if self.selected_index == 0:
				self.blank_red_btn.draw()
			else:
				self.blank_yellow_btn.draw()
			self.label = pyglet.text.Label("maglaro gamit nito", font_name='Point Soft DEMO Semi Bold', font_size=14.5, x=WINDOW_WIDTH/2, y = 202, anchor_x='center', anchor_y='center', bold=True)
			self.label.draw()
		else:
			if animals_price_list[character-1] <= coins:
				if self.selected_index == 0:
					self.blank_btn.draw()
				else:
					self.blank_light_btn.draw()
			else:
				if self.selected_index == 0:
					self.blank_grey_btn.draw()
				else:
					self.blank_light_grey_btn.draw()

			self.label = pyglet.text.Label("bilhin: " + str(animals_price_list[character-1]) , font_name='Point Soft DEMO Semi Bold', font_size=14.5, x=WINDOW_WIDTH/2, y = 202, anchor_x='center', anchor_y='center', bold=True)
			self.label.draw()


# "Pumili ng Hayop" menu item (toggling menu Item)
class ChangeCharacters(MenuItem):
	pointer_color = (1, 1, 1)
	inverted_pointers = True

	def __init__(self, y):
		super(ChangeCharacters, self).__init__(self.get_img(), y, None)

	def get_img(self):
		global character
		global animals
		global characters_list

		return animals[character-1]

	def on_key_release(self, symbol, modifiers):
		global character
		global characters_list
		global char_list
		global animals_price_list
		global in_game
		global coins
		global character_used
		global animal_player
		global animals
		global player
		
		money = open('money.txt', 'w')
		char_write = open('characters.txt','a+')
		char_read_file = open('characters.txt','r')
		char_read = char_read_file.readlines()
		char_list = []

		for char in char_read:
			char_list.append(char.replace('\n', ''))

		print(char_list)
		if symbol == key.LEFT:
			character -= 1
		elif symbol == key.RIGHT:
			character += 1
		elif symbol == key.ENTER:
			if animals_names[character-1] in char_list: 
				character_used = character
				print('animal' + animals_names[character_used-1])
				animal_player = animals[character_used-1]
				main_pangalan()
				in_game = False
			else:
				if animals_price_list[character-1] <= coins:
					characters_list.append(character)
					char_write.write('\n' + animals_names[character-1])
					coins = coins - animals_price_list[character-1]
					if enable_sound:
						load_resources.buy_sound.play()
				else:
					if enable_sound:
						load_resources.disabled_sound.play()

		character = min(max(character, 1), 14)
		self.img = self.get_img()

		if symbol in (key.LEFT, key.RIGHT) and enable_sound:
			load_resources.button_sound.play()

		char_read_file.close()
		money.write(str(coins))
		money.close()

# Text Widget class from Pyglet.Master
class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), dict(color=(0, 0, 0, 55)))
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

# "Ano ang Pangalan Mo?" Scene
class Pangalan(Menu):
	def __init__(self):
		super(Pangalan, self).__init__(0, 530, load_resources.maglaro_title)
		
		center_anchor(load_resources.box_small)
		self.batch = pyglet.graphics.Batch()
		self.box_small = GameObject(WINDOW_WIDTH/2, 300, Sprite(load_resources.box_small))
		self.labels = [pyglet.text.Label('Ano ang pangalan mo?', font_name='Point Soft DEMO Semi Bold', font_size=14.5, x=WINDOW_WIDTH/2, y = 320, anchor_x='center', anchor_y='center', bold=True, batch=self.batch), pyglet.text.Label('anim na karakter lamang', font_name='Point Soft DEMO Semi Bold', font_size=8, x=WINDOW_WIDTH/2, y = 302, anchor_x='center', anchor_y='center', bold=True, batch=self.batch)]
		self.widgets = [TextWidget('Kalaro', 150, 275, 100, self.batch)]
		self.focus = None
		self.set_focus(self.widgets[0])

		self.items.append(MenuItem(load_resources.OK_btn, 200, main_maglaro))

		self.reset()

	def draw(self):
		super(Pangalan, self).draw()
		self.box_small.draw()
		self.batch.draw()

	def on_text(self, text):
		if self.focus:
			self.focus.caret.on_text(text)

	def on_text_motion(self, motion):
		if self.focus:
			self.focus.caret.on_text_motion(motion)

	def on_text_motion_select(self, motion):
		if self.focus:
			self.focus.caret.on_text_motion_select(motion)

	def set_focus(self, focus):
		if focus == self.focus:
			return

		if self.focus:
			self.focus.caret.visible = False
			self.focus.caret.mark = self.focus.caret.position = 0

		self.focus = focus
		if self.focus:
			self.focus.caret.visible = True
			self.focus.caret.mark = 0
			self.focus.caret.position = len(self.focus.document.text)

	def on_key_release(self, symbol, modifiers):
		global character_name

		self.widgets[0].document.text.upper()

		if symbol == key.ENTER:
			if self.widgets[0].document.text.isspace() == False:
				if len(self.widgets[0].document.text) <= 6:
					character_name = self.widgets[0].document.text
					character_name = character_name[:-1]
					main_maglaro()
				else:
					self.widgets[0].document.text = 'MAG-TYPE ULIT'
			else:
				character_name = 'Kalaro'
				main_maglaro()

		print(character_name)

# "Maglaro" scene
class Maglaro(Overlay):
	def __init__(self):
		self.bg_img = load_resources.game_bg
		self.bg_list = []
		global in_game
		in_game = True

		global show_countdown

		show_countdown = True
		
		if in_game == True:
			for i in range(3):
				self.bg_list.append(GameObject(0, i*600, Sprite(self.bg_img)))

			for bg in load_resources.bg_list:
				bg.vely = -50

	def draw(self):
		global character_name
		global show_countdown
		global score
		if in_game == True:
			for bg in self.bg_list:
				bg.draw()

		if show_countdown == True:
			self.countdown = pyglet.text.Label("Maghanda, " + character_name + '!', font_name='Point Soft DEMO Semi Bold', font_size=25, x=WINDOW_WIDTH/2, y = WINDOW_HEIGHT/2, anchor_x='center', anchor_y='center', bold=True)
			self.press_enter = pyglet.text.Label("I-press ang enter para maglaro.", font_name='Point Soft DEMO Semi Bold', font_size=14.5, x=WINDOW_WIDTH/2, y = WINDOW_HEIGHT/2 - 30, anchor_x='center', anchor_y='center', bold=True)
			self.countdown.draw()
			self.press_enter.draw()
		else:
			self.countdown.delete()
			self.press_enter.delete()

	def update_bg(self, dt):
		if in_game == True and show_countdown == False:
			for bg in self.bg_list:
				bg.update(dt)
				if bg.posy <= -600:
					self.bg_list.remove(bg)
					self.bg_list.append(GameObject(0, 580, Sprite(self.bg_img)))
				bg.vely = -50

	def update(self, dt):
		global score
		global stats_multiplier
		global character_used
		global character_name
		global in_game

		if character_used_lives == 0:
			print("why")
			print(character_name)
			print(character_used_lives)
			in_game = False
			game_end()
			
		self.update_bg(dt)


	def on_key_release(self, symbol, modifiers):
		global show_countdown
		global character_used
		global character_used_lives
		global in_game

		if symbol == key.ENTER:
			show_countdown = False
			in_game = True

			game_start()
	
# Player class
class Player():
    def __init__(self):
    	global animal_player
    	global character_used
    	global score
    	global animals

    	animal_player = animals[character_used-1]
    	self.sprite = pyglet.sprite.Sprite(animal_player)
    	self.sprite.scale = .4
    	self.sprite.x = 200 - self.sprite.width/2
    	self.sprite.y = 100
    	self.score = 0
    	self.posx = self.sprite.x
    	self.posy = self.sprite.y
    	self.velx = 2# can be changed
    	self.vely = 0

# Obstacles class
class Obstacle():
	def __init__(self, vely, spawnLimits = None):
		global obstacleSpawnWidth
		self.velx = 0
		self.vely = vely
		self.sprite = pyglet.sprite.Sprite(load_resources.obstacle_game)
		self.sprite.scale = 0.2

		if spawnLimits is not None:
			possibleSpawns = []
			spawnLimits.sort()
			for i in range(len(spawnLimits)):
				if i == 0:
					if spawnLimits[0][0] - obstacleSpawnWidth[0] > self.sprite.width:
						possibleSpawns.append([obstacleSpawnWidth[0],spawnLimits[0][0]])
				if i == len(spawnLimits) - 1:
					if obstacleSpawnWidth[1] - spawnLimits[i][1] > self.sprite.width:
						possibleSpawns.append([spawnLimits[i][1], obstacleSpawnWidth[1]])
					else:
						continue
				else:
					if spawnLimits[i+1][0] - spawnLimits[i][1] > self.sprite.width:
						possibleSpawns.append([spawnLimits[i][1], spawnLimits[i+1][0]])

			random.shuffle(possibleSpawns)
			self.sprite.x = random.uniform(possibleSpawns[0][0], possibleSpawns[0][1] - self.sprite.width)

		else:
			self.sprite.x = random.uniform(obstacleSpawnWidth[0], obstacleSpawnWidth[1] - self.sprite.width)

		self.sprite.y = 600-self.sprite.height
		self.posx = self.sprite.x
		self.posy = self.sprite.y
		self.draw()

	def draw(self):
		self.sprite.draw()

	def update(self, dt):
		self.posy += self.vely*dt
		self.vely -= 4*dt
		self.sprite.y = self.posy

	def collide(dt):
		global character_used_lives
		global in_game
		global show_countdown
		print(character_used_lives)
		print('coli')
		if in_game == True and show_countdown == False:
			game_end()

class Coin():
	def __init__(self, vely):
		#global load_resources.coin_game
		self.velx = 0
		self.vely = vely
		self.sprite = pyglet.sprite.Sprite(load_resources.coin_game)
		self.sprite.scale = 0.2
		self.sprite.x = random.uniform(obstacleSpawnWidth[0], obstacleSpawnWidth[1] - self.sprite.width)
		self.sprite.y = 600-self.sprite.height
		self.posx = self.sprite.x
		self.posy = self.sprite.y
		self.draw()

	def draw(self):
		self.sprite.draw()

	def update(self, dt):
		self.posy += self.vely*dt
		self.vely -= 4*dt
		self.sprite.y = self.posy

	def collide(dt):
		global coins
		global in_game
		if in_game == True:
			coins += 1

class Game_Over(Menu):
	def __init__(self):
		super(Game_Over, self).__init__(0, 530, load_resources.game_over_title)

		self.items.append(MenuItem(load_resources.back_btn, 150, main_menu))
		self.reset()

	def draw(self):
		global score
		global character_name
		global in_main_menu
		global coins

		super(Game_Over, self).draw()

		print(character_name, player.score)

		if in_main_menu == False:
			score_label = pyglet.text.Label('ang iskor ni', font_name='Point Soft DEMO Semi Bold', font_size=25, x=WINDOW_WIDTH/2, y = 450, anchor_x='center', anchor_y='top', bold=True)
			name_label = pyglet.text.Label(character_name, font_name='Point Soft DEMO Semi Bold', font_size=25, x=WINDOW_WIDTH/2, y = 410, anchor_x='center', anchor_y='top', bold=True)
			score_display = pyglet.text.Label(str(round(float(player.score))), font_name='Point Soft DEMO Semi Bold', font_size=60, x=WINDOW_WIDTH/2, y = 350, anchor_x='center', anchor_y='top', bold=True)
			bonus_coins_display = pyglet.text.Label('+ ' + str(round(float(player.score))//10) + ' coins', font_name='Point Soft DEMO Semi Bold', font_size=25, x=WINDOW_WIDTH/2, y=250, anchor_x='center', anchor_y='top', bold=True)

			score_label.draw()
			name_label.draw()
			score_display.draw()
			bonus_coins_display.draw()
		
	
#-----------------------------------------------------------
# GAME STATE FUNCTIONS
#-----------------------------------------------------------

# Scene changes
def set_overlay(new_overlay):
	global overlay
	if overlay:
		win.remove_handlers(overlay)
	overlay = new_overlay
	print(overlay)
	if overlay:
		win.push_handlers(overlay)

def main_menu():
	global in_main_menu
	global music
	set_overlay(MainMenu())
	in_main_menu = True

	if enable_sound:
		music.play()
	else:
		music.pause()

	global score
	global character_name
	global character_used
	global character_used_lives
	global in_game

	if in_main_menu == True:
		score = 0
		character_name = 'Kalaro'
		character_used = 1
		character_used_lives = 1

		in_game = False

def main_characters():
	set_overlay(CharacterSelect())

def main_pangalan():
	set_overlay(Pangalan())

def main_maglaro():
	set_overlay(Maglaro())

def main_paano_maglaro():
	set_overlay(Paano_Maglaro())

def main_baguhin_ang_laro():
	set_overlay(Baguhin_Ang_Laro())

def main_leaderboard():
	set_overlay(Ranggo_Ng_Iskor())

def game_start():
	global player
	global music

	player = Player()

	#plays background music when not in game and paused when playing
	if enable_sound:
		music.next_source()
		music.queue(load_resources.bg_sound)
	else:
		music.pause()

	pyglet.clock.schedule_interval(checkCollisions, 1/60)
	pyglet.clock.schedule_interval(generateObstacle, 4)
	pyglet.clock.schedule_interval(newSched, 5)

	print("GAME START!!!")

def game_end():
	global in_main_menu
	global in_game
	global obstacles
	global score
	global character_name
	global leaderboard_names
	global leaderboard_scores
	global coins

	#enables a different music to be played in the background during gameplay. It changes when gameplay is done.
	if enable_sound:
		music.next_source()
		music.queue(load_resources.game_sound)
	else:
		music.pause()

	in_main_menu = False

	coins += round(float(player.score))//10

	money = open('money.txt', 'w')
	money.write(str(coins))
	money.close()

	set_overlay(Game_Over())
	pyglet.clock.unschedule(generateObstacle)
	pyglet.clock.unschedule(checkCollisions)
	pyglet.clock.unschedule(newSched)
	obstacles = []
	obstacles.append([True, Coin(-40)])

	leaderboard_names_read_file = open('leaderboard_names.txt', 'r')
	leaderboard_names_read = leaderboard_names_read_file.readlines()
	leaderboard_names = []

	leaderboard_scores_read_file = open('leaderboard_scores.txt', 'r')
	leaderboard_scores_read = leaderboard_scores_read_file.readlines()
	leaderboard_scores = []

	for name in leaderboard_names_read:
		leaderboard_names.append(name.replace('\n', ''))

	for score in leaderboard_scores_read:
		leaderboard_scores.append(int(score.replace('\n', '')))

	print(leaderboard_names)
	print(leaderboard_scores)

	if len(leaderboard_names) < 5:
		leaderboard_names.append(character_name)
	elif len(leaderboard_names) == 5:
		print('min leaderboard: ' + str(float(min(leaderboard_scores))))
		if float(player.score) > float(min(leaderboard_scores)):
			leaderboard_names.remove(leaderboard_names[leaderboard_scores.index(min(leaderboard_scores))])
			leaderboard_names.append(character_name)

	leaderboard_names_read_file.close()

	print('player score:', player.score)
	
	if len(leaderboard_scores) < 5:
		leaderboard_scores.append(round(player.score))
	elif len(leaderboard_scores) == 5 and float(player.score) > float(min(leaderboard_scores)):
		leaderboard_scores.remove(min(leaderboard_scores))
		leaderboard_scores.append(round(player.score))

	leaderboard_scores_read_file.close()

	leaderboard_names_write_file = open('leaderboard_names.txt', 'w')
	leaderboard_names_write_file.write('')
	leaderboard_names_write_file.close()

	leaderboard_scores_write_file = open('leaderboard_scores.txt', 'w')
	leaderboard_scores_write_file.write('')
	leaderboard_scores_write_file.close()

	leaderboard_names_write_file = open('leaderboard_names.txt', 'a+')

	for name in leaderboard_names:
		leaderboard_names_write_file.write(name + '\n')

	leaderboard_names_write_file.close()

	leaderboard_scores_write_file = open('leaderboard_scores.txt', 'a+')

	score_str = str(round(float(player.score)))

	for score in leaderboard_scores:
		leaderboard_scores_write_file.write(str(round((float(score)))) + '\n')

	leaderboard_scores_write_file.close()

	in_game = False
	


#-----------------------------------------------------------
# GLOBAL GAME STATE VARIABLES
#-----------------------------------------------------------

#load background music when app is opened
music = pyglet.media.Player()

music.queue(load_resources.bg_sound)
music.queue(load_resources.game_sound)

#current scene
overlay = None

#difficult of game
difficulty = 0

#default name of a character
character_name = 'Kalaro'

#for character-toggling in CharacterSelect menu
character = 1

#the character being played
character_used = 1

#the number of lives the character being used has
#character_used_lives = stats_lives[character_used-1]

#the characters owned by the user
characters_list = [1]

#the animal representation of the character being played
animal_player = animals[character_used-1]

# toggle sound on/off
enable_sound = True

# toggle FPS on/off
show_fps = False

# "Maglaro" boolean value for countdown
show_countdown = False


# player variable for Player()
player = None

score = 0

#coins balance
coins = 0

#coins display
coins_display = Coins()

leaderboard_names_read_file = open('leaderboard_names.txt', 'r')
leaderboard_names_read = leaderboard_names_read_file.readlines()
leaderboard_names = []

# accessing leaderboard text files
for name in leaderboard_names_read:
	leaderboard_names.append(name.replace('\n', ''))

leaderboard_names_read_file.close()

leaderboard_scores_read_file = open('leaderboard_scores.txt', 'r')
leaderboard_scores_read = leaderboard_scores_read_file.readlines()
leaderboard_scores = []

for score in leaderboard_scores_read:
	leaderboard_scores.append(score.replace('\n', ''))

leaderboard_scores_read_file.close()

#-----------------------------------------------------------
# CREATE WINDOW
#-----------------------------------------------------------

win = GameWindow(WINDOW_WIDTH, WINDOW_HEIGHT, 'Pybilisan', resizable = False)
win.push_handlers(keys)

fps_display = pyglet.window.FPSDisplay(win)

obstacles.append([True, Coin(-40)])

@win.event()
def on_draw():
	win.clear()
	global show_countdown
	global score
	global obstacles

	win.draw()

	glColor3f(1, 1, 1)

	# top, left, center, right, bottom
	for (x, y) in ((0, WINDOW_HEIGHT), (-WINDOW_WIDTH, 0), (0, 0), (WINDOW_WIDTH, 0), (0, -WINDOW_HEIGHT)):
		glLoadIdentity()
		glTranslatef(x, y, 0)
		load_resources.wrapping_batch.draw()

	glLoadIdentity()	
	load_resources.batch.draw()

	if overlay:
		overlay.draw()

	if show_fps:
		fps_display.draw()

	if in_game == True and show_countdown == False and player != None and len(obstacles) != None:
		for rowNo in range(len(obstacles)):
			if (obstacles[rowNo][0] == True):
				for o in range(1, len(obstacles[rowNo])):
					obstacles[rowNo][o].draw()

		player.sprite.draw()
		score_display = pyglet.text.Label(str(round(float(player.score))), font_name='Point Soft DEMO Semi Bold', font_size=40, x=WINDOW_WIDTH/2, y = 530, anchor_x='center', anchor_y='center', bold=True)
		score_display.draw()
		
	if in_game == True and player != None:
			player.score += .1*stats_multiplier[character_used-1]

	coins_display.draw()


# Obstacles generator
@win.event()
def generateObstacle(dt):
	global difficulty
	obstacles.append([True])
	spCoin = random.randint(0, 10)
	if spCoin%4 == 0:
		obstacles[len(obstacles)-1].append(Coin(obstacles[len(obstacles)-2][1].vely))
	else:
		obstacles[len(obstacles)-1].append(Obstacle(obstacles[len(obstacles)-2][1].vely))

	r = random.randint(1, 6)
	if difficulty == 0:
		if r == 0:
			numOfObs = 3
		elif r < 3:
			numOfObs = 2
		else:
			numOfObs = 1
	elif difficulty == 1:
		numOfObs = r%3 + 1
	else:
		if r == 1 or r == 3:
			numOfObs = r
		else:
			numOfObs = 3

	while len(obstacles[len(obstacles)-1]) < 1 + numOfObs:
		obstacles[len(obstacles)-1].append(Obstacle(obstacles[len(obstacles)-2][1].vely,[[i.posx,i.posx+i.sprite.width] for i in obstacles[len(obstacles)-1][1:]]))

	if obstacles[0][1].posy < -obstacles[0][1].sprite.height and len(obstacles) > 1:
		obstacles.pop(0)

#-----------------------------------------------------------
# GAME UPDATE
#-----------------------------------------------------------

def update(dt):
	win.update(dt)

	global show_countdown

	if overlay:
		overlay.update(dt)

	if in_game == True and show_countdown == False and player != None:
		for row in obstacles:
			if(row[0] == True):
				for o in range(1,len(row)):
					row[o].update(dt)

		if keys[key.LEFT]:
			if player.posx > obstacleSpawnWidth[0] + player.sprite.width/2:
				player.posx -= player.velx
				player.sprite.x = player.posx

		if keys[key.RIGHT]:
			if player.posx < obstacleSpawnWidth[1] - player.sprite.width/2:
				player.posx += player.velx
				player.sprite.x = player.posx

def checkCollisions(dt):
	if player != None:
		for row in obstacles:
			if (row[1].posy > 100 and row[1].posy - 100 < player.sprite.height) or (row[1].posy < 100 and 100 - row[1].posy < row[1].sprite.height):
				for i in row[1:]:
					if (i.posx > player.posx and i.posx - player.posx < player.sprite.width) or (player.posx > i.posx and player.posx - i.posx < i.sprite.width):
						i.collide() #triggers object thins

def newSched(dt):
	pyglet.clock.unschedule(generateObstacle)
	pyglet.clock.schedule_interval(generateObstacle, 200/abs(obstacles[0][1].vely))

#-----------------------------------------------------------
# START GAME
#-----------------------------------------------------------

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pyglet.clock.schedule_interval(update, 1/60)

main_menu()

win.push_handlers(keys)
win.push_handlers(pyglet.window.event.WindowEventLogger())
pyglet.app.run()

