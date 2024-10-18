import cv2
import numpy as np
import pyautogui

# Fonction pour détecter le lobby dans une image
def detect_lobby(image, lobby_image_path):
    # Charger l'image modèle du lobby (fournir le chemin vers ton modèle)
    template = cv2.imread(lobby_image_path, 0)  # Image du lobby en niveaux de gris
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Comparer l'image actuelle avec le modèle de lobby
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Ajuste le seuil pour la précision souhaitée
    loc = np.where(res >= threshold)
    
    # Si le modèle est trouvé dans l'image actuelle, retourne True
    if len(loc[0]) > 0:
        return True
    return False

# Fonction pour superposer la publicité à l'image
def overlay_ad(image, ad_image_path):
    # Charger l'image de la publicité (fournir le chemin vers la publicité)
    ad_image = cv2.imread(ad_image_path, -1)  # Charger avec transparence si c'est un PNG
    
    # Redimensionner la publicité si nécessaire pour qu'elle s'adapte à l'image
    ad_resized = cv2.resize(ad_image, (image.shape[1], image.shape[0])) 
    
    # Superposition de la publicité (tu peux ajuster l'opacité si nécessaire)
    overlay_image = cv2.addWeighted(image, 1, ad_resized, 0.5, 0)
    
    return overlay_image

# Fonction pour obtenir la liste des écrans disponibles
def get_screens():
    return pyautogui.getAllMonitors()

# Fonction pour afficher l'image avec publicité sur l'écran choisi
def display_on_screen(image, screen_number):
    screens = get_screens()
    
    # Vérifier si l'écran choisi existe
    if screen_number < len(screens):
        screen = screens[screen_number]
        cv2.imshow("Ad Display", image)
        
        # Positionner la fenêtre sur l'écran choisi
        cv2.moveWindow("Ad Display", screen['left'], screen['top'])
        cv2.waitKey(0)  # Attendre que l'utilisateur ferme la fenêtre
    else:
        print("Écran non disponible. Vérifie le numéro d'écran.")

# Fonction principale pour traiter la rediffusion vidéo
def process_video(video_path, lobby_image_path, ad_image_path, screen_number):
    # Ouvrir la vidéo (fournir le chemin de la vidéo de rediffusion)
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()  # Lire une image de la vidéo
        if not ret:
            break  # Si on atteint la fin de la vidéo, sortir de la boucle
        
        # Vérifier si le lobby est détecté
        if detect_lobby(frame, lobby_image_path):
            print("Lobby détecté, affichage de la publicité...")
            
            # Superposer la publicité sur l'image
            frame_with_ad = overlay_ad(frame, ad_image_path)
            
            # Afficher sur l'écran choisi
            display_on_screen(frame_with_ad, screen_number)
        else:
            print("Lobby non détecté, passage à l'image suivante...")
    
    cap.release()  # Fermer la vidéo après traitement

# --- PARTIE À MODIFIER SELON TES FICHIERS ---

# Chemin vers la vidéo de rediffusion
video_path = "chemin/vers/la/video_rediffusion.mp4"  # Remplace avec le chemin réel de la vidéo

# Chemin vers l'image du lobby
lobby_image_path = "chemin/vers/lobby_template.png"  # Remplace avec l'image modèle du lobby

# Chemin vers l'image de la publicité
ad_image_path = "chemin/vers/publicite.png"  # Remplace avec l'image de la publicité

# Numéro de l'écran (0 pour le premier écran, 1 pour le second, etc.)
screen_number = 1  # Choisis l'écran sur lequel afficher la publicité

# --- FIN DES MODIFICATIONS ---

# Lancer le traitement vidéo
process_video(video_path, lobby_image_path, ad_image_path, screen_number)
