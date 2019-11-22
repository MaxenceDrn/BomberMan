#!/usr/bin/python3

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import numpy as np
from random import randint
import time
import subprocess

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette()
        p.setColor(QPalette.Window, QColor(72,72,72))
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,150,0))
        self.setPalette(p)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self): # Initialisation de la fenêtre

        # Initialisation de la fenêtre principale
        self.setGeometry(10, 10, 1200, 900)
        self.setWindowTitle('Bomberman')
        self.setCenter()

        # Initialisation des différentes variables du jeu
        self.initVar()

        # Initialisation de la fenêtre de jeu
        self.initMatrice()

        # Initialisation menu sur la droite
        self.initMenu()

        # Initialisation des textures
        self.initTextures()

        # Initialisation de la bombe
        self.initBombe()

        # Initialisation Déplacement perso + Bombes
        self.initPerso()

        # Initialisation de l'IA
        self.initIA()


        self.show()
    
    def initVar(self): # Fonction permettant l'initialisation de toutes les variables du code
        global posee,walkIA,powerState, timerBonus, powerSpawned ,etatIA,timer, indXIA,posXB12,posYB12, indYIA, posXIA,bombe2, posYIA, scoreP, tabDroiteIA, tabGaucheIA, tabFaceIA, tabDosIA,tabDroite, tabGauche, tabFace, tabDos, tabBomb, walk, indX, indY, moveBoardD, moveBoardQ, moveBoardZ, moveBoardZ, posX, posY, bombe1, posXB11, posYB11, rad

        # Tableaux des textures en fonctions des orientations et de l'évolution du personnage dans l'espace.
        tabDroite=["./img/perso/droite1.png","./img/perso/droite3.png","./img/perso/droite3.png"]
        tabGauche=["./img/perso/gauche1.png","./img/perso/gauche2.png","./img/perso/gauche3.png"]
        tabFace=["./img/perso/face1.png","./img/perso/face2.png","./img/perso/face3.png"]
        tabDos=["./img/perso/dos1.png","./img/perso/dos2.png","./img/perso/dos3.png"]

        tabDroiteIA=["./img/IA/droite1.png","./img/IA/droite3.png","./img/IA/droite3.png"]
        tabGaucheIA=["./img/IA/gauche1.png","./img/IA/gauche2.png","./img/IA/gauche3.png"]
        tabFaceIA=["./img/IA/face1.png","./img/IA/face2.png","./img/IA/face3.png"]
        tabDosIA=["./img/IA/dos1.png","./img/IA/dos2.png","./img/IA/dos3.png"]

        # Différentes variables utilisées dans le code

        scoreP = 0 # valeur numérique du score
        rad = 1 # valeur numérique du rayon d'effet de la bombe
        walk = 0 # compteur dans les différents tableaux
        walkIA = 0 #compteur pour l'IA
        indX = 1 # position du personnage dans boardB
        indY = 1 # position du personnage dans board B
        moveBoardD = 0
        moveBoardQ = 0
        moveBoardZ = 0
        moveBoardS = 0
        posX = 60 # position du personnage en pixel
        posY = 60 # position du personnage en pixel
        bombe1 = False # etat de bombe 1
        bombe2 = False # etat de bombe 2
        posXB11 = 1 # position de bombe 1 dans bombB
        posYB11 = 1 # position de bombe 1 dans bombB
        posXB12 = 1 # position de bombe 2 dans bombB
        posYB12 = 1 # position de bombe 2 dans bombB

        posee = 0 #Permet de gérer la 1ere action lorsque l'ia pose une bombe
        indXIA = 13 # position de l'IA dans boardB
        indYIA = 13 # position de l'IA dans boardB
        posXIA = 13 * 60 # position de l'IA en pixel
        posYIA = (13 * 60) - 30 # position de l'IA en pixel
        timer = QTimer(self) # Initilisation du timer principal de l'IA
        etatIA = True # Etat de l'IA
        
        powerSpawned = False
        powerState = False
        indXPo= 0
        indYPo= 0

        self.vieIA() # Démarrage de l'IA
        

    def initMenu(self): # Fonction permettant l'initialisation du menu
        global nb, etatBonus

        # Image de background du menu
        background = QLabel(self)
        background.setPixmap(QPixmap('./img/bar/background.jpg'))
        background.setGeometry(900, 0, 700, 900)
        background.show()

        # Bouton pause
        pauseButton = QPushButton(self)
        pauseButton.setText("Pause")
        pauseButton.setGeometry(975, 850, 50, 45)
        pauseButton.show()

        # Bouton reset
        resetButton = QPushButton(self)
        resetButton.setText("Reset")
        resetButton.setGeometry(1057.5, 850, 50, 45)
        resetButton.show()

        # Connexion des boutons aux fonctions associées
        resetButton.clicked.connect(self.reset)
        pauseButton.clicked.connect(self.pause)

        # Image du tableau de score
        score = QLabel(self)
        score.setPixmap(QPixmap('./img/bar/score1.png'))
        score.setGeometry(950, 0, 200, 150)
        score.show()

        # QLabel contenant la valeur du score
        nb = QLabel(self)
        nb.setText('0')
        nb.setGeometry(950, 0, 200, 150)
        nb.setAlignment(Qt.AlignCenter)
        nb.setFont(QFont('Impact', 35))
        nb.show()

        # Logo du jeu
        logo = QLabel(self)
        logo.setPixmap(QPixmap('./img/bar/logoJeu.png'))
        logo.setGeometry(950, 150, 200, 250)
        logo.show()

        etatBonus = QLabel(self)
        etatBonus.setPixmap(QPixmap('./img/bombe/powerUP.png'))
        etatBonus.setGeometry(950, 250, 60, 60)
        etatBonus.hide()


    def reset(self): # Fonction permettant de stopper la partie actuelle et de la remplacer par une nouvelle.
        timer.stop() # Arret du timer de l'IA

        # masquage des textures des perso de la partie en cours
        self.persoDroite.hide()
        self.persoGauche.hide()
        self.persoFace.hide()
        self.persoDos.hide()
        self.IADroite.hide()
        self.IAGauche.hide()
        self.IAFace.hide()
        self.IADos.hide()
        time.sleep(1)
        self.initVar()

        # Ré-initialisation de la fenêtre de jeu
        self.initMatrice()
        time.sleep(0.25)
        # Ré-initialisation menu sur la droite
        self.initMenu()
        time.sleep(0.25)
        # Ré-initialisation des textures
        self.initTextures()
        time.sleep(0.25)
        # Ré-initialisation de la bombe
        self.initBombe()
        time.sleep(0.25)
        # Ré-initialisation Déplacement perso + Bombes
        self.initPerso()
        time.sleep(0.25)
        # Ré-initialisation de l'IA
        self.initIA()
        time.sleep(0.25)
        self.show()

    def pause(self): # Fonction permettant de mettre le jeu en pause

        timer.stop() # Mise en pause du timer de l'IA
        QMessageBox.about(self, "Pause", "Reprendre ?") # Affichage de la boite de dialog
        timer.start(500) # Reprise du timer de l'IA après avoir quitter la boite de dialogue

    def setCenter(self): # Fonction permettant de mettre la fenêtre au centre de l'écran
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initBombe(self): # Fonction permettant l'initialisation de la bombe
        # Image de la bombe
        self.bomb1 = QLabel(self)
        self.bomb1.setPixmap(QPixmap('./img/60x60/bombe1.png'))
        self.bomb1.setGeometry(0,0,0,0)

    def initPerso(self): # Fonction permettant l'initialisation du joueur
        global posX, posY

        #Image de gauche
        self.persoGauche = QLabel(self)
        self.persoGauche.setPixmap(QPixmap('./img/perso/gauche1.png'))
        self.persoGauche.setGeometry(posX,posY,0,0)

        #Image de droite
        self.persoDroite = QLabel(self)
        self.persoDroite.setPixmap(QPixmap('./img/perso/droite1.png'))
        self.persoDroite.setGeometry(posX,posY,0,0)

        #Image de face
        self.persoFace = QLabel(self)
        self.persoFace.setPixmap(QPixmap('./img/perso/face1.png'))
        self.persoFace.setGeometry(posX,posY,70,60)

        #Image de dos
        self.persoDos = QLabel(self)
        self.persoDos.setPixmap(QPixmap('./img/perso/dos1.png'))
        self.persoDos.setGeometry(posX,posY,0,0)

        self.persoGauche.show()
        self.persoDroite.show()
        self.persoFace.show()
        self.persoDos.show()
        # Quand le jeu est lancé on montre l'image de face

    def initMatrice(self): # Fonction qui sert à créer une matrice de la taille du plateau de jeu.
        # /!\ Attention, lorsque que je dis on met un sol ou un mur ici: un mur = -1 et un sol = 0, on ne met pas encore les textures
        global boardB, bombB
        boardB = [] # Matrice pour le déplacement du personnage / de l'IA
        bombB = [] # Matrice pour la position des bombes
        for i in range(15):
            line = []
            lineBomb = []
            if i == 0 or i == 14: # Si on est a la toute première ligne ou à la toute dernière on met des murs
                for j in range(15):
                    line.append(-1)
                    lineBomb.append(-1)
                boardB.append(line)
                bombB.append(lineBomb)
            elif i == 1 or i == 13: # Si c'est la 2e ou 14e ligne.
                for l in range(15):
                    if l == 0 or l == 14: # Si c'est la première ou derniere colonne on pose un mur
                        line.append(-1)
                        lineBomb.append(-1)
                    else: # Sinon, on pose un sol.
                        line.append(0)
                        lineBomb.append(0)
                boardB.append(line)
                bombB.append(lineBomb)
            elif i % 2 == 0: # Si on est sur une ligne d'indice paire
                for k in range(15):
                    if k % 2 == 0: #Si on a une colonne d'indice paire on alterne entre mur et sol
                        line.append(-1)
                        lineBomb.append(-1)
                    else: # Sinon on pose des sols
                        line.append(0)
                        lineBomb.append(0)
                boardB.append(line)
                bombB.append(lineBomb)
            else:
                for j in range(15): # Si c'est la 14e ligne du tableau
                    if j == 0 or j == 14: # On met un mur à gauche et a droite
                        line.append(-1)
                        lineBomb.append(-1)
                    else: # On met un sol au milieu
                        line.append(0)
                        lineBomb.append(0)
                boardB.append(line)
                bombB.append(lineBomb)

        for m in range(2): # Boucle qui permet de faire apparaitre aléatoirement des brique dans la matrice.
            for i in range(15):
                for j in range(15):
                    if boardB[i][j] == 0 and (i != 1 or j != 1) and (i != 13 or j != 13) and (i!=2 or j != 1) and (i!=1 or j != 2) and (i!=12 or j!=13) and (i!=13 or j != 12):
                        k = randint(1,2)
                        if k == 1:
                            boardB[i][j] = 2
        boardB[1][1] = 10 # On indique dans la matrice la postion de l'IA au départ.
        boardB[13][14] = 9 # On fait une sortie en bas a droite.

    def initTextures(self): # Fonction qui permet l'initialisation des textures en fonction de la matrice   
        global boardB
        x = 0
        y = 0
        
        for i in range(len(boardB)): # On parcours toutes les ligne de la matrice
            for j in range(len(boardB[i])): # On parcours toutes les colonnes de la matrice
                if boardB[i][j] == -1: # Si c'est égal à -1, on pose un sol puis un mur au dessus
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry(x, y, 60,60)
                    sol.show()
                    mur = QLabel(self)
                    mur.setPixmap(QPixmap('./img/block/brique.png'))
                    mur.setGeometry(x, y, 60, 60)
                    mur.show()
                    x += 60 # On décale la position du prochain de 60 px sur la droite
                if boardB[i][j] == 0 or boardB[i][j] == 10: # Si c'est égal à 0 ou à 10, on pose un sol
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry(x, y, 60,60)
                    sol.show()
                    x += 60
                if boardB[i][j] == 2: # Si c'est égal à deux on pose un sol puis une brique (botte de paille ici)
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry(x, y, 60,60)
                    sol.show()
                    brique = QLabel(self)
                    brique.setPixmap(QPixmap('./img/block/paille.png'))
                    brique.setGeometry(x, y, 60, 60)
                    brique.show()
                    x += 60
                if boardB[i][j] == 9: # Si c'est égal à 9 on pose un sol puis la sortie.
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry(x, y, 60,60)
                    sol.show()
                    porte = QLabel(self)
                    porte.setPixmap(QPixmap('./img/block/sortie.png'))
                    porte.setGeometry(x, y, 60,60)
                    porte.show()
                    x += 60
            x = 0 # On repasse tout à gauche
            y += 60 # Et on descend d'une ligne.

    def keyPressEvent(self, event): #Fonction qui gere : les déplacement, les collisions, le placement de la bombe, le contact entre le personnage et le bonus
        global timer, scoreP, posX, posY, bombe1, bombe2, walk, indX, indY, posXB11, posYB11, posXB12, posYB12, rad, powerState
        key = event.key()
        if key == Qt.Key_D: # Le personnage va à droite
            if boardB[indY][indX +1] == 0 or boardB[indY][indX +1] == 5 or boardB[indY][indX +1] == 9: # Il peut se déplacer si c'est un sol ou un item ou la sortie
                if boardB[indY][indX +1] == 9: # Si c'est la sortie le joueur à gagné
                    self.win()
                if boardB[indY][indX +1] == 5: # Si c'est un item
                    rad = 2
                    powerState = True
                    etatBonus.show() # On montre l'item
                    timerBonus = QTimer(self)
                    timerBonus.singleShot(15000, self.resetRad) # On l'active pendant 15 sec
                    timerBonus.start()
                    self.deletePowerUP()
                # Gerer le sprite du perso pour faire une animation de déplacement
                walk += 1
                if walk ==3:
                    walk = 0
                posX += 60
                indX += 1
                boardB[indY][indX - 1] = 0
                boardB[indY][indX] = 10
            self.persoDroite.setGeometry(posX,posY,70,60)
            self.persoDos.setGeometry(posX,posY,0,0)
            self.persoGauche.setGeometry(posX,posY,0,0)
            self.persoFace.setGeometry(posX,posY,0,0)
            self.persoDroite.setPixmap(QPixmap(tabDroite[walk]))
        elif key == Qt.Key_Z:# Le personnage va vers le haut
            if boardB[indY-1][indX] == 0 or boardB[indY-1][indX] == 5:
                if boardB[indY-1][indX] == 5:
                    rad = 2
                    powerState = True
                    etatBonus.show()
                    timerBonus = QTimer(self)
                    timerBonus.singleShot(15000, self.resetRad)
                    timerBonus.start()
                    self.deletePowerUP()
                walk += 1
                if walk ==3:
                    walk = 0
                posY -= 60
                indY -= 1
                boardB[indY+1][indX] = 0
                boardB[indY][indX] = 10
                #print(np.array(boardB))
            self.persoDos.setGeometry(posX,posY,70,60)
            self.persoGauche.setGeometry(posX,posY,0,0)
            self.persoFace.setGeometry(posX,posY,0,0)
            self.persoDroite.setGeometry(posX,posY,0,0)
            self.persoDos.setPixmap(QPixmap(tabDos[walk]))
        elif key == Qt.Key_Q:#Le personnafe va vers la gauche
            if boardB[indY][indX - 1] == 0 or boardB[indY][indX -1] == 5:
                if boardB[indY][indX -1] == 5:
                    rad = 2
                    powerState = True
                    etatBonus.show()
                    timerBonus = QTimer(self)
                    timerBonus.singleShot(15000, self.resetRad)
                    timerBonus.start()
                    self.deletePowerUP()
                walk += 1
                if walk ==3:
                    walk = 0
                posX -= 60
                indX -= 1
                boardB[indY][indX+1] = 0
                boardB[indY][indX] = 10
                #print(np.array(boardB))
            self.persoGauche.setGeometry(posX,posY,70,60)
            self.persoFace.setGeometry(posX,posY,0,0)
            self.persoDroite.setGeometry(posX,posY,0,0)
            self.persoDos.setGeometry(posX,posY,0,0)
            self.persoGauche.setPixmap(QPixmap(tabGauche[walk]))
        elif key == Qt.Key_S: #Le personnage va vers le bas
            if boardB[indY+1][indX] == 0 or boardB[indY +1][indX] == 5:
                if boardB[indY +1][indX] == 5:
                    rad = 2
                    powerState = True
                    etatBonus.show()
                    timerBonus = QTimer(self)
                    timerBonus.singleShot(15000, self.resetRad)
                    timerBonus.start()
                    self.deletePowerUP()
                walk += 1
                if walk ==3:
                    walk = 0
                posY += 60
                indY += 1
                boardB[indY-1][indX] = 0
                boardB[indY][indX] = 10
                #print(np.array(boardB))
            self.persoFace.setGeometry(posX,posY,70,60)
            self.persoDroite.setGeometry(posX,posY,0,0)
            self.persoDos.setGeometry(posX,posY,0,0)
            self.persoGauche.setGeometry(posX,posY,0,0)
            self.persoFace.setPixmap(QPixmap(tabFace[walk]))
        elif key == Qt.Key_X: #Le personnage pose une bombe
            #Il peut poser une poser une bombe a la fois
            if(not bombe1):
                bombe1 = True
                bombB[indY][indX] = 11
                posXB11 = indX
                posYB11 = indY
                #Gif de la bombe
                self.bomb1 = QLabel(self)
                movie = QMovie("./img/bombe/bombePerso.gif")
                self.bomb1.setGeometry(posX,posY-3,60,60)
                self.bomb1.setMovie(movie)
                movie.start()
                self.bomb1.show()
                #Explosion de la bombe au bout de 2,7 sec
                timer1 = QTimer(self)
                timer1.singleShot(2700, self.exploser)

    def resetRad(self): # Fonction qui permet de remettre le rayon d'explosion à 1.
        global rad, etatBonus, powerState
        powerState = False # On passe l'état du bonus a Faux
        etatBonus.hide() # On fait disparaitre l'icone de bonus dans le menu
        rad = 1 # on repasse le rayon à 1

    def spawnPowerUP(self, x, y): # Fonction qui permet de faire apparaitre un Power UP
        global power, indXPo, indYPo, powerSpawned
        powerSpawned = True # On indique qu'il est apparu en changeant son état
        indXPo = x # on stock sa position dans des variable
        indYPo = y
        power = QLabel(self) # On initialise sa texture
        power.setPixmap(QPixmap('./img/bombe/powerUP.png'))
        power.setGeometry(x*60,y*60, 60, 60)
        power.show() # On le fait apparaitre
        boardB[indYPo][indXPo] = 5 # On le place dans la matrice
        timerP = QTimer(self) # On lance un timer de 5 secondes. Lorsqu'il se termine si le bonus n'a pas été récupéré, celui-ci disparait.
        timerP.singleShot(5000, self.deletePowerUP)
        timerP.start()
    
    def deletePowerUP(self): # Fonction qui permet de faire disparaitre le power up de la carte.
        global power, powerSpawned
        powerSpawned = False # Indique que le power UP a disparu en changeant son état
        power.hide() # On cache le power UP
        boardB[indYPo][indXPo] = 0 # On l'enlève de la matrice

    def exploser(self): #Fonction qui gere l'explosion de la bombe, et les briques qui se détruise.
        global bombe1, scoreP, y, x, etatIA
        x = posXB11
        y = posYB11
        if rad == 2: # Si le rayon d'explosion = 2 (Nous avons le bonus)
            if (boardB[y][x+1] == 2 or boardB[y][x+1] == 0) and (boardB[y][x+1] != -1): # Droite
                if boardB[y][x+1] == 2: # Si on a une brique a une case a droite
                    boardB[y][x+1] = 0 # on retire la brique de la matrice
                    sol = QLabel(self) # on la masque en posant un sol dessus.
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x+1)*60, y*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False: # On place un item selon une variable aléatoire et si nous en avons pas deja un
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x+1, y)

                    scoreP += 10 # Quand une brique est cassé nous avons +10 points
                if boardB[y][x+2] == 2 and x != 13: # Si nous avons une brique a 2 case 
                    boardB[y][x+2] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x+2)*60, y*60, 60,60)
                    sol.show()
                    
                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x+2, y)

                    scoreP += 10
                nb.setText(str(scoreP))
            if (boardB[y+1][x] == 2 or boardB[y+1][x] == 0) and (boardB[y+1][x] != -1): # Bas
                if boardB[y+1][x] == 2: 
                    boardB[y+1][x] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x)*60, (y+1)*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x, y+1)

                    scoreP += 10
                if boardB[y+2][x] == 2:
                    boardB[y+2][x] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x)*60, (y+2)*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x, y+2)

                    scoreP += 10
                nb.setText(str(scoreP))
            if (boardB[y-1][x] == 2 or boardB[y-1][x] == 0) and (boardB[y-1][x] != -1): # Haut
                if boardB[y-1][x] == 2:
                    boardB[y-1][x] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x)*60, (y-1)*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x, y-1)

                    scoreP += 10
                if boardB[y-2][x] == 2:
                    boardB[y-2][x] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x)*60, (y-2)*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x, y-2)

                    scoreP += 10
                nb.setText(str(scoreP))
            if (boardB[y][x-1] == 2 or boardB[y][x-1] == 0) and (boardB[y][x-1] != -1): # Gauche
                if boardB[y][x-1] == 2:
                    boardB[y][x-1] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x-1)*60, y*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x-1, y)

                    scoreP += 10
                if boardB[y][x-2] == 2:
                    boardB[y][x-2] = 0
                    sol = QLabel(self)
                    sol.setPixmap(QPixmap('./img/block/sol.png'))
                    sol.setGeometry((x-2)*60, y*60, 60,60)
                    sol.show()

                    if powerSpawned == False and powerState == False:
                        alea = randint(1, 2)

                        if alea == 2:
                            self.spawnPowerUP(x-2, y)

                    scoreP += 10
                nb.setText(str(scoreP))
            self.verifRad1()
            self.verifRad2()
            
            
        elif rad == 1: # Si le rayon d'explosion = 1 (Nous n'avons pas le bonus)
            if boardB[y][x+1] == 2: # Droite
                boardB[y][x+1] = 0
                sol = QLabel(self)
                sol.setPixmap(QPixmap('./img/block/sol.png'))
                sol.setGeometry((x+1)*60, y*60, 60,60)
                sol.show()

                if powerSpawned == False and powerState == False:
                    alea = randint(1, 2)
                    if alea == 2:
                        self.spawnPowerUP(x+1, y)

                scoreP += 10
                nb.setText(str(scoreP))
            if boardB[y+1][x] == 2: # Bas
                boardB[y+1][x] = 0
                sol = QLabel(self)
                sol.setPixmap(QPixmap('./img/block/sol.png'))
                sol.setGeometry(x*60, (y+1)*60, 60,60)
                sol.show()

                if powerSpawned == False and powerState == False:
                    alea = randint(1, 2)
                    if alea == 2:
                        self.spawnPowerUP(x, y+1)

                scoreP += 10
                nb.setText(str(scoreP))
            if boardB[y-1][x] == 2: # Haut
                boardB[y-1][x] = 0
                sol = QLabel(self)
                sol.setPixmap(QPixmap('./img/block/sol.png'))
                sol.setGeometry(x*60, (y-1)*60, 60,60)
                sol.show()

                if powerSpawned == False and powerState == False:
                    alea = randint(1, 2)
                    if alea == 2:
                        self.spawnPowerUP(x, y-1)

                scoreP += 10
                nb.setText(str(scoreP))
            if boardB[y][x-1] == 2: # Gauche
                boardB[y][x-1] = 0
                sol = QLabel(self)
                sol.setPixmap(QPixmap('./img/block/sol.png'))
                sol.setGeometry((x-1)*60, y*60, 60,60)
                sol.show()

                if powerSpawned == False and powerState == False:
                    alea = randint(1, 2)
                    if alea == 2:
                        self.spawnPowerUP(x-1, y)

                scoreP += 10
                nb.setText(str(scoreP))
            self.verifRad1()

        #On initialise le perso et l'IA pour qu'il repasse au dessus des sols
        self.bomb1.setGeometry(posX,posY+20,0,0)
        self.persoDroite.setGeometry(posX,posY,0,0)
        self.persoGauche.setGeometry(posX,posY,0,0)
        self.persoFace.setGeometry(posX,posY,0,0)
        self.persoDos.setGeometry(posX,posY,0,0)
        self.IAGauche.setGeometry(posXIA,posYIA,0,0)
        self.IADroite.setGeometry(posXIA,posYIA,0,0)
        self.IAFace.setGeometry(posXIA,posYIA,0,0)
        self.IADos.setGeometry(posXIA,posYIA,0,0)
        self.initPerso()
        if etatIA == True:
            self.initIA()
        sound_bomb = "./sound/bombe.wav"
        QSound.play(sound_bomb)
        bombe1 = False

    def verifRad1(self): # Fonction qui sert a vérifier si le perso et l'IA se trouve a un rayon de 1 de la bombe et sont vulnérables
        global x, y
        if boardB[y][x+1] == 10 or boardB[y+1][x] == 10 or boardB[y-1][x] == 10 or boardB[y][x-1] == 10 or boardB[y][x] == 10:
            self.mortPerso()
        if boardB[y][x+1] == 20 or boardB[y+1][x] == 20 or boardB[y-1][x] == 20 or boardB[y][x-1] == 20 or boardB[y][x] == 20:
            self.mortIA()
    
    def verifRad2(self): # Fonction qui sert a vérifier si le perso et l'IA se trouve a un rayon de 2 de la bombe et sont vulnérables
        global x, y
        if y == 13:
            if (boardB[y][x+2] == 10 and boardB[y][x+1] != -1) or (boardB[y+1][x] == 10 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 10 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 10 and boardB[y][x-1] != -1) or boardB[y][x] == 10:
                self.mortPerso()
            if (boardB[y][x+2] == 20 and boardB[y][x+1] != -1) or (boardB[y+1][x] == 20 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 20 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 20 and boardB[y][x-1] != -1) or boardB[y][x] == 20:
                self.mortIA()
        elif x == 13:
            if (boardB[y][x+1] == 10 and boardB[y][x+1] != -1) or (boardB[y+2][x] == 10 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 10 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 10 and boardB[y][x-1] != -1) or boardB[y][x] == 10:
                self.mortPerso()
            if (boardB[y][x+1] == 20 and boardB[y][x+1] != -1) or (boardB[y+2][x] == 20 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 20 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 20 and boardB[y][x-1] != -1) or boardB[y][x] == 20:
                self.mortIA()
        if (x >= 1 and x < 13) and (y >= 1 and y < 13):
            if (boardB[y][x+2] == 10 and boardB[y][x+1] != -1) or (boardB[y+2][x] == 10 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 10 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 10 and boardB[y][x-1] != -1) or boardB[y][x] == 10:
                self.mortPerso()
            if (boardB[y][x+2] == 20 and boardB[y][x+1] != -1) or (boardB[y+2][x] == 20 and boardB[y+1][x] != -1) or (boardB[y-2][x] == 20 and boardB[y-1][x] != -1) or (boardB[y][x-2] == 20 and boardB[y][x-1] != -1) or boardB[y][x] == 20:
                self.mortIA()

    def mortIA(self): #Fonction qui gere la mort de l'IA
        global scoreP, etatIA
        etatIA = False # Son état de vie passe à False
        boardB[indYIA][indXIA] = 0 # On la retire de la matrice
        timer.stop() # On stop son timer
        self.IAGauche.hide() # On cache ses textures
        self.IADroite.hide()
        self.IAFace.hide()
        self.IADos.hide()
        scoreP += 1000 # On ajoute 1000 points au compteur de score

        nb.setText(str(scoreP)) # On actualise le compteur de score

    def exploserIA(self): # Fonction qui gere l'explosion de la bombe de l'IA (idem que le perso sans le bonus)
        global bombe2, etatIA
        x = posXB12
        y = posYB12
        if boardB[y][x+1] == 2: # Droite
            boardB[y][x+1] = 0
            sol = QLabel(self)
            sol.setPixmap(QPixmap('./img/block/sol.png'))
            sol.setGeometry((x+1)*60, y*60, 60,60)
            sol.show()
        if boardB[y+1][x] == 2: # Bas
            boardB[y+1][x] = 0
            sol = QLabel(self)
            sol.setPixmap(QPixmap('./img/block/sol.png'))
            sol.setGeometry(x*60, (y+1)*60, 60,60)
            sol.show()
        if boardB[y-1][x] == 2: # Haute
            boardB[y-1][x] = 0
            sol = QLabel(self)
            sol.setPixmap(QPixmap('./img/block/sol.png'))
            sol.setGeometry(x*60, (y-1)*60, 60,60)
            sol.show()
        if boardB[y][x-1] == 2: # Gauche
            boardB[y][x-1] = 0
            sol = QLabel(self)
            sol.setPixmap(QPixmap('./img/block/sol.png'))
            sol.setGeometry((x-1)*60, y*60, 60,60)
            sol.show()
        if boardB[y][x+1] == 10 or boardB[y+1][x] == 10 or boardB[y-1][x] == 10 or boardB[y][x-1] == 10 or boardB[y][x] == 10 :
            self.mortPerso()
        self.IAGauche.setGeometry(posXIA,posYIA,0,0)
        self.IADroite.setGeometry(posXIA,posYIA,0,0)
        self.IAFace.setGeometry(posXIA,posYIA,0,0)
        self.IADos.setGeometry(posXIA,posYIA,0,0)
        self.persoDroite.setGeometry(posX,posY,0,0)
        self.persoGauche.setGeometry(posX,posY,0,0)
        self.persoFace.setGeometry(posX,posY,0,0)
        self.persoDos.setGeometry(posX,posY,0,0)
        self.initPerso()
        if etatIA == True:
            self.initIA()
        bombB[y][x] = 0


        self.bomb2.setGeometry(posXIA,posYIA,0,0)
        sound_bomb = "./sound/bombe.wav"
        QSound.play(sound_bomb)
        bombe2 = False

    def mortPerso(self): # Fontion qui dis au joueur quand son personnage est mort et propose de rejouer ou quiiter le jeu
        reply = QMessageBox.question(self, "Mort", "Vous êtes mort   :'(  Voulez vous rejouez ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes )
        if reply == QMessageBox.Yes:
            self.reset()
        else:
            QApplication.exit()

    def initIA(self): # Initialisation de l'IA (idem que le perso)
        global posXIA,posYIA
        
        self.IAGauche = QLabel(self)
        self.IAGauche.setPixmap(QPixmap('./img/IA/gauche1.png'))
        self.IAGauche.setGeometry(posXIA,posYIA,0,0)

        self.IADroite = QLabel(self)
        self.IADroite.setPixmap(QPixmap('./img/IA/droite1.png'))
        self.IADroite.setGeometry(posXIA,posYIA,0,0)

        self.IAFace = QLabel(self)
        self.IAFace.setPixmap(QPixmap('./img/IA/face1.png'))
        self.IAFace.setGeometry(posXIA,posYIA,60,90)

        self.IADos = QLabel(self)
        self.IADos.setPixmap(QPixmap('./img/IA/dos1.png'))
        self.IADos.setGeometry(posXIA,posYIA,0,0)

        self.IAGauche.show()
        self.IADroite.show()
        self.IAFace.show()
        self.IADos.show()

    def vieIA(self): # Fonction qui permet a l'IA de faire un déplacement ou poser une bombe tout les demi seconde
        global timer
        timer.setSingleShot(False)
        timer.timeout.connect(self.moveIA)
        timer.start(500)

    def moveIA(self): #Fonction qui gere les actions de l'IA aléatoirement
        global indXIA, indYIA, posYIA, posXIA, bombe2, walkIA

        res = self.conditionsIA() #On récuprere un tableau avec toutes les possibilités de déplacemet possibles par l'IA
        randomIA = randint(0,len(res)-1) 
        alea = res[randomIA] #On Prends une action dans le tableau

        walkIA += 1  #Ce compteur permet d'afficher une image différente a chaque déplacement de l'IA
        if walkIA ==3:
            walkIA = 0

        if (alea == 1 ): # L'IA se déplace a droite
            if boardB[indYIA][indXIA +1] == 10: #Si elle rencontre le personnage
                self.mortPerso()
            if boardB[indYIA][indXIA +1] == 0:
                posXIA +=60
                indXIA +=1
                boardB[indYIA][indXIA - 1] = 0
                boardB[indYIA][indXIA] = 20
            if (boardB[indYIA][indXIA+1] == 2 or boardB[indYIA][indXIA+1] == 10): # On pose unne bombe si le perso ou une brique cassable est à côté
                self.placerBombeIA()
            self.IADroite.setGeometry(posXIA,posYIA,60,90)
            self.IADroite.setPixmap(QPixmap(tabDroiteIA[walkIA])) # On affiche l'image en fonction du compteur
            self.IADos.setGeometry(posXIA,posYIA,0,0)
            self.IAGauche.setGeometry(posXIA,posYIA,0,0)
            self.IAFace.setGeometry(posXIA,posYIA,0,0)
            
        if (alea == 2): # se déplace en haut
            if boardB[indYIA-1][indXIA] == 10:
                self.mortPerso()
            if boardB[indYIA-1][indXIA] == 0:
                posYIA -= 60
                indYIA -= 1
                boardB[indYIA+1][indXIA] = 0
                boardB[indYIA][indXIA] = 20
            if (boardB[indYIA-1][indXIA] == 2 or boardB[indYIA-1][indXIA] == 10): # On pose unne bombe si le perso ou une brique cassable est à côté
                self.placerBombeIA()
            self.IADos.setGeometry(posXIA,posYIA,60,90)
            self.IADos.setPixmap(QPixmap(tabDosIA[walkIA])) # On affiche l'image en fonction du compteur
            self.IAGauche.setGeometry(posXIA,posYIA,0,0)
            self.IAFace.setGeometry(posXIA,posYIA,0,0)
            self.IADroite.setGeometry(posXIA,posYIA,0,0)
            
        if (alea == 3): # se déplace à gauche
            if boardB[indYIA][indXIA -1] == 10:
                self.mortPerso()
            if boardB[indYIA][indXIA - 1] == 0:
                posXIA -= 60
                indXIA -= 1
                boardB[indYIA][indXIA+1] = 0
                boardB[indYIA][indXIA] = 20
            if (boardB[indYIA][indXIA-1] == 2 or boardB[indYIA][indXIA-1] == 10): # On pose unne bombe si le perso ou une brique cassable est à côté
                self.placerBombeIA()
            self.IAGauche.setGeometry(posXIA,posYIA,60,90)
            self.IAGauche.setPixmap(QPixmap(tabGaucheIA[walkIA])) # On affiche l'image en fonction du compteur
            self.IAFace.setGeometry(posXIA,posYIA,0,0)
            self.IADroite.setGeometry(posXIA,posYIA,0,0)
            self.IADos.setGeometry(posXIA,posYIA,0,0)
            
        if (alea == 4): # se déplace en bas
            if boardB[indYIA+1][indXIA] == 10:
                self.mortPerso()
            if boardB[indYIA+1][indXIA] == 0:
                posYIA += 60
                indYIA += 1
                boardB[indYIA-1][indXIA] = 0
                boardB[indYIA][indXIA] = 20
            if (boardB[indYIA+1][indXIA] == 2 or boardB[indYIA+1][indXIA] == 10): # On pose unne bombe si le perso ou une brique cassable est à côté
                self.placerBombeIA()
            self.IAFace.setGeometry(posXIA,posYIA,60,90)
            self.IAFace.setPixmap(QPixmap(tabFaceIA[walkIA])) # On affiche l'image en fonction du compteur
            self.IADroite.setGeometry(posXIA,posYIA,0,0)
            self.IADos.setGeometry(posXIA,posYIA,0,0)
            self.IAGauche.setGeometry(posXIA,posYIA,0,0)

        if (boardB[indYIA-1][indXIA] == 2 or boardB[indYIA][indXIA-1] ==2 or boardB[indYIA+1][indXIA] == 2 or boardB[indYIA][indXIA+1] == 2): #pose une bombe
            self.placerBombeIA()

    def placerBombeIA(self): # Fonction qui permet à l'IA de poser la bombe
        global posXIA, posYIA, indXIA, indYIA, posXB12,posYB12, bombe2
        if(not bombe2):
                bombe2 = True
                bombB[indYIA][indXIA] = 12
                posXB12 = indXIA
                posYB12 = indYIA
                self.bomb2 = QLabel(self)
                movieIA = QMovie("./img/bombe/bombeIA.gif")
                self.bomb2.setGeometry(posXIA,posYIA+22,60,60)
                self.bomb2.setMovie(movieIA)
                movieIA.start()
                self.bomb2.show()
                timer1 = QTimer(self)
                timer1.singleShot(2700, self.exploserIA)

    def conditionsIA(self): #Fonction qui permet d'obtenir le tableau des possiblités d'action de l'IA utilisé dans moveIA()
        global posee
        possible = []
        rien = 0
        if(bombe2  == False):
            posee = 0
        if(bombe2 == True): 
            posee += 1
        if posee == 1 : # permet de gérer la premiere action lorsque l'IA pose une bombe
            if (boardB[indYIA][indXIA+1] == 0 and boardB[indYIA][indXIA+2] == 0):
                possible.append(1)
            elif (boardB[indYIA-1][indXIA] ==0 and boardB[indYIA-2][indXIA] ==0):
                possible.append(2)
            elif (boardB[indYIA][indXIA-1] == 0 and boardB[indYIA][indXIA-2] == 0):
                possible.append(3)
            elif (boardB[indYIA+1][indXIA] ==0 and boardB[indYIA+2][indXIA] ==0):
                possible.append(4)
            else:
                if (boardB[indYIA+1][indXIA] ==0):
                    possible.append(4)
                if(boardB[indYIA][indXIA-1] == 0):
                    possible.append(3)
                if (boardB[indYIA-1][indXIA] ==0):
                    possible.append(2)
                if(boardB[indYIA][indXIA+1] == 0):
                    possible.append(1)

        if posee !=1: 
            if (boardB[indYIA][indXIA+1] == 0 or boardB[indYIA-1][indXIA] ==0 or boardB[indYIA][indXIA-1] == 0 or boardB[indYIA+1][indXIA] ==0) and (bombB[indYIA+1][indXIA+1] != 12 and bombB[indYIA-1][indXIA-1] != 12 and bombB[indYIA+1][indXIA-1] != 12 and bombB[indYIA-1][indXIA+1] != 12): # Si on peut faire au moins une des actions 
                if (boardB[indYIA][indXIA+1] == 0 or boardB[indYIA][indXIA+1] == 10) and (bombB[indYIA][indXIA+1] != 12 and bombB[indYIA][indXIA+2] != 12): # Si il n'y a rien ou le perso et qu'une bombe de l'IA n'est pas a une ou 2 cases.
                    possible.append(1)
                    if (boardB[indYIA][indXIA+2] == 2 ): #Augmente les chances d'aller vers une brique cassable
                        possible.append(1)
                        possible.append(1)
                    if (boardB[indYIA][indXIA+2] == 0 ):#Augmente les chances d'avancer lorsque il y a 2 cases vides consécutives
                        possible.append(1)
                else:
                    rien +=1
                
                    
                if (boardB[indYIA-1][indXIA] == 0 or boardB[indYIA-1][indXIA] == 10) and (bombB[indYIA-1][indXIA] != 12 and bombB[indYIA-2][indXIA] != 12 ):# Si il n'y a rien ou le perso et qu'une bombe de l'IA n'est pas a une ou 2 cases.
                    possible.append(2)
                    if (boardB[indYIA-2][indXIA] == 2):#Augmente les chances d'aller vers une brique cassable
                        possible.append(2)
                        possible.append(2)
                    if (boardB[indYIA-2][indXIA] == 0):#Augmente les chances d'avancer lorsque il y a 2 cases vides consécutives
                        possible.append(2)
                else:
                    rien +=1

                if (boardB[indYIA][indXIA-1] ==0 or boardB[indYIA][indXIA-1] == 10) and (bombB[indYIA][indXIA-1] != 12 and bombB[indYIA][indXIA-2] != 12):# Si il n'y a rien ou le perso et qu'une bombe de l'IA n'est pas a une ou 2 cases.
                    possible.append(3)
                    if (boardB[indYIA][indXIA-2] == 2):#Augmente les chances d'aller vers une brique cassable
                        possible.append(3)
                        possible.append(3)
                    if (boardB[indYIA][indXIA-2] == 0):#Augmente les chances d'avancer lorsque il y a 2 cases vides consécutives
                        possible.append(3)
                else:
                    rien +=1

                if (boardB[indYIA+1][indXIA] == 0 or boardB[indYIA+1][indXIA] == 10) and (bombB[indYIA+1][indXIA] != 12 and bombB[indYIA+2][indXIA] != 12):# Si il n'y a rien ou le perso et qu'une bombe de l'IA n'est pas a une ou 2 cases.
                    possible.append(4)
                    if (boardB[indYIA+2][indXIA] == 2):#Augmente les chances d'aller vers une brique cassable
                        possible.append(4)
                        possible.append(4)
                    if (boardB[indYIA+2][indXIA] == 0):#Augmente les chances d'avancer lorsque il y a 2 cases vides consécutives
                        possible.append(4)
                else:
                    rien +=1

                if rien == 4:
                    possible.append(0) # Si l'IA ne peut rien faire on ajoute 0 au tableau donc elle reste au meme endroit
            else:
                possible.append(0) # Si l'IA ne peut rien faire on ajoute 0 au tableau donc elle reste au meme endroit
        return possible 
    
    def win(self):# Fonction qui permet de dire au joueur quand il a gagné et propose de rejouer
        reply = QMessageBox.question(self, "Gagné ! ", "Vous avez gagné :) ! Voulez-vous rejouer ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes )
        if reply == QMessageBox.Yes:
            self.reset()
        else:
            QApplication.exit()