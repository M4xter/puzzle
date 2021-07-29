# -*- coding: Utf-8 -*
import pygame as pg
from pygame.locals import *

class Piece(pg.sprite.Sprite):
    """Classe permettant la création d'un objet Piece pour le jeu Pygzzle."""
    
    def __init__(self,image,indiceColonne,indiceLigne,rotation,colonneBoite):
        pg.sprite.Sprite.__init__(self,self.containers)

        # coordonnées en (colonne,ligne) de la pièce dans un tableau imaginaire de découpage de l'image
        self.indiceColonne = indiceColonne
        self.indiceLigne = indiceLigne

        # colonne de positionnement dans la boite pour calculer son rectInitialBoite
        self.colonneBoite = colonneBoite

        # facteur de rotation à 90 degrés compris entre 0 et 3, 0=image à l'endroit
        self.rotation = rotation

        # surface à afficher qui contiendra l'image de la pièece plus un cadre rouge si elle n'est pas
        # à sa position vraie
        self.image = pg.Surface((64,64)).convert()

        # l'image de la pièece après rotation
        self.imagePiece = pg.transform.rotate(image,-90*self.rotation)        

        # marge de la boite
        self.margeHorizontale = 4
        self.margeVerticale = 18

        # calcule du Rect initial(invariant) de la pièce dans la boite à comparer avec rectBoite pour déterminer les limites de scrolling
        self.rectInitialBoite = self.image.get_rect(x=(self.colonneBoite*64)+(self.colonneBoite+1)*self.margeHorizontale,
                                                       y=self.margeVerticale+572)
                                                         
        # Rect(variant) de la pièce dans la boite en fonction du scrolling
        self.rectBoite = self.rectInitialBoite.copy()

        # Rect(variant) de la pièce si celle-ci est sélectionnée
        self.rect = self.rectInitialBoite.copy()

        # Rect de 20x20 autour du centre de la position vraie de la pièce dans le plateau
        self.rectPositionnementPlateau = Rect(self.indiceColonne*64+32-10,self.indiceLigne*64+32-10+60,20,20)        

        # booléen qui empèche le scrolling de la pièce si celle-ci est sur le plateau
        self.surPlateau = False

        # booléen qui empèche la sélection de la pièece si celle-ci est à sa position vraie
        self.fixe = False

    def update(self,scrollingDroit,scrollingGauche):
        """Scrolling de la boite."""

        if scrollingDroit:
            if self.rectBoite.x - self.rectInitialBoite.x < 0:
                self.rectBoite.x += 8
                if not self.surPlateau:
                    self.rect.x += 8
        elif scrollingGauche:
            if self.rectBoite.x - self.rectInitialBoite.x >= -3840:
                self.rectBoite.x -= 8
                if not self.surPlateau:
                    self.rect.x -= 8

    def draw(self,surface):
        """Dessin de l'image de la pièce et de son rectangle englobant dans la surface."""
        
        self.image.fill((0,0,0))
        self.image.blit(self.imagePiece,(0,0))
        if not self.fixe:
            pg.draw.rect(self.image,(255,0,0),(0,0,64,64),1)
        
        surface.blit(self.image,self.rect)

        
