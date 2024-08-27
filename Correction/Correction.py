import cv2
import numpy as np
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import array
import xlwt

# Création d'un nouveau classeur Excel
workbook = xlwt.Workbook()
# Ajout d'une feuille nommée "Notes QCM"
sheet = workbook.add_sheet("Notes QCM")
# Définition du style pour les en-têtes
style = xlwt.easyxf('font: bold 1')
# Écriture des en-têtes de colonnes
sheet.write(0, 0, 'Les Etudiants', style)
sheet.write(0, 1, 'Notes', style)

# Fonction pour obtenir la lettre correspondant à un numéro
def alph(i):
    switcher = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
    }
    return switcher.get(i, 'A')

# Fonction pour obtenir le numéro correspondant à une lettre
def tonum(letter):
    switcher = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
    }
    return switcher.get(letter, 0)

# Liste des réponses correctes pour le QCM
arrrep = ['a', 'd', 'b', 'a', 'a']

# Création d'un tableau pour stocker les réponses détectées
arr = array.array('i', [])

# Chargement de l'image contenant le QCM à corriger
image = cv2.imread('C:\\Users\\HP\\ECOMMERCES\\correcteur QCM\\Correction QCM\\coupage.jpg')

# Conversion de l'image en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Application d'un flou médian pour réduire le bruit
blur = cv2.medianBlur(gray, 5)
# Application d'un filtre pour accentuer les contours
sharpen_kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

# Binarisation de l'image
thresh = cv2.threshold(sharpen, 160, 250, cv2.THRESH_BINARY_INV)[1]
# Définition de la structure élémentaire pour la morphologie
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# Application de la fermeture morphologique pour fermer les petites régions blanches
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Détection des contours dans l'image traitée
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 1800  # Aire minimale des contours pour être considérés
max_area = 1900  # Aire maximale des contours pour être considérés
image_number = 0  # Compteur pour les images traitées
answers = 0  # Compteur pour les réponses détectées
i = 0
image1 = image

# Traitement des contours détectés
for c in cnts:
    area = cv2.contourArea(c)
    if min_area < area < max_area:
        x, y, w, h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+h]
        answers += 1

for c in reversed(cnts):
    area = cv2.contourArea(c)
    if min_area < area < max_area:
        x, y, w, h = cv2.boundingRect(c)
        ROI = image[y:y + h, x:x + h]
        # Dessin d'un rectangle autour de la réponse détectée
        cv2.rectangle(image1, (x, y), (x + w, y + h), (255, 255, 255), 2)
        image_number += 1
        resized = imutils.resize(ROI, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        # Application d'un flou gaussien
        blurred = cv2.GaussianBlur(resized, (5, 5), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]

        # Détection des contours dans l'image floutée
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cl = ColorLabeler()
        # Boucle sur les contours détectés
        for c in cnts:
            # Calcul du centre du contour
            M = cv2.moments(c)
            # Détection de la couleur du contour
            color = cl.label(lab, c)
            # Étiquetage de la couleur sur l'image
            text = "{}".format(color)

            if text == 'white':
                arr.append(0)
            else:
                # Vérification si la réponse détectée est correcte
                if tonum(arrrep[i]) == image_number % 4:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
                else:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (12, 36, 255), 3)
                i += 1
                arr.append(1)

# Enregistrement de l'image corrigée
cv2.imwrite('Correction/coupage.jpg', image)

# Création d'une liste pour les réponses corrigées
arrc = []

# Traitement des réponses pour les comparer aux réponses correctes
j = 0
for i in range(i, answers, 4):
    itt = 0
    for i in range(j, answers):
        if arr[i] == 1:
            char = alph(itt)
            arrc.append(char)
            itt += 1
            j += 1
            if itt == 4:
                break
        else:
            itt += 1
            j += 1
            if itt == 4:
                break

# Calcul de la note
note = 0
for i in range(len(arrc)):
    print("La réponse de la question sélectionnée par l'étudiant", i + 1, "est :", arrc[i])
print("\r")

for i in range(len(arrc)):
    if arrc[i] == arrrep[i]:
        note += 4

print("La note de l'étudiant est :", note)
# Écriture des résultats dans le fichier Excel
sheet.write(1, 0, 'Etudiant 2')
sheet.write(1, 1, note)
workbook.save("sample.xls")
