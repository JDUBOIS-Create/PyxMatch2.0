import cv2
import numpy as np
import pyautogui
import subprocess
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Fonction pour détecter le lobby dans une capture d'écran
def detect_lobby(image, lobby_image_path):
    template = cv2.imread(lobby_image_path, 0)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Ajuste ce seuil selon la précision
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        return True
    return False

# Fonction pour capturer l'écran du jeu
def capture_game_screen(screen_region):
    screenshot = pyautogui.screenshot(region=screen_region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

# Fonction pour afficher la publicité en utilisant VLC
def play_ad(ad_video_path):
    vlc_process = subprocess.Popen(["vlc", "--fullscreen", ad_video_path])
    return vlc_process

# Fonction pour arrêter la publicité
def stop_ad(vlc_process):
    vlc_process.terminate()

# Fonction pour exécuter la détection en temps réel
def process_real_time(lobby_image_path, ad_video_path, screen_region):
    ad_playing = False
    vlc_process = None

    while True:
        frame = capture_game_screen(screen_region)

        if detect_lobby(frame, lobby_image_path):
            if not ad_playing:
                print("Lobby détecté, lancement de la publicité...")
                vlc_process = play_ad(ad_video_path)
                ad_playing = True
        else:
            if ad_playing:
                print("Lobby non détecté, arrêt de la publicité...")
                stop_ad(vlc_process)
                ad_playing = False

        time.sleep(1)

# Fonction pour lancer le script de détection via le bouton
def start_script():
    try:
        lobby_image_path = "chemin/vers/lobby_template.png"  # Remplace par l'image modèle du lobby
        ad_video_path = "chemin/vers/publicite.mp4"  # Remplace par le fichier vidéo de la publicité
        screen_region = (0, 0, 1920, 1080)  # Ajuste selon ton écran

        # Lancer la détection dans un thread séparé pour ne pas bloquer l'interface
        threading.Thread(target=process_real_time, args=(lobby_image_path, ad_video_path, screen_region)).start()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Création de l'interface utilisateur avec Tkinter
def create_gui():
    window = tk.Tk()
    window.title("PyxMatch - Lancement de la publicité")
    window.geometry("400x200")
    window.configure(bg="#1c1c1c")

    # Fonction pour styliser le bouton
    btn_font = ("Arial", 16, "bold")
    btn_color = "#4CAF50"
    btn_fg = "#ffffff"

    # Bouton pour lancer le script
    start_button = tk.Button(window, text="PyxMatch", command=start_script, font=btn_font, bg=btn_color, fg=btn_fg, padx=20, pady=10)
    start_button.pack(pady=50)

    window.mainloop()

# Lancer l'interface graphique
if __name__ == "__main__":
    create_gui()

