# Importer les packages nécessaires
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        # Initialiser le dictionnaire des couleurs, contenant le nom de la couleur
        # comme clé et le tuple RGB comme valeur
        colors = OrderedDict({
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "white":(255, 255, 255),
            "black":(0, 0, 0)})

        # Allouer de la mémoire pour l'image, puis initialiser
        # la liste des noms de couleurs
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        # Boucle sur le dictionnaire des couleurs
        for (i, (name, rgb)) in enumerate(colors.items()):
            # Mettre à jour le tableau  et la liste des noms de couleurs
            self.lab[i] = rgb
            self.colorNames.append(name)

        # Convertir le tableau  de l'espace de couleur RGB
       
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # Construire un masque pour le contour, puis calculer la
        # valeur moyenne  pour la région masquée
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # Initialiser la distance minimale trouvée jusqu'à présent
        minDist = (np.inf, None)

        # Boucle sur les valeurs de couleur L*a*b* connues
        for (i, row) in enumerate(self.lab):
            # Calculer la distance entre la valeur de couleur L*a*b* actuelle
            # et la moyenne de l'image
            d = dist.euclidean(row[0], mean)

            # Si la distance est plus petite que la distance actuelle,
            # mettre à jour la variable de suivi
            if d < minDist[0]:
                minDist = (d, i)

        # Retourner le nom de la couleur avec la distance la plus petite
        return self.colorNames[minDist[1]]
