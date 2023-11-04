import json

def lire_fichier(chemin_du_fichier):
    """Extrait et retourne le contenu du fichier json "chemin_du_fichier"."""
    with open(chemin_du_fichier, 'r', encoding='utf-8') as f_in:
        return json.load(f_in)

def construire_mapping(personnes):
    """Retourne un dictionnaire avec pour clés les noms des personnes et pour
    valeurs les noms de leurs enfants sur base de la liste de dictionnaires
    "personnes"."""
    mapping = {}
    for i in range(len(personnes)):
        mapping[personnes[i]["nom"]] = personnes[i]["enfants"]
    return mapping



mapping = construire_mapping(lire_fichier())
