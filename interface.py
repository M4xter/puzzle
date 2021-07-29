# -*- coding: Utf-8 -*
################################################################################
#                                                                              #
#                        Classe Interface pour le jeu Pygzzle                  #
#                                                                              # 
################################################################################

from constantes import *
from sprites import *

class Interface(object):
    def __init__(self,screen,plateau=None):
        """Classe interface qui crée une surface contenant les options et 2 petites surfaces pour le scrolling
           quand la souris les survole."""

        # surface du display
        self.screen = screen

        # surface du haut
        self.surfaceInterface1 = pg.Surface((512,60)).convert()
        self.rectSurfaceInterface1 = self.surfaceInterface1.get_rect()

        # surface de scrolling des pièeces vers la droite
        self.surfaceScrollingDroit = pg.Surface((30,100)).convert()
        self.surfaceScrollingDroit.fill((12,153,186))
        self.surfaceScrollingDroit.set_alpha(150)
        self.rectSurfaceScrollingDroit = self.surfaceScrollingDroit.get_rect(x=0,y=572)

        # surface de scrolling des pièeces vers la gauche
        self.surfaceScrollingGauche = pg.Surface((30,100)).convert()
        self.surfaceScrollingGauche.fill((12,153,186))
        self.surfaceScrollingGauche.set_alpha(150)
        self.rectSurfaceScrollingGauche = self.surfaceScrollingGauche.get_rect(x=482,y=572)

        # textes des options
        self.font = pg.font.Font(PATH_FONT,30)
        self.texteLabelAfficherImage = self.font.render("Afficher Image",1,(204,255,255))
        self.rectTexteLabelAfficherImage = self.texteLabelAfficherImage.get_rect(centerx=self.rectSurfaceInterface1.w/2,y=22)
        
        self.font = pg.font.Font(None,24)
        self.textePiecesGauche = self.font.render("0",1,(255,255,255))
        self.textePiecesDroite = self.font.render("64",1,(255,255,255))
        
        self.font = pg.font.Font(None,20)
        self.surfaceQuitter = self.font.render("Quitter",1,(255,255,255))
        self.rectSurfaceQuitter = self.surfaceQuitter.get_rect()

        self.surfacePleinEcran = self.font.render("Plein ecran",1,(255,255,255))
        self.rectSurfacePleinEcran = self.surfacePleinEcran.get_rect(x=435)

        self.surfaceMusiqueOn = self.font.render("Musique",1,(255,255,255))
        self.surfaceMusiqueOff = self.font.render("Musique",1,(255,0,0))
        self.surfaceMusique = self.surfaceMusiqueOn
        self.rectSurfaceMusique = self.surfaceMusiqueOn.get_rect(x=156)

        self.surfaceSonOn = self.font.render("Son",1,(255,255,255))
        self.surfaceSonOff = self.font.render("Son",1,(255,0,0))
        self.surfaceSon = self.surfaceSonOn
        self.rectSurfaceSon = self.surfaceSonOn.get_rect(x=320)

        self.font = pg.font.Font(None,24)
        
    def update(self,musiqueOn=True,sonOn=True,modeMenu=False):
        """Mise à jour des informations."""

        if musiqueOn:
            self.surfaceMusique = self.surfaceMusiqueOn
        else:
            self.surfaceMusique = self.surfaceMusiqueOff
        if sonOn:
            self.surfaceSon = self.surfaceSonOn
        else:
            self.surfaceSon = self.surfaceSonOff

        if not modeMenu:
            # compteur des pièce à droite de l'écran    
            nbrPiecesDroite = 0
            for piece in Piece.containers:
                if piece.rect.centerx > 512:
                    nbrPiecesDroite += 1
            self.textePiecesDroite = self.font.render(str(nbrPiecesDroite),1,(255,255,255))

            # compteur des pièce à gauche de l'écran            
            nbrPiecesGauche = 0
            for piece in Piece.containers:
                if piece.rect.centerx < 0:
                    nbrPiecesGauche += 1
            self.textePiecesGauche = self.font.render(str(nbrPiecesGauche),1,(255,255,255))
        
    def draw(self):
        """Dessin de l'interface."""
        
        self.surfaceInterface1.fill((0,0,0))
        self.surfaceInterface1.blit(BACKGROUND_INTERFACE1,(0,0))
        self.surfaceInterface1.blit(self.texteLabelAfficherImage,self.rectTexteLabelAfficherImage)
        self.surfaceInterface1.blit(self.surfaceQuitter,self.rectSurfaceQuitter)
        self.surfaceInterface1.blit(self.surfacePleinEcran,self.rectSurfacePleinEcran)
        self.surfaceInterface1.blit(self.surfaceMusique,self.rectSurfaceMusique)
        self.surfaceInterface1.blit(self.surfaceSon,self.rectSurfaceSon)

        self.screen.blit(self.surfaceScrollingDroit,self.rectSurfaceScrollingDroit)
        self.screen.blit(self.textePiecesGauche,(4,622))        

        self.screen.blit(self.surfaceScrollingGauche,self.rectSurfaceScrollingGauche)
        self.screen.blit(self.textePiecesDroite,(490,622))        

        self.screen.blit(self.surfaceInterface1,self.rectSurfaceInterface1)
   
