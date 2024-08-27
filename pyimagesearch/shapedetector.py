# Importer les packages nécessaires
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # Initialiser le nom de la forme et approximer le contour
        shape = "non identifié"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # Si la forme a 3 sommets, c'est un triangle
        if len(approx) == 3:
            shape = "triangle"

        # Si la forme a 4 sommets, c'est soit un carré soit un rectangle
        elif len(approx) == 4:
            # Calculer la boîte englobante du contour et utiliser cette boîte
            # pour calculer le ratio d'aspect
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # Un carré aura un ratio d'aspect proche de un, sinon, la forme est un rectangle
            shape = "carré" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # Si la forme a 5 sommets, c'est un pentagone
        elif len(approx) == 5:
            shape = "pentagone"

        # Sinon, nous supposons que la forme est un cercle
        else:
            shape = "cercle"

        # Retourner le nom de la forme
        return shape
