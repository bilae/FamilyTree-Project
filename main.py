"""
Auteurs: Bilal El Aisati et Midas Opsomer
Date: 11/11/2023
Fonction: Sur base d'un fichier contenant des données généalogiques ce programme crée un second
fichier contenant ces mêmes données sous un autre format et ouvre une fenêtre dans laquelle on
peut afficher soit des listes ordonnées de toutes les personnes soit un arbre généalogique.
"""

# Import des modules nécessaires
import json
from tkinter import *
from turtle import RawTurtle


def lire_fichier(chemin_du_fichier):

    """Extrait et retourne le contenu du fichier json "chemin_du_fichier"."""

    with open(chemin_du_fichier, 'r', encoding='utf-8') as f_in:
        return json.load(f_in)


def construire_mapping(personnes):

    """Retourne un dictionnaire avec pour clés les noms des personnes et pour
    valeurs les noms de leurs enfants sur base de la liste de dictionnaires
    "personnes"."""

    mapping = {}

    for personne in personnes: # S'occupe du cas général
        nom = personne["nom"]
        enfants = personne.get("enfants", [])
        mapping[nom] = enfants

    for personne in personnes:  # S'occupe du cas où une personne n'est que dans des dictionnaires sous forme d'enfant
        for personne2 in personne["enfants"]:
            if personne2 not in mapping.keys():
                mapping[personne2] = []

    return mapping


def trouver_generation(personne, mapping, cache_generation):
    """Calcul la génération de la personne par rapport à ses parents, grands-parents etc"""
    max_ancetre_generation = 0 # Initialisation
    for parent, enfants in mapping.items():
        if personne in enfants:
            ancetre_generation = trouver_generation(parent, mapping, cache_generation)
            max_ancetre_generation = max(max_ancetre_generation, ancetre_generation)
            cache_generation[personne] = max_ancetre_generation + 1
            return cache_generation[personne]
    for parent, enfants in mapping.items():    
        if personne not in enfants:
            for dico in resultats:
                if dico["nom"] == personne:
                    if dico["generations"] == trouve_prof_max(resultats):
                        cache_generation[personne] = 1
                        return cache_generation[personne]
                    else:
                        for personne1 in mapping.keys():
                            if mapping[personne] != []:
                                if mapping[personne][0] in mapping[personne1] and personne != personne1:
                                    cache_generation[personne] = trouver_generation(personne1, mapping, cache_generation)
                                    return cache_generation[personne]


def compter_descendants_et_profondeur(nom, mapping, cache_compte={}, cache_profondeur={}, cache_generation={}):
    """Fonction qui permet de calculer les descendants ainsi que la pronfondeur des différents éléments du fichier lûs grâce à la fonction lire_fichier"""
    total_descendants = 0 # Initalisation
    generations = 0  # Initialise la profondeur à zéro, puisqu'elle sera calculée correctement

    if nom in mapping:
        for enfant in mapping[nom]:
            result = compter_descendants_et_profondeur(enfant, mapping, cache_compte, cache_profondeur)
            total_descendants += 1 + result["total_descendants"]
            generations = max(generations, 1 + result["generations"])

    cache_compte[nom] = total_descendants
    cache_profondeur[nom] = generations

    return {"nom": nom, "total_descendants": total_descendants, "generations": generations}



def trier_par_selection(personnes, nb_desc_ou_gen):

    """Trie personnes par nombre de descendants quand nb_desc_ou_gen vaut True sinon trie par nombre de générations
    (et trie par ordre alphabétique les personnes dont générations ou total_descendants est pareil)."""

    if nb_desc_ou_gen:  # Trie par descendants
        for i in range(len(personnes)):
            x = personnes[i]
            y = i
            for j in range(i+1, len(personnes)):
                if x["total_descendants"] < personnes[j]["total_descendants"] or (x["total_descendants"] == personnes[j]["total_descendants"] and x["nom"] > personnes[j]["nom"]):
                    x = personnes[j]
                    y = j
            personnes[i], personnes[y] = x, personnes[i]

    else:  # Trie par générations qui suivent les personnes
        for i in range(len(personnes)):
            x = personnes[i]
            y = i
            for j in range(i+1, len(personnes)):
                if x["generations"] < personnes[j]["generations"] or (x["generations"] == personnes[j]["generations"] and x["nom"] > personnes[j]["nom"]):
                    x = personnes[j]
                    y = j
            personnes[i], personnes[y] = x, personnes[i]


def spawn_buttons():

    """Initialise la fenêtre et crée les boutons par lesquels on choisit ce qu'on affiche."""

    global frame

    # Initialise la fenêtre en créant un nouveau canvas
    frame = Canvas(window, height=800, width=600)
    frame.pack()

    # Création des boutons
    button = Button(window, text="Tri par descendants", command=liste_desc, font=("Arial", 15))
    button.place(x=42.5, y=750)  # largeur=190

    button = Button(window, text="Tri par génération", command=liste_gen, font=("Arial", 15))
    button.place(x=275, y=750)  # largeur=172

    button = Button(window, text="Arbre", command=arbre, font=("Arial", 15))
    button.place(x=489.5, y=750)  # largeur=68


def liste_desc():

    """Imprime la liste tri_par_desc établit dans le programme général sous forme de phrases."""

    # Initialisation de la fenêtre
    frame.destroy()
    spawn_buttons()

    # Tri selon les paramètres voulus
    trier_par_selection(resultats, True)

    # Impression de la liste
    for dico in tri_par_desc:
        label1 = Label(frame, text=(str(dico["nom"]) + " a " + str(dico["total_descendants"]) + " descendants sur " + str(dico["generations"]) + " générations."))
        label1.pack(side=TOP)


def liste_gen():

    """Imprime la liste tri_par_gen établit dans le programme général sous forme de phrases."""

    # Initialisation de la fenêtre
    frame.destroy()
    spawn_buttons()

    # Tri selon les paramètres voulus
    trier_par_selection(resultats, False)

    # Impression de la liste
    for dico in tri_par_gen:
        label2 = Label(frame, text=(str(dico["nom"]) + " a " + str(dico["total_descendants"]) + " descendants sur " + str(dico["generations"]) + " générations."))
        label2.pack(side=TOP)


def arbre():

    """Affiche l'arbre généalogique des personnes dont les relations sont données par mapping."""

    # Initialisation de la fenêtre
    frame.destroy()
    spawn_buttons()

    dico_coord = {}

    # Initialisation de Turtle
    turtle = RawTurtle(frame)
    turtle.hideturtle()
    turtle.speed(1000)
    turtle.up()

    for i in range(trouve_prof_max(tri_par_desc)+2):  # Imprime les noms aux bons endroits et retient leurs coordonnées
        coordx = 20
        coordy = i * 75
        for dico in tri_par_desc:
            if dico["generation"] == i:
                Label(frame, text=str(dico["nom"])).place(x=coordx, y=coordy)
                dico_coord[dico["nom"]] = coordx, coordy
                coordx += 100

    for nom in mapping.keys():  # Trace les lignes entre les personnes
        for nom_enfant in mapping[nom]:
            turtle.setpos(dico_coord[nom][0]-300+25, -dico_coord[nom][1]+400-25)
            turtle.down()
            turtle.goto(dico_coord[nom_enfant][0]-300+25, -dico_coord[nom_enfant][1]+400)
            turtle.up()


def trouve_prof_max(tri_par_desc):

    """Trouve prof_max dans tri_par_desc. Ceci est utilisé dans la fonction qui construit l'arbre généalogique."""

    prof_max = 0
    for p in tri_par_desc:
        if p["generation"] > prof_max:
            prof_max = p["generation"]
    return prof_max


# Charge le fichier JSON
data = lire_fichier("chemin_du_fichier.json")

# Construit le mapping
mapping = construire_mapping(data)

# Liste de dictionnaires en format voulu
resultats = []

for nom in mapping.keys():
    resultats.append(compter_descendants_et_profondeur(nom, mapping))

# Sauvegarde les résultats dans un fichier JSON
with open("resultats.json", "w") as fichier_sortie:
    json.dump(resultats, fichier_sortie, indent=4)

# Crée la fenêtre de l'application
window = Tk()
window.geometry('600x800+500+50')

# Crée les listes de dictionnaires qui seront triées ultérieurement
tri_par_desc = resultats
tri_par_gen = resultats

# Crée les boutons qui appellent les différentes fonctions
spawn_buttons()

window.mainloop()
