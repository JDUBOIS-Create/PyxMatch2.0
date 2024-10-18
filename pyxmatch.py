import cv2
import numpy as np
import pyautogui
import subprocess
import time
import threading
import tkinter as tk
from tkinter import messagebox

def detect_lobby(image, lobby_image_paths):
    """
    Fonction pour détecter le lobby en comparant la capture d'écran avec une ou plusieurs images du lobby.
    """
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    for lobby_image_path in lobby_image_paths:
        print(f"Vérification de l'image du lobby: {lobby_image_path}")
        template = cv2.imread(lobby_image_path, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            print("Match trouvé pour le lobby!")
            return True
    return False

def capture_game_screen(screen_region):
    """
    Capture une portion de l'écran spécifiée pour vérifier la présence du lobby.
    """
    screenshot = pyautogui.screenshot(region=screen_region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    print("Capture d'écran effectuée")
    return frame

def play_ad(ad_video_path):
    """
    Lance la vidéo publicitaire en plein écran via VLC.
    """
    print("Lancement de la publicité...")
    vlc_process = subprocess.Popen(["vlc", "--fullscreen", ad_video_path])
    return vlc_process

def stop_ad(vlc_process):
    """
    Arrête la vidéo publicitaire.
    """
    print("Arrêt de la publicité...")
    vlc_process.terminate()

def process_real_time(lobby_image_paths, ad_video_path, screen_region):
    """
    Boucle principale qui vérifie en temps réel si le lobby est présent et gère la diffusion de la publicité.
    """
    ad_playing = False
    vlc_process = None

    while True:
        frame = capture_game_screen(screen_region)

        if detect_lobby(frame, lobby_image_paths):
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

def start_script():
    """
    Fonction appelée par le bouton pour démarrer la détection et la publicité.
    """
    try:
        print("Script lancé, démarrage de la détection du lobby...")

        lobby_image_paths = [
            "chemin/vers/lobby_template1.png",
            "chemin/vers/lobby_template2.png",
            "chemin/vers/lobby_template3.png"
        ]
        ad_video_path = "chemin/vers/publicite.mp4"
        screen_region = (0, 0, 1920, 1080)

        threading.Thread(target=process_real_time, args=(lobby_image_paths, ad_video_path, screen_region)).start()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def create_gui():
    """
    Crée une interface graphique avec un bouton pour lancer le script.
    """
    window = tk.Tk()
    window.title("PyxMatch - Lancement de la publicité")
    window.geometry("400x200")
    window.configure(bg="#1c1c1c")

    btn_font = ("Arial", 16, "bold")
    btn_color = "#4CAF50"
    btn_fg = "#ffffff"

    start_button = tk.Button(window, text="PyxMatch", command=start_script, font=btn_font, bg=btn_color, fg=btn_fg, padx=20, pady=10)
    start_button.pack(pady=50)

    window.mainloop()

def main():
    """
    Point d'entrée du script. Organise les appels de fonctions.
    """
    create_gui()

if __name__ == "__main__":
    main()
