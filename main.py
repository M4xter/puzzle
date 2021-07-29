# -*- coding: Utf-8 -*
################################################################################
#                                                                              #
#                              PYGZZLE                                         #
#                                                                              #
#                        Jeu de type puzzle                                    #
#                                                                              #
#                       langage : Python 2.7                                   #
#                       API     : Pygame 1.9                                   #
#                       date    : 30/08/2017                                   #
#                       version : 1.0                                          #
#                       auteur  : guillaume michon                             #
#                                                                              #
################################################################################

from constantes import *
from plateau import *
from interface import*

class Pygzzle(object):
    def __init__(self):
        """Class principale préparant le jeu avant son lancement."""        

        #+- Surface du Display 
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        #+- Attributs de contrôle du jeu
        self.quitterJeu = False
        self.retourMenu = False

        #+- Attribut contenant un plateau 
        self.plateau = None
        
        #+- Attribut contenant l'affichage des infos        
        self.interface = Interface(self.screen)

        #+- Attribut de l'horloge de pygame
        self.clock = pg.time.Clock()

        #+- booléens options
        self.modeEcran = 0
        self.musique = True
        self.son = True
        
    def event_loop(self):
        """Récupération des événements utilisateur."""

        for event in pg.event.get():
            # /-------------------------- CLAVIER --------------------------------\
            # |----------------------- Touche relachée ---------------------------|
            if event.type == KEYUP:
                # touche 'echapement' : retour
                if event.key == K_ESCAPE:
                    self.retourMenu = True

            # /-------------------------- SOURIS ---------------------------------\
            # |------------------------- Survole ---------------------------------|
            # affichage ou non de l'image
            if self.interface.rectTexteLabelAfficherImage.collidepoint(pg.mouse.get_pos()):
                self.plateau.afficherImage = True
            else:
                self.plateau.afficherImage = False
            # scrolling pièces
            if self.interface.rectSurfaceScrollingDroit.collidepoint(pg.mouse.get_pos()):
                self.plateau.scrollingDroit = True
                self.plateau.scrollingGauche = False 
            elif self.interface.rectSurfaceScrollingGauche.collidepoint(pg.mouse.get_pos()):
                self.plateau.scrollingGauche = True
                self.plateau.scrollingDroit = False                
            else:
                self.plateau.scrollingDroit = False
                self.plateau.scrollingGauche = False
                
            # |-------------------- Clique gauche enfoncé ------------------------|
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # quitter
                if self.interface.rectSurfaceQuitter.collidepoint(pg.mouse.get_pos()):
                    self.retourMenu = True
                # plein ecran on/off
                if self.interface.rectSurfacePleinEcran.collidepoint(pg.mouse.get_pos()):                        
                    if self.modeEcran == 0:
                        self.modeEcran = FULLSCREEN
                    elif self.modeEcran == FULLSCREEN:
                        self.modeEcran = 0
                    pg.display.set_mode((512,672),self.modeEcran)
                # musique on/off
                if self.interface.rectSurfaceMusique.collidepoint(pg.mouse.get_pos()):
                    self.musique = not self.musique
                    if self.musique:
                        pg.mixer.music.set_volume(1/10.)
                    else:
                        pg.mixer.music.set_volume(0)
                # son on/off
                if self.interface.rectSurfaceSon.collidepoint(pg.mouse.get_pos()):
                    self.son = not self.son
                    if self.son:
                        SON1.set_volume(1/10.)
                        SON2.set_volume(1/10.)
                    else:
                        SON1.set_volume(0)
                        SON2.set_volume(0)                    
                # sélection d'une pièce
                if self.plateau.rectPlateau.collidepoint(pg.mouse.get_pos()) or\
                   self.plateau.rectBoite.collidepoint(pg.mouse.get_pos()):
                    self.plateau.mouse_button_down()

            # |-------------------- Clique gauche relaché ------------------------|
            elif event.type == MOUSEBUTTONUP and event.button == 1 :
                # dans l'interface ou la boite
                if self.interface.rectSurfaceInterface1.collidepoint(pg.mouse.get_pos()) or \
                   self.plateau.rectBoite.collidepoint(pg.mouse.get_pos()):
                    self.plateau.mouse_button_up(placeSurPlateau=False)
                # sur le plateau
                else:
                    self.plateau.mouse_button_up(placeSurPlateau=True)

            # |-------------------- Clique droit relaché -------------------------|
            elif event.type == MOUSEBUTTONUP and event.button == 3 :
                # rotation pièece
                self.plateau.rotation()                    

    def update(self):
        """Méthode de mise à jour des éléments du jeu."""

        self.interface.update(self.musique,self.son)        
        self.plateau.update()
            
    def draw(self):
        """Dessine le plateau courant et l'interface."""
        
        self.screen.fill((225,225,150))
        self.plateau.draw()
        self.interface.draw()          

    def display_fps(self):
        """Montre le taux de FPS."""

        caption = "{} - FPS: {:.0f}/{}".format(TITRE, self.clock.get_fps(),FPS)
        pg.display.set_caption(caption)

    def main_loop(self):
        """Boucle principale."""

        self.retourMenu = False
        while not self.retourMenu:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)
            self.display_fps()        

    def menu(self):
        """"Menu principal."""

        font = pg.font.Font(PATH_FONT,80)
        texteTitre = font.render("PYGZZLE",1,(250,250,250))
        rectTexteTitre = texteTitre.get_rect(centerx=512/2,centery=90)

        font = pg.font.Font(None,20)
        texteProgrammeur = font.render("v1.0 par M4xter",1,(250,250,250))
        rectTexteProgrammeur = texteProgrammeur.get_rect(centerx=512/2,centery=630)
        texteCompositeur = font.render("Musique : Evan Schaeffer",1,(250,250,250))
        rectTexteCompositeur = texteCompositeur.get_rect(centerx=512/2,centery=650)        
        
        image1a = pg.transform.smoothscale(IMAGE_PUZZLE1,(128,128))
        rectImage1a = image1a.get_rect(center=(96,230))        
        image1b = pg.transform.smoothscale(IMAGE_PUZZLE1,(134,134))
        rectImage1b = image1b.get_rect(center=(96,230))

        image2a = pg.transform.smoothscale(IMAGE_PUZZLE2,(128,128))
        rectImage2a = image2a.get_rect(center=(256,230))
        image2b = pg.transform.smoothscale(IMAGE_PUZZLE2,(134,134))
        rectImage2b = image2b.get_rect(center=(256,230))

        image3a = pg.transform.smoothscale(IMAGE_PUZZLE3,(128,128))
        rectImage3a = image3a.get_rect(center=(416,230))
        image3b = pg.transform.smoothscale(IMAGE_PUZZLE3,(134,134))
        rectImage3b = image3b.get_rect(center=(416,230))

        image4a = pg.transform.smoothscale(IMAGE_PUZZLE4,(128,128))
        rectImage4a = image4a.get_rect(center=(96,380))
        image4b = pg.transform.smoothscale(IMAGE_PUZZLE4,(134,134))
        rectImage4b = image4b.get_rect(center=(96,380))

        image5a = pg.transform.smoothscale(IMAGE_PUZZLE5,(128,128))
        rectImage5a = image5a.get_rect(center=(256,380))
        image5b = pg.transform.smoothscale(IMAGE_PUZZLE5,(134,134))
        rectImage5b = image5b.get_rect(center=(256,380))

        image6a = pg.transform.smoothscale(IMAGE_PUZZLE6,(128,128))
        rectImage6a = image6a.get_rect(center=(416,380))
        image6b = pg.transform.smoothscale(IMAGE_PUZZLE6,(134,134))        
        rectImage6b = image6b.get_rect(center=(416,380))

        image7a = pg.transform.smoothscale(IMAGE_PUZZLE7,(128,128))
        rectImage7a = image7a.get_rect(center=(96,530))
        image7b = pg.transform.smoothscale(IMAGE_PUZZLE7,(134,134))
        rectImage7b = image7b.get_rect(center=(96,530))

        image8a = pg.transform.smoothscale(IMAGE_PUZZLE8,(128,128))
        rectImage8a = image8a.get_rect(center=(256,530))
        image8b = pg.transform.smoothscale(IMAGE_PUZZLE8,(134,134))        
        rectImage8b = image8b.get_rect(center=(256,530))

        image9a = pg.transform.smoothscale(IMAGE_PUZZLE9,(128,128))
        rectImage9a = image9a.get_rect(center=(416,530))
        image9b = pg.transform.smoothscale(IMAGE_PUZZLE9,(134,134))
        rectImage9b = image9b.get_rect(center=(416,530))

        pg.mixer.music.load(MUSIQUE)
        pg.mixer.music.play(-1)

        while not self.quitterJeu:
            for event in pg.event.get():
                # /-------------------------- CLAVIER --------------------------------\
                # |----------------------- Touche relachée ---------------------------|
                if event.type == KEYUP:
                    # touche échap
                    if event.key == K_ESCAPE:
                        self.quitterJeu = True

                # /-------------------------- SOURIS ---------------------------------\
                # |------------------------- Survole ---------------------------------|
                # grossissement de l'image survolée
                if rectImage1a.collidepoint(pg.mouse.get_pos()):
                    image1 = image1b
                    rectImage1 = rectImage1b
                else:
                    image1 = image1a
                    rectImage1 = rectImage1a
                    
                if rectImage2a.collidepoint(pg.mouse.get_pos()):
                    image2 = image2b
                    rectImage2 = rectImage2b                                       
                else:
                    image2 = image2a
                    rectImage2 = rectImage2a

                if rectImage3a.collidepoint(pg.mouse.get_pos()):
                    image3 = image3b
                    rectImage3 = rectImage3b                                       
                else:
                    image3 = image3a
                    rectImage3 = rectImage3a

                if rectImage4a.collidepoint(pg.mouse.get_pos()):
                    image4 = image4b
                    rectImage4 = rectImage4b
                else:
                    image4 = image4a
                    rectImage4 = rectImage4a
                    
                if rectImage5a.collidepoint(pg.mouse.get_pos()):
                    image5 = image5b
                    rectImage5 = rectImage5b
                else:
                    image5 = image5a
                    rectImage5 = rectImage5a

                if rectImage6a.collidepoint(pg.mouse.get_pos()):
                    image6 = image6b
                    rectImage6 = rectImage6b
                else:
                    image6 = image6a
                    rectImage6 = rectImage6a
                    
                if rectImage7a.collidepoint(pg.mouse.get_pos()):
                    image7 = image7b
                    rectImage7 = rectImage7b
                else:
                    image7 = image7a
                    rectImage7 = rectImage7a
                    
                if rectImage8a.collidepoint(pg.mouse.get_pos()):
                    image8 = image8b
                    rectImage8 = rectImage8b
                else:
                    image8 = image8a
                    rectImage8 = rectImage8a
                    
                if rectImage9a.collidepoint(pg.mouse.get_pos()):
                    image9 = image9b
                    rectImage9 = rectImage9b
                else:
                    image9 = image9a
                    rectImage9 = rectImage9a
                
                # |-------------------- Clique gauche enfoncé ------------------------|
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # quitter
                    if self.interface.rectSurfaceQuitter.collidepoint(pg.mouse.get_pos()):
                        self.quitterJeu = True
                    # plein ecran on/off
                    elif self.interface.rectSurfacePleinEcran.collidepoint(pg.mouse.get_pos()):                        
                        if self.modeEcran == 0:
                            self.modeEcran = FULLSCREEN
                            pg.display.set_mode((512,672),self.modeEcran)
                        elif self.modeEcran == FULLSCREEN:
                            self.modeEcran = 0
                            pg.display.set_mode((512,672),self.modeEcran)
                    # musique on/off
                    elif self.interface.rectSurfaceMusique.collidepoint(pg.mouse.get_pos()):
                        self.musique = not self.musique
                        if self.musique:
                            self.interface.update(self.musique,self.son,True)
                            pg.mixer.music.set_volume(1/10.)
                        else:
                            self.interface.update(self.musique,self.son,True)                            
                            pg.mixer.music.set_volume(0)                        
                    # son on/off
                    elif self.interface.rectSurfaceSon.collidepoint(pg.mouse.get_pos()):
                        self.son = not self.son
                        if self.son:
                            self.interface.update(self.musique,self.son,True)                            
                            SON1.set_volume(1/10.)
                            SON2.set_volume(1/10.)
                        else:
                            self.interface.update(self.musique,self.son,True)
                            SON1.set_volume(0)
                            SON2.set_volume(0)                        
                    # sélection image
                    elif rectImage1.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE1)
                        self.main_loop()
                    elif rectImage2.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE2)
                        self.main_loop()
                    elif rectImage3.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE3)
                        self.main_loop()                        
                    elif rectImage4.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE4)
                        self.main_loop()
                    elif rectImage5.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE5)
                        self.main_loop()
                    elif rectImage6.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE6)
                        self.main_loop()
                    elif rectImage7.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE7)
                        self.main_loop()
                    elif rectImage8.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE8)
                        self.main_loop()                        
                    elif rectImage9.collidepoint(pg.mouse.get_pos()):
                        self.plateau = Plateau(self.screen,IMAGE_PUZZLE9)
                        self.main_loop()                                                


            self.screen.fill((125,125,150))
            self.screen.blit(self.interface.surfaceQuitter,self.interface.rectSurfaceQuitter)
            self.screen.blit(self.interface.surfaceMusique,self.interface.rectSurfaceMusique)
            self.screen.blit(self.interface.surfaceSon,self.interface.rectSurfaceSon)
            self.screen.blit(self.interface.surfacePleinEcran,self.interface.rectSurfacePleinEcran)
            self.screen.blit(texteCompositeur,rectTexteCompositeur)                
            self.screen.blit(texteProgrammeur,rectTexteProgrammeur)
            self.screen.blit(texteTitre,rectTexteTitre)
            self.screen.blit(image1,rectImage1)
            self.screen.blit(image2,rectImage2)
            self.screen.blit(image3,rectImage3)
            self.screen.blit(image4,rectImage4)
            self.screen.blit(image5,rectImage5)
            self.screen.blit(image6,rectImage6)
            self.screen.blit(image7,rectImage7)
            self.screen.blit(image8,rectImage8)
            self.screen.blit(image9,rectImage9)                         
            pg.display.flip()

            self.clock.tick(FPS)
            self.display_fps()
        
if __name__ == "__main__":

    pygzzle = Pygzzle()
    pygzzle.menu()
    
    pg.quit()
    try:
        sys.exit()
    except:
        pass
