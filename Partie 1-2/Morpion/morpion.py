#!/usr/bin/env python3

"""Un jeu de morpion"""


# Les différents types de joueurs sont représentés par des modules.
# Les modules joueur_humain et joueur_ordi doivent être réaliser.
# Le module joueur_ordi_malin est fourni.
# Le module joueur_humain demande simplement à l'utilisateur de jouer.
# Le module joueur_ordi joue automatiquement. Sa stratégie n'est pas spécifiée.
import joueur_humain
import joueur_ordi
import joueur_ordi_malin
import sys

class bcolors:
  RED = '\u001b[31m'
  BLUE = '\u001b[34m'
  RESET = '\u001b[0m'

def recupere_chaine_a_afficher(symbole):
    """Renvoie la chaîne de caractère à afficher pour le symbole donné.

    Pour le symbole "x", le caractère unicode "MULTIPLICATION X", affiché
    en rouge doit être utilisé.
    Pour le symbole "x", le caractère unicode "WHITE CIRCLE", affiché
    en bleu doit être utilisé.

    précondition : symbole est soit "x" soit "o"
    """
    if symbole == 'x':
      return bcolors.RED + '\u2715' + bcolors.RESET
    else:
      return bcolors.BLUE + '\u25CB' + bcolors.RESET

  
def affiche_plateau(cases):
    """Affiche le plateau représenté par le tuples cases à 9 éléments.

    L'affichage se fait sur la sortie standard uniquement en utilisant
    des appels à la fonction print.

    précondition : chacune des cases contient soit
      - la chaîne de caractères "x" (case occupée par le joueur 1)
      - la chaîne de caractères "o" (case occupée par le joueur 2)
      - la chaîne de caractères "i" avec i entier correspondant au
        numéro de la case (case libre)
    précondition : cases est un tuple de 9 éléments
    """
    form = "{0:1}{1:1}{2:1}"
    tab = [['|','|',''],['|','|',''],['|','|','']]
    for i in range(9):
        if cases[i] in 'ox':
            tab[i//3][i%3] = recupere_chaine_a_afficher(cases[i]) + tab[i//3][i%3]
        else:
            tab[i//3][i%3] = ' ' + tab[i//3][i%3]
    for val in tab:
        print(form.format(*val))


def joue_coup(joueur, joueur_num, cases, symbole):
    """Joue un coup.

    Cette fonction effectue les opérations suivantes tout en affichant
    ce qu'il se passe sur la sortie standard :
      - affiche le plateau représenté par cases
      - utilise le module joueur pour savoir quel coup doit être joué
      - met à jour le plateau de jeu avec ce coup
      - affiche le plateau et le numéro du joueur gagnant si c'est gagné
        puis quitte le programme
      - renvoie le nouveau plateau

    précondition : joueur est un module avec une fonction
                   joue_coup(cases, symbole) qui renvoie le
                   numéro d'une case précédemment inoccupée.
    précondition : joueur_num est soit l'entier 1 soit l'entier 2
    précondition : cases est un tuple de 9 éléments
    précondition : symbole est soit "x" soit "o"
    """

    # Etape 1
    affiche_plateau(cases)

    # Etape 2
    numero = joueur.joue_coup(cases, symbole)

    # Etape 3
    cases[numero] = symbole

    # Etape 4
    
    (partie_finie, symbole_gagnant) = victoire(cases)
    if partie_finie:
      affiche_plateau(cases)
      if symbole_gagnant == symbole:
        print(f'Le joueur {joueur_num} a gagne !')
      else:
        print('Le joueur ' + (2+joueur_num)%2+1 + ' a gagne !')
      sys.exit()
    
    # Etape 5
    return cases
      

def victoire(cases):
    """
    Fonction qui va regarder si il y a un vainqueur a partir d'un tableau de morpion.
    Si c'est le cas la fonction retourne le symbole du gagnant.
    """
    for i in range(3):
      if cases[3*i] == cases[1+3*i] == cases[2+3*i]:
        return True, cases[3*i]
      if cases[i] == cases[3+i] == cases[6+i]:
        return True, cases[i]
    if cases[0] == cases[4] == cases[8]:
      return True, cases[0]
    if cases[2] == cases[4] == cases[6]:
      return True, cases[2]
    return False, ''

def aide_joueur():
  """ Programme qui va afficher des explications pour un joueur humain."""
  print("Voici les numéros pour un plateau de morpion : ")
  form = "{0:1}{1:1}{2:1}"
  tab = [['1|','2|','3'],['4|','5|','6'],['7|','8|','9']]
  for val in tab:
    print(form.format(*val))
  print()

def joue_partie():
    """Joue une partie complète de morpion"""

    # Initialisation des deux joueurs en demandant à l'utilisateur
    # Parenthèses nécessaires pour "spliter un string literal"
    message_choix_joueur = ("Veuillez choisir le type du joueur {} en tapant\n"
                            "  0 pour humain\n"
                            "  1 pour un ordinateur\n"
                            "  2 pour un ordinateur très malin\n"
                            "  entrez votre choix : ")

    print(message_choix_joueur.format(1), end="")
    type1 = int(input())
    print(message_choix_joueur.format(2), end="")
    type2 = int(input())
    joueur1 = joueur_humain if type1 == 0 else (joueur_ordi
                                                if type1 == 1
                                                else joueur_ordi_malin)
    joueur2 = joueur_humain if type2 == 0 else (joueur_ordi
                                                if type2 == 1
                                                else joueur_ordi_malin)
    print()

    # Initialisation et affichage du plateau vide
    # Une case vide est représentée par son numéro,
    # utilisé par le joueur humain pour indiquer
    # quelle case il joue.
    cases = ["0", "1", "2",
             "3", "4", "5",
             "6", "7", "8"]
    
    if (joueur1 or joueur2) == joueur_humain:
      aide_joueur() # Affichage du plateau pour jouer pour les humains
      
    
    # Joue 9 coups au maximum
    joue_coup(joueur1, 1, cases, "x")
    joue_coup(joueur2, 2, cases, "o")
    joue_coup(joueur1, 1, cases, "x")
    joue_coup(joueur2, 2, cases, "o")
    joue_coup(joueur1, 1, cases, "x")
    joue_coup(joueur2, 2, cases, "o")
    joue_coup(joueur1, 1, cases, "x")
    joue_coup(joueur2, 2, cases, "o")
    joue_coup(joueur1, 1, cases, "x")

    # Si on arrive là, il y a égalité
    print("Match nul !")

    affiche_plateau(cases)

if __name__ == "__main__":
    joue_partie()