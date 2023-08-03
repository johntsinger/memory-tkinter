
def mini(attribute):

    """
    Modifie column et line de la méthode create_cartes(self, column, line)
    de la classe Apli
    Passe les paramètres du decorateur au décorateur
    :param attribute: int, attribut self.nombre_carte de la classe Apli
    :return: func: le décorateur
    """

    def decorator(fonc_exe):

        """
        Décorateur
        :param fonc_exe: func, la fonction a éxécuter
        :return: func, la fontion modifiée
        """

        def fonc_modif(self, column, line):

            """
            Fonction que l'on va renvoyer.
            Calcule column et line en fonction du nombre passé en paramètre
            du décorateur.
            :param self: la classe Apli
            :param column: le nombre de carte par colone
            :param line: le nombre de carte par ligne
            :return: la méthode de classe exécuté avec les nouveaux attributs
            """

            # Calcul les multiples du nombre passé en paramètre
            # et les ajoute a une liste
            li = []
            number = getattr(self, attribute)
            for i in range(4, 11):
                if number % i == 0:
                    li.append(i)

            # Pour chaque multiple du resultat recherche un nombre entre 4 et 10
            # qui multiplié par le multiple donne le nombre passé en paramètre et
            # ajoute a une liste sous forme de tuple le multiple et le nombre
            li1 = []
            for i in range(4, 11):
                for elt in li:
                    if elt * i == number:
                        li1.append((i, elt))

            # Soustrait les deux nombres de chaque tuples et ajoute a une liste un
            # tuple contenant le résultat de la soustraction et le tuple précédant
            li2 = []
            for elt in li1:
                soustrac = elt[1] - elt[0]
                li2.append((soustrac, (elt[0], elt[1])))

            # Créé une liste de transition contenant les resultats de la soustraction
            li3 = []
            for elt in li2:
                li3.append(elt[0])

            # recharche le résultat de la soustractiob le plus proche de 0
            mi = min(li3, key=abs)
            for elt in li2:
                if elt[0] == mi:
                    column, line = elt[1]

            return fonc_exe(self, column, line)
        return fonc_modif
    return decorator


"""
# Test
@mini(number)
def a(x,y):
    print(x, y)
    
number = int(input())
a(0,0)
"""
