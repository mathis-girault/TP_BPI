#!/usr/bin/env python3

"""Listes simplement chaînées avec partages de suffixes."""

import traceur

class Cellule:
    """Une cellule d'une liste simplement chaînée.

    Contient une référence vers la valeur, une référence vers la cellule
    suivante et une référence vers un compteur comptabilisant combien
    de cellules pointent dessus.
    """
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant
        self.utilisation = 1

    def __str__(self):
        return str(self.valeur) + " , " + str(self.utilisation)

class ListeSimplementChainee:
    """Liste simplement chainée avec partage de cellule.

    Des listes simplement chainées différentes peuvent partager
    des cellules communes.
    """
    def __init__(self, mot):
        """Construit une liste simplement chaînée à partir d'un mot.

        La liste simplement chaînée construite ne partage aucune cellule
        pour le moment.
        """
        premiere_cellule = None
        self.taille = 0
        for lettre in reversed(mot):
            premiere_cellule = Cellule(lettre, premiere_cellule)
            self.taille += 1
        self.tete = premiere_cellule

    def __str__(self):
        """Renvoie la chaîne de cractères "val1 --> val2 --> val3 ..." """
        return "-->".join(str(cell.valeur) for cell in recupere_cellules(self))


def recupere_cellules(liste_chainee):
    """Générateur renvoyant un itérateur sur toutes les cellules."""
    if liste_chainee.tete is not None:
        cellule_courante = liste_chainee.tete
        yield cellule_courante
        while cellule_courante.suivant is not None:
            cellule_courante = cellule_courante.suivant
            yield cellule_courante

def ajoute_suffixe(liste_chainee, autre):
    """Ajoute la liste chaînée `autre` à la fin de `liste_chainee`.

    Toutes les cellules de autre sont partagées.
    Si la fin de `liste_chainee` était déjà partagée avec quelqu'un, alors
    il faut dédoubler toute la partie partagée avant l'ajout pour ne pas changer
    les autres listes chaînées utilisant cette fin.
    """
    if autre.taille == 0:
        return

    iter_cellules_liste = recupere_cellules(liste_chainee)
    iter_cellules_autres = recupere_cellules(autre)
    cellule_courante_liste = None

    for cellule_suivante_liste in iter_cellules_liste:
        if cellule_suivante_liste.utilisation == 1:
            cellule_courante_liste = cellule_suivante_liste
        else:
            cellule_suivante_liste.utilisation -= 1
            if cellule_courante_liste is None:
                liste_chainee.tete = Cellule(cellule_suivante_liste.valeur, None)
                cellule_courante_liste = liste_chainee.tete
            else:
                cellule_courante_liste.suivant = Cellule(cellule_suivante_liste.valeur, None)
                cellule_courante_liste = cellule_courante_liste.suivant
            for cellule_duplique in iter_cellules_liste:
                cellule_courante_liste.suivant = Cellule(cellule_duplique.valeur, None)
                cellule_courante_liste = cellule_courante_liste.suivant

    flag = False
    for cellule_courante_autre in iter_cellules_autres:
        if not flag: # Premiere cellule:
            flag = True
            cellule_courante_autre.utilisation += 1
        if cellule_courante_liste is None:
            liste_chainee.tete = cellule_courante_autre
            cellule_courante_liste = cellule_courante_autre
        else:
            cellule_courante_liste.suivant = cellule_courante_autre
            cellule_courante_liste = cellule_courante_autre

    liste_chainee.taille = liste_chainee.taille + autre.taille


def teste_listes():
    """On teste toutes les operations dans différentes configurations."""

    print("on crée une list, c'est à dire un tableau dynamique, de 4 listes simplement chainées")
    listes_chainees = [ListeSimplementChainee(mot) for mot in
                       ("SE", "PAS", "DE", "DEVIS")]
    print(*listes_chainees, sep="\n")

    # On temporise
    _ = input("tapez sur une touche pour continuer")
    print()

    print("on ajoute", listes_chainees[0], "apres", listes_chainees[1])
    ajoute_suffixe(listes_chainees[1], listes_chainees[0])
    print(*listes_chainees, sep="\n")

    # On temporise
    _ = input("tapez sur une touche pour continuer")
    print()

    print("on ajoute une liste vide après", listes_chainees[1])
    ajoute_suffixe(listes_chainees[1], ListeSimplementChainee(""))
    print(*listes_chainees, sep="\n")

    # On temporise
    _ = input("tapez sur une touche pour continuer")
    print()

    print("on ajoute", listes_chainees[1], "apres", listes_chainees[2], "et",
          listes_chainees[0], "apres", listes_chainees[3])
    ajoute_suffixe(listes_chainees[2], listes_chainees[1])
    ajoute_suffixe(listes_chainees[3], listes_chainees[0])
    print(*listes_chainees, sep="\n")
    traceur.display_vars(traceur.Variable('listes', listes_chainees), deeply=False,
                         visualize=False, image_name="4_listes")

    # On temporise
    _ = input("tapez sur une touche pour continuer")
    print()

    liste_chainee_nt = ListeSimplementChainee("NT")
    print("on ajoute 'NT' apres 'PASSE'")

    ajoute_suffixe(listes_chainees[1], liste_chainee_nt)
    print(*listes_chainees, liste_chainee_nt, sep="\n")

    # On temporise
    _ = input("tapez sur une touche pour continuer")
    print()

    print("on ajoute 'SE' apres elle-meme")
    ajoute_suffixe(listes_chainees[0], listes_chainees[0])
    print(*listes_chainees, sep="\n")
    traceur.display_vars(traceur.Variable('listes', listes_chainees),
                         traceur.Variable('liste_chainee_nt', liste_chainee_nt),
                         deeply=False,
                         visualize=False, image_name="5_listes")

if __name__ == "__main__":
    teste_listes()
