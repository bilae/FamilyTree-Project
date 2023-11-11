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
    for personne in personnes:
        nom = personne["nom"]
        enfants = personne.get("enfants", [])
        mapping[nom] = enfants
    return mapping

# Charge le fichier JSON
data = lire_fichier("chemin_du_fichier.json")

# Construit le mapping
mapping = construire_mapping(data)

def compter_descendants_et_profondeur(nom, mapping, cache_compte={}, cache_profondeur={}, generation_courante=1):

    total_descendants = 0
    profondeur = generation_courante

    for enfant in mapping.get(nom, []):
        result = compter_descendants_et_profondeur(enfant, mapping, cache_compte, cache_profondeur, generation_courante + 1)
        total_descendants += 1 + result["total_descendants"]
        if result["generations"] > profondeur:
            profondeur = result["generations"]

    cache_compte[nom] = total_descendants
    cache_profondeur[nom] = profondeur

    return {"nom": nom, "total_descendants": total_descendants, "generations": profondeur}

# Liste de résultats
resultats = []

for nom in mapping.keys():
    resultats.append(compter_descendants_et_profondeur(nom, mapping))

# Sauvegarde les résultats dans un fichier JSON
with open("resultats.json", "w") as fichier_sortie:
    json.dump(resultats, fichier_sortie, indent=4)


def trier_par_selection(personnes, nb_desc_ou_gen):
    """Trie personnes par nombre de descendants quand nb_desc_ou_gen vaut
    True sinon trie par nombre de générations (et trie par ordre alphabétique
    les personnes dont générations ou total_descendants est pareil)."""
    if nb_desc_ou_gen:
        for i in range(len(personnes)):
            x = personnes[i]
            y = i
            for j in range(i+1, len(personnes)):
                if x["total_descendants"] < personnes[j]["total_descendants"] or (x["total_descendants"] == personnes[j]["total_descendants"] and x["name"] > personnes[j]["name"]):
                    x = personnes[j]
                    y = j
            personnes[i], personnes[y] = x, personnes[i]
    else:
        for i in range(len(personnes)):
            x = personnes[i]
            y = i
            for j in range(i+1, len(personnes)):
                if x["générations"] < personnes[j]["générations"] or (x["générations"] == personnes[j]["générations"] and x["name"] > personnes[j]["name"]):
                    x = personnes[j]
                    y = j
            personnes[i], personnes[y] = x, personnes[i]

