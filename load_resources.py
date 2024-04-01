#import main

import pyglet
from pyglet import resource
#-----------------------------------------------------------
# LOAD RESOURCES
#-----------------------------------------------------------

# to draw by batch
batch = pyglet.graphics.Batch()
wrapping_batch = pyglet.graphics.Batch()

resource.path.append('res')
resource.reindex()

pointer_image = resource.image('arrow.png')
pointer_image.width = pointer_image.width
pointer_image.height = pointer_image.height
pointer_image.anchor_x = pointer_image.width // 2
pointer_image.anchor_y = pointer_image.height // 2
pointer_image_flip = resource.image('arrow.png', flip_x=True)
pointer_image_flip.width = pointer_image_flip.width
pointer_image_flip.height = pointer_image_flip.height
pointer_image_flip.anchor_x = pointer_image_flip.width // 2
pointer_image_flip.anchor_y = pointer_image_flip.height // 2

pybilisan = resource.image('title.png')
paano_title = resource.image('paano_title.png')
baguhin_title = resource.image('baguhin_title.png')
leaderboard_title = resource.image('leaderboard_title.png')
character_select_title = resource.image('character_select_title.png')
maglaro_title = resource.image('maglaro_title.png')
game_over_title = resource.image('natalo_ka_title.png')

#MAIN MENU
main_menu_bg = resource.image('main_menu_bg.png')
game_bg = resource.image('game_bg.png')

bg_list = []

#MAIN MENU ITEMS
maglaro_btn = resource.image("maglaro_btn.png")
paano_btn = resource.image("paano_btn.png")
baguhin_btn = resource.image("baguhin_btn.png")
leaderboard_btn = resource.image("leaderboard_btn.png")
umalis_btn = resource.image("umalis_btn.png")
OK_btn = resource.image("OK_btn.png")

maglaro_btn_pressed = resource.image("maglaro_btn_pressed.png")
paano_btn_pressed = resource.image("paano_btn_pressed.png")
baguhin_btn_pressed = resource.image("baguhin_btn_pressed.png")
leaderboard_btn_pressed = resource.image("leaderboard_btn_pressed.png")
umalis_btn_pressed = resource.image("umalis_btn_pressed.png")
OK_btn_pressed = resource.image("OK_btn_pressed.png")

#PAANO MAGLARO ITEMS
directions = pyglet.image.load_animation("res/direction.gif")

#BAGUHIN ANG LARO ITEMS

#MGA LEBEL
lebel_1 = resource.image("lebel_1.png")
lebel_2 = resource.image("lebel_2.png")
lebel_3 = resource.image("lebel_3.png")

#SOUND ON/OFF
sound_on = resource.image("sound on.png")
sound_off = resource.image("sound off.png")

#FPS ON/OFF
fps_on = resource.image("fps on.png")
fps_off = resource.image("fps off.png")

# SOUNDS
button_sound = resource.media('button_sound.wav', streaming=False)
disabled_sound = resource.media('disabled_sound.wav', streaming=False)
buy_sound = resource.media('buy_sound.wav', streaming=False)
bg_sound = resource.media('bg_sound.wav', streaming=True)
game_sound = resource.media('game_sound.wav', streaming=True)
#RANGGO NG ISKOR ITEMS
box = resource.image("box.png")
box_small = resource.image("box_small.png")

#MAGLARO ITEMS
blank_light_btn = resource.image("blank_light_btn.png")
blank_btn = resource.image("blank_btn.png")
blank_yellow_btn = resource.image("blank_yellow_btn.png")
blank_red_btn = resource.image("blank_red_btn.png")
blank_light_grey_btn = resource.image("blank_light_grey_btn.png")
blank_grey_btn = resource.image("blank_grey_btn.png")
back_btn = resource.image("back_btn.png")
back_btn_pressed = resource.image("back_btn_pressed.png")
stats = resource.image("stats.png")
stats.width = stats.width // 1.5
stats.height = stats.height // 1.5


resource.path.append('animals')
resource.reindex()

#CHARACTERS
animals = []

sisiw_01 = resource.image("01 sisiw.png")
animals.append(sisiw_01)
daga_02 = resource.image("02 daga.png")
animals.append(daga_02)
palaka_03 = resource.image("03 palaka.png")
animals.append(palaka_03)
unggoy_04 = resource.image("04 unggoy.png")
animals.append(unggoy_04)
baka_05 = resource.image("05 baka.png")
animals.append(baka_05)
pusa_06 = resource.image("06 pusa.png")
animals.append(pusa_06)
aso_07 = resource.image("07 aso.png")
animals.append(aso_07)
uso_08 = resource.image("08 uso.png")
animals.append(uso_08)
lobo_09 = resource.image("09 lobo.png")
animals.append(lobo_09)
oso_10 = resource.image("10 oso.png")
animals.append(oso_10)
koala_11 = resource.image("11 koala.png")
animals.append(koala_11)
panda_12 = resource.image("12 panda.png")
animals.append(panda_12)
tigre_13 = resource.image("13 tigre.png")
animals.append(tigre_13)
leon_14 = resource.image("14 leon.png")
animals.append(leon_14)

for animal in animals:
    animal.width = animal.width//4
    animal.height = animal.height//4

#COINS
coins_icon = resource.image("coin.png")
coins_icon.width = coins_icon.width // 12
coins_icon.height = coins_icon.height // 12

#IN-GAME
obstacle_game = resource.image('rock.png')
obstacle_game.width = obstacle_game.width // 2.5
obstacle_game.height = obstacle_game.height // 2.5
coin_game = resource.image('coin_game.png')
coin_game.width = coin_game.width // 3.5
coin_game.height = coin_game.height // 3.5
life_game = resource.image('life.png')