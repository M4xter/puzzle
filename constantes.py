import pygame as pg
from pygame.locals import *
import os,sys,glob

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.mixer.pre_init(22050,16,2,512)    
pg.init()
pg.key.set_repeat(20,100)

pg.display.set_mode((512,672),0)   

infoDisplay = pg.display.Info()
LARGEUR_ECRAN = infoDisplay.current_w
HAUTEUR_ECRAN = infoDisplay.current_h

TITRE = "PYGZZLE 1.0"

FPS = 30

#--- IMAGES
#-- background
BACKGROUND_INTERFACE1 = pg.image.load(os.path.join("Ressources","Images","backgroundInterface1.bmp")).convert()
BACKGROUND_INTERFACE2 = pg.image.load(os.path.join("Ressources","Images","backgroundInterface2b.bmp")).convert()

#-- images puzzle
IMAGE_PUZZLE1 = pg.image.load(os.path.join("Ressources","Images","image_puzzle1.jpg")).convert()
IMAGE_PUZZLE2 = pg.image.load(os.path.join("Ressources","Images","image_puzzle2.jpg")).convert()
IMAGE_PUZZLE3 = pg.image.load(os.path.join("Ressources","Images","image_puzzle3.jpg")).convert()
IMAGE_PUZZLE4 = pg.image.load(os.path.join("Ressources","Images","image_puzzle4.jpg")).convert()
IMAGE_PUZZLE5 = pg.image.load(os.path.join("Ressources","Images","image_puzzle5.jpg")).convert()
IMAGE_PUZZLE6 = pg.image.load(os.path.join("Ressources","Images","image_puzzle6.jpg")).convert()
IMAGE_PUZZLE7 = pg.image.load(os.path.join("Ressources","Images","image_puzzle7.jpg")).convert()
IMAGE_PUZZLE8 = pg.image.load(os.path.join("Ressources","Images","image_puzzle8.jpg")).convert()
IMAGE_PUZZLE9 = pg.image.load(os.path.join("Ressources","Images","image_puzzle9.jpg")).convert()

#--- SONS
#-- jeu
SON1 = pg.mixer.Sound(os.path.join("Ressources","Sons","piece_tomb2.wav"))
SON1.set_volume(1/10.)
SON2 = pg.mixer.Sound(os.path.join("Ressources","Sons","glass-cork-close-1.wav"))
SON2.set_volume(1/10.)
#--- Musique
MUSIQUE = os.path.join("Ressources","Sons","Evan_Schaeffer_-_06_-_React.mp3")
pg.mixer.music.set_volume(1/10.)

#--- Font
PATH_FONT = os.path.join("Ressources","Font","Fonts Bomb JiGSAW.ttf")
