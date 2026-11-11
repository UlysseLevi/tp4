#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

from TAD.piles_listes_python import Pile
from TAD.files_listes_python import File
#from TAD.piles_listes_simplement_chainees import Pile
#from TAD.files_listes_doublement_chainees import File
from notation_polonaise_inverse import *

OPERATEURS = ['+', '-', '*', '/'] 

def parcours_DFS(cartons, cible) : 

    nb_noeuds = 0
    meilleure_expression = []
    meilleur_ecart = None 

    p = Pile()
    p.empiler(([], cartons))

    while not p.est_vide() :
        expression, restants = p.depiler()
        nb_noeuds+=1
        valide, valeur = eval_NPI_liste(expression)
        if not valide :
            continue
        if valeur is not None :
            ecart = abs(valeur - cible)
            if meilleur_ecart is None or ecart < meilleur_ecart :
                meilleur_ecart = ecart
                meilleure_expression = expression
                print(expression, "=", valeur)
                if ecart == 0 :
                    return meilleure_expression, nb_noeuds
                
        for i in range(len(restants)) :
            nouveaux_restants = restants[:i] + restants[i+1:]
            p.empiler((expression + [restants[i]], nouveaux_restants))    

        nb_ops = sum(1 for x in expression if x in OPERATEURS)
        en_attente = len(expression) - 2 * nb_ops
        if en_attente >= 2 :
            for op in OPERATEURS :
                p.empiler((expression + [op], restants))
    return meilleure_expression, nb_noeuds

def parcours_BFS(cartons, cible) : 
    nb_noeuds = 0
    meilleure_expression = []
    meilleur_ecart = None 

    f = File()
    f.enfiler(([], cartons))

    while not f.est_vide() :
        expression, restants = f.defiler()
        nb_noeuds+=1
        valide, valeur = eval_NPI_liste(expression)
        if not valide :
            continue
        if valeur is not None :
            ecart = abs(valeur - cible)
            if meilleur_ecart is None or ecart < meilleur_ecart :
                meilleur_ecart = ecart
                meilleure_expression = expression
                print(expression, "=", valeur)
                if ecart == 0 :
                    return meilleure_expression, nb_noeuds
                
        for i in range(len(restants)) :
            nouveaux_restants = restants[:i] + restants[i+1:]
            f.enfiler((expression + [restants[i]], nouveaux_restants))    

        nb_ops = sum(1 for x in expression if x in OPERATEURS)
        en_attente = len(expression) - 2 * nb_ops
        if en_attente >= 2 :
            for op in OPERATEURS :
                f.enfiler((expression + [op], restants))
    return meilleure_expression, nb_noeuds

def parcours_DFS_recursif(cartons, cible) :
    meilleure_expression = []
    nb_noeuds = 0
    meilleur_ecart = None 

    def parcours_DFSR_aux(choisis, restants) :
        nonlocal meilleure_expression
        nonlocal nb_noeuds
        nonlocal meilleur_ecart 
        nonlocal cible
        nb_noeuds +=1

        valide, valeur = eval_NPI_liste(choisis)
        if not valide :
            return False 

        if valeur is not None :
            ecart = abs(valeur - cible)
            if meilleur_ecart is None or ecart < meilleur_ecart :
                meilleur_ecart = ecart
                meilleure_expression = choisis
                print(choisis, "=", valeur)
                if ecart == 0 :
                    return True

        for i in range(len(restants)) :
            if parcours_DFSR_aux(choisis + [restants[i]], restants[:i] + restants[i+1:]) :
                return True
        nb_ops = sum(1 for x in choisis if x in OPERATEURS)
        if len(choisis) - 2 * nb_ops >= 2 :
            for op in OPERATEURS :
                if parcours_DFSR_aux(choisis + [op], restants) :
                    return True
        return False

    parcours_DFSR_aux([], cartons)
    return meilleure_expression, nb_noeuds


if __name__ == "__main__":
    parcours_DFS([3,5, 7, 9, 25, 50], 859)
    parcours_BFS([3,5, 7, 9, 25, 50], 859)
    parcours_DFS_recursif([3,5, 7, 9, 25, 50], 859)
 
