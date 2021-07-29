# -*- coding: Utf-8 -*
from constantes import *
from sprites import *
from random import choice,shuffle

class Plateau(object):
    """Classe Plateau qui gère la mise à jour des éléments (déplacements,collision,redessin)."""
    
    def __init__ (self,screen,image):

        # la surface de dessin correspondant au display
        self.screen = screen

        # l'image du puzzle
        self.image = image

        # le rect correspondant à la zone de placement des pièces
        self.rectPlateau = pg.Rect(0,60,512,512)

        # la boite des pièces mélangées(une simple surface de la largeur de l'écran)
        self.surfaceBoite = pg.Surface((512,100)).convert()
        self.surfaceBoite.fill((124,153,186))
        self.rectBoite = pg.Rect(30,572,452,100)

        # container des sprites Piece de type LayeredUpdates permettant ainsi la sélection de ceux-ci par la souris
        Piece.containers = pg.sprite.LayeredUpdates()

        # groupe d'unique sprite pour la pièce sélectionnée
        self.pieceSelectionnee = pg.sprite.GroupSingle()
        
        # création des 64 pièces par découpage de l'image en sous-surfaces de 64x64 par le biais d'une liste
        # contenant des couples de (ligne,colonne) de 0 à 7 mélangés
        colonneBoite = 0 #<- la position de la pièce dans la boite
        listeCoordPieces = []
        for i in range(8):
            for j in range(8):
                listeCoordPieces.append((i,j))
        shuffle(listeCoordPieces)
        for coord in listeCoordPieces:
            piece = Piece(self.image.subsurface((coord[1]*64,coord[0]*64,64,64)).convert(),coord[1],coord[0],choice(range(1,4)),colonneBoite)
            colonneBoite += 1

        # booléens de défilement de la boite
        self.scrollingDroit = False
        self.scrollingGauche = False

        # booléen d'affichage de l'image
        self.afficherImage = False

    def mouse_button_down(self):
        """Pick up d'une pièce."""
        
        hitList = Piece.containers.get_sprites_at(pg.mouse.get_pos())
        if hitList:
            for hit in hitList:
                if not hit.fixe:
                    self.pieceSelectionnee = hit
                    Piece.containers.move_to_front(self.pieceSelectionnee)

    def mouse_button_up(self,placeSurPlateau=False):
        """Positionnement de la pièce."""
        
        if self.pieceSelectionnee:
            # si on la lache en dehors du plateau elle reprend sa place d'origine dans la boite
            if not placeSurPlateau:
                self.pieceSelectionnee.rect = self.pieceSelectionnee.rectBoite.copy()
                self.pieceSelectionnee.surPlateau = False
                self.pieceSelectionnee = None
            # sinon on test si elle est à sa place dans le plateau
            elif placeSurPlateau:
                self.pieceSelectionnee.surPlateau = True # <- pour éviter qu'elle soit aussi déplacée pendant le scrolling
                if self.pieceSelectionnee.rectPositionnementPlateau.collidepoint(self.pieceSelectionnee.rect.center) and self.pieceSelectionnee.rotation == 0:
                    self.pieceSelectionnee.rect.center = self.pieceSelectionnee.rectPositionnementPlateau.center
                    self.pieceSelectionnee.fixe = True
                    SON1.play()
                self.pieceSelectionnee = None

    def rotation(self):
        """rotation et test de positionnement de la pièce."""
        
        hitList = Piece.containers.get_sprites_at(pg.mouse.get_pos())
        if hitList:
            self.pieceSelectionnee = hitList[0]
            if not self.pieceSelectionnee.fixe:
                Piece.containers.move_to_front(self.pieceSelectionnee)
                self.pieceSelectionnee.imagePiece = pg.transform.rotate(self.pieceSelectionnee.imagePiece,-90)
                self.pieceSelectionnee.rotation = (self.pieceSelectionnee.rotation+1)%4
                if self.pieceSelectionnee.rectPositionnementPlateau.collidepoint(self.pieceSelectionnee.rect.center) and self.pieceSelectionnee.rotation == 0:
                    self.pieceSelectionnee.rect.center = self.pieceSelectionnee.rectPositionnementPlateau.center
                    self.pieceSelectionnee.fixe = True
                if self.pieceSelectionnee.fixe:
                    SON1.play()
                else:
                    SON2.play()
        self.pieceSelectionnee = None            
        
    def update(self):
        """"Mise à jour des éléments du plateau."""

        # la pièece sélectionnée suit la souris
        if self.pieceSelectionnee:
            self.pieceSelectionnee.rect.center = pg.mouse.get_pos()
            if self.pieceSelectionnee.rect.right > 512:
                self.pieceSelectionnee.rect.right = 512
            elif self.pieceSelectionnee.rect.left < 0:
                self.pieceSelectionnee.rect.left = 0
            if self.pieceSelectionnee.rect.top < 60:
                self.pieceSelectionnee.rect.top = 60

        # déplacement de la boite 
        Piece.containers.update(self.scrollingDroit,self.scrollingGauche)
            
    def draw(self):
        """Dessin de la boite, des pièces et de l'image."""

        self.screen.blit(self.surfaceBoite,(0,572))        
        for piece in Piece.containers:
            piece.draw(self.screen)
        if self.afficherImage:
            self.screen.blit(self.image,(0,60))
