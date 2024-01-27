from tkinter import *
import random
import time

'''
bug(s) à noter: -on peut faire demi tour sur soi-même
                -la pomme peut apparaitre sur le corps du serpent
'''


"""
on déclare quelques variables
"""
pommeX = 1
pommeY = 1 #les coordonnées de base de la pomme

largeur = 600
hauteur = 600 #les dimensions du canvas

score = 0

niveau = 0

en_pause = False

en_partie = False

temps = 3

bouton_remouvement = False

game_over = True

score_final = False

#coordonees et vitesse de départ
x0, y0 = 100, 100  #les coordonees de la tete ( le coin haut, gauche)
dx = 20 #vitesse horizontale
dy = 0 #vitesse verticale

"""
on crée la fenetre tkinter
"""
fenetre = Tk()
fenetre.title("Snake")
canvas = Canvas(fenetre, width=largeur, height= hauteur, background="light cyan")
canvas.grid(column = 1) #on crée le canvas



while pommeX % 20 != 0:#on fait en sorte que la pomme apparraisse 'dans la grille' (1 px = 20 unités de longueur)
    pommeX = random.randrange(20,largeur-20) # et qu'elle n'apparraisse ni dans un murs, ni au dela des limites
while pommeY % 20 != 0:
    pommeY = random.randrange(20,hauteur-20)

head = canvas.create_rectangle(x0+1, y0+1, x0+19, y0+19, width=2, fill="green")#on cree la tete du serpent sur le canvas

serpent = [head]  #on cree la liste des elements du corps, on agrandi cette liste a chaque fois que la tete touche une pomme

pomme = canvas.create_oval(pommeX+1, pommeY+1, pommeX+19, pommeY+19, fill="red") #on cree la 1ere pomme sur le canvas

"""
on crée les fonctions qui changent la direction
"""
def droite(event):
    global dx, dy
#dans toute le fonctions on défini les variables en global, pour qu'elles soit réutilisables hors de ces foncions

    if dy != 0: #on fait ce test pour ne pas pouvoir faire demi tour sur soi-même
        dx = 20
        dy = 0

def gauche(event):
    global dx, dy

    if dy != 0:
        dx = -20
        dy = 0

def haut(event):
    global dx, dy

    if dx != 0:
        dx = 0
        dy = -20

def bas(event):
    global dx, dy

    if dx != 0:
        dx = 0
        dy = 20


"""
on créer une fonction qui permet de mettre en pause la partie en appuyant sur la touche "espace"
"""
def pause(event):
    global en_pause, pause_label, dx, dy, en_partie

    if en_partie == True:
        if dx != 0 or dy != 0:
            if en_pause == False:
                en_pause = True
                pause_label = Label(fenetre, text=" ~Pause~ ", width=10, font=('Haettenschweiler', 50), background="light cyan")
                pause_label.grid(column=1, row=0)

            elif en_pause == True:
                en_pause = False
                Label.destroy(pause_label)
                mouvement()



"""
on défini les touches qui changes la direction du serpent et une touche qui met en pause(qui lancent les fonctions)
"""
canvas.bind_all('<Right>', droite)
canvas.bind_all('<Left>', gauche)
canvas.bind_all('<Up>', haut)
canvas.bind_all('<Down>', bas)
canvas.bind_all('<space>', pause)



"""
on défini la fonction qui va créer des murs
"""
def murs():
    global murN, murW, murE, murS, pomme, serpent, largeur, hauteur

    murN = canvas.create_rectangle(0, 0, largeur, 20, width=2, fill="black") #création du mur Nord
    murW = canvas.create_rectangle(0, 0, 20, hauteur, width=2, fill="black") #création du mur Ouest
    murE = canvas.create_rectangle(largeur-20, 0, largeur+1, hauteur, width=2, fill="black") #création du mur Est
    murS = canvas.create_rectangle(0, hauteur-20, largeur+1, hauteur+1, width=2, fill="black") #création du mur Sud



"""
on ajoute un decompte avant le début de la partie
"""
def decompte():
    global temps, attente_print, attente, bouton_remouvement, bouton_mouvement, game_over

    #on va ici detruire le bouton "commencer"
    if bouton_remouvement == False: #et on le remplace par un bouton "recommencer", si il n'existe pas deja
        bouton_remouvement = Button(fenetre, text="Recommencer",  width=13, height=3, font=('Haettenschweiler', 20), background= "light grey" ,command=recommencer, state=DISABLED)
        bouton_remouvement.grid(column=0, row=0) #avec "state=DISABLED", on fait en sorte que le bouton ne soit pas cliquable tant que la partie est en cours
        Button.destroy(bouton_mouvement)
        bouton_mouvement = False

    game_over = False

    attente = StringVar()

    if temps != 0:

        attente.set("{}".format(temps))

        attente_print = Label(fenetre, textvariable=attente, width=5, font=('Haettenschweiler', 50), background="light cyan")
        attente_print.grid(column=1, row=0)

        temps -= 1
        canvas.after(1000, onsupprimeleslabelsicioupas)
    else:

        attente.set("{}".format("GO !"))
        temps -= 1

        attente_print = Label(fenetre, textvariable=attente, width=5, font=('Haettenschweiler', 50), background="light cyan")
        attente_print.grid(column=1, row=0)

        canvas.after(500, onsupprimeleslabelsicioupas)

    return


"""
on supprime les labels (les chiffres) du decompte (au fur et a mesure qu'ils s'affichent)
"""
def onsupprimeleslabelsicioupas():
    global attente_print, attente, temps

    Label.destroy(attente_print)

    if temps != -1:
        decompte()

    else:
        temps = 3
        mouvement()


"""
on crée la fonction pricipale qui va déplacer le serpent et tester les collisions
"""
def mouvement():
    global x0, y0, dx, dy, murN, murW, murE, murS, serpent, game_over, bouton_remouvement, niveau, temps, en_pause, en_partie

    if en_partie == False:
        en_partie = True


    x0 += dx #on change la position horizontale en y ajoutant la vitesse horizontale
    y0 += dy #on change la position verticale en y ajoutant la vitesse verticale

    canvas.coords(serpent[-1], x0+1, y0+1, x0+19, y0+19) #on deplace le dernier objet de la liste serpent devant (le bout de la queue devient la tete) sur le canvas

    serpent.insert(0, serpent.pop(-1)) #on deplace le dernier objet de la liste serpent (le bout de la queue devient la tete) dans la liste : liste[-1] -> liste [0] // liste[n] -> liste[n+1]


    #on teste les collisions de la tête du serpent
    if len(canvas.find_overlapping(canvas.coords(serpent[0])[0],canvas.coords(serpent[0])[1],canvas.coords(serpent[0])[2],canvas.coords(serpent[0])[3]))>1:
        #et on verifie que cette collision ne soit pas avec un pomme
        if len(canvas.find_overlapping(canvas.coords(pomme)[0],canvas.coords(pomme)[1],canvas.coords(pomme)[2],canvas.coords(pomme)[3]))<=1:
            game_over = True
            en_partie = False
            Game_Over() #on lance la fonction "Game_Over"

    #tant que la partie n'est pas fini ou n'est pas en pause
    if game_over == False and en_pause == False:
        #on recommence la fonction mouvement en boucle
        canvas.after(100-niveau,mouvement) #toute les '100-niveau' milliseconde: faire la fonction 'mouvement' (plus 'niveau' est grand plus la vitesse augmente)

    return

"""
on crée la fonction qui va faire apparaitre (et disparaitre) les pommes
"""
def food():
    global x0, y0, pommeX, pommeY, pomme, score, niveau, hauteur, largeur

    #si il y a un autre objet au dessus de la pomme
    if len(canvas.find_overlapping(canvas.coords(pomme)[0],canvas.coords(pomme)[1],canvas.coords(pomme)[2],canvas.coords(pomme)[3]))>1:
        #on la supprime
        canvas.delete(pomme)

        #et on en crée une nouvelle
        pommeX = random.randrange(20,largeur-20)
        while pommeX % 20 != 0:
            pommeX = random.randrange(20,largeur-20)

        pommeY = random.randrange(20,hauteur-20)
        while pommeY % 20 != 0:
            pommeY = random.randrange(20,hauteur-20)

        pomme = canvas.create_oval(pommeX+1, pommeY+1, pommeX+19, pommeY+19, fill="red")

        #on ajoute aussi 1 au score
        score += 1
        if niveau < 56: #et on augmente la vitesse et donc la difficulté à chaque fois qu'on mange une pomme
            niveau +=1

        current_score.set("Votre score est {}".format(score))

        #enfin, on aggrandie le serpent
        serpent.append(score+1)
        serpent[score] = canvas.create_rectangle(x0+1, y0+1, x0+19, y0+19, width=2, fill="green") # la pour ces coordonnes je il faudra sans doute les changer

    canvas.after(100-niveau,food)#toute les '100-niveau' milliseconde: faire la fonction 'food'
    return


"""
on crée une fonction de fin de partie
"""
def Game_Over():
    global score_final

    Button.config(bouton_remouvement, state=ACTIVE)#le bouton recommencer devient actif

    #on affiche le score final du joueur
    if score >= 10:
        score_final = Label(fenetre, font=('Haettenschweiler', 45), text="Vous avez obtenu {} points".format(score), background="light cyan")
    elif score > 1:
        score_final = Label(fenetre, font=('Haettenschweiler', 50), text="Vous avez obtenu {} points".format(score), background="light cyan")
    else:
        score_final = Label(fenetre, font=('Haettenschweiler', 50), text="Vous avez obtenu {} point".format(score), background="light cyan")
    score_final.grid(column=1, row=0)

    return

"""
on definie ici la fonction pour recommencer un partie
(cette fonction va aussi être utiliser pour commencer (et recommencer) une partie avec la touche "entrer")
"""
def recommencer():
    global serpent, game_over, x0, y0, score, dx, dy, mouvement, score_final, niveau, en_partie

    #on supprime tous les éléments de la liste 'serpent'
    for loop in range (len(serpent)):
        canvas.delete(serpent[loop])

    #on redéfinie les variables
    x0, y0 = 100, 100
    dx, dy = 20, 0
    niveau = 0
    score = 0

    #on recrée un nouveau serpent
    head = canvas.create_rectangle(x0+1, y0+1, x0+19, y0+19, width=2, fill="green")
    serpent = [head]

    if bouton_remouvement != False:
        Button.config(bouton_remouvement, state=DISABLED)#on desactive a nouveau le bouton recommencer

    current_score.set("Votre score est {}".format(score))

    game_over = False

    if score_final != False:
        Label.destroy(score_final)#on enlève le score de l'ancienne partie de la fenetre

    decompte()
    return

"""
on fait en sorte de pouvoir lancer (et relancer) la partie avec la touche "entrer"
"""
def enter(event):
    global game_over, recommencer

    if game_over == True:
        recommencer()


canvas.bind_all('<Return>', enter)#on défini que la touche entrer va lancer la fonction "enter(event)"

"""
on crée un bouton qui va lancer la fonction mouvement, et ainsi commencer le jeu
"""
#on doit crée le bouton qui lance la fonction mouvement après avoir crée la fonction elle même
bouton_mouvement = Button(fenetre, text="Commencer", width=13, height=3, font=('Haettenschweiler', 20), command=decompte, background= "light grey")
bouton_mouvement.grid(column=0, row=0)

"""
on affiche le score
"""
current_score = StringVar()
current_score.set("Votre score est {}".format(score))

affichage_score = Label(fenetre, textvariable=current_score, width=18, font=('Haettenschweiler', 20))
affichage_score.grid(column=2, row=0)


murs()#on lance la fonction qui crée les murs

food()#on lance la fonction qui fait apparaitre les pommes

fenetre.mainloop()#on ouvre la fenetre tkinter