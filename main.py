import os
import pygame
from tkinter import Tk, Button, Label, Scale, filedialog, StringVar
from pydub import AudioSegment
import random
import time

class LecteurAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Audio")

        self.current_track = StringVar()
        self.current_track.set("Aucune piste sélectionnée")

        self.volume = 50
        self.is_playing = False
        self.is_looping = False
        self.audio = None
        self.current_audio_path = None
        self.tracks = []
        self.current_track_index = 0

        self.initialize_ui()

    def initialize_ui(self):
        Label(self.root, textvariable=self.current_track).pack(pady=10)

        Button(self.root, text="Choisir une piste", command=self.choose_track).pack(pady=10)
        Button(self.root, text="Lancer la lecture", command=self.play).pack(pady=5)
        Button(self.root, text="Mettre en pause", command=self.pause).pack(pady=5)
        Button(self.root, text="Arrêter la lecture", command=self.stop).pack(pady=5)
        Button(self.root, text="Augmenter le volume", command=self.increase_volume).pack(pady=5)
        Button(self.root, text="Diminuer le volume", command=self.decrease_volume).pack(pady=5)
        Button(self.root, text="Lire en boucle", command=self.toggle_loop).pack(pady=5)
        Button(self.root, text="Piste suivante", command=self.next_track).pack(pady=5)
        Button(self.root, text="Sélection aléatoire", command=self.random_track).pack(pady=5)

        self.progress_scale = Scale(self.root, from_=0, to=100, orient="horizontal", length=200,
                                    label="Progression de la lecture", command=self.set_progress)
        self.progress_scale.pack(pady=10)

        
        self.root.after(100, self.update_progress)

    def choose_track(self):
        file_path = filedialog.askopenfilename(title="Choisir une piste audio", filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.current_track.set(os.path.basename(file_path))
            self.current_audio_path = file_path
            self.audio = AudioSegment.from_file(file_path)
            self.tracks = [file for file in os.listdir(os.path.dirname(file_path)) if file.endswith(('.mp3', '.wav'))]
            self.current_track_index = self.tracks.index(os.path.basename(file_path))

    def play(self):
        if not self.is_playing and self.current_audio_path is not None:
            self.is_playing = True
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(self.current_audio_path)
            pygame.mixer.music.play()

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def increase_volume(self):
        if self.is_playing:
            self.volume = min(100, self.volume + 10)
            pygame.mixer.music.set_volume(self.volume / 100)

    def decrease_volume(self):
        if self.is_playing:
            self.volume = max(0, self.volume - 10)
            pygame.mixer.music.set_volume(self.volume / 100)

    def toggle_loop(self):
        if self.is_playing:
            self.is_looping = not self.is_looping
            if self.is_looping:
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.set_endevent(0)

    def set_progress(self, value):
        if self.is_playing:
            progress = int(value) * len(self.audio) / 100
            pygame.mixer.music.set_pos(progress / 1000) 

    def update_progress(self):
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos()
            total_time = len(self.audio) 
            progress_percent = (current_time / total_time) * 100
            self.progress_scale.set(progress_percent)

        
        self.root.after(100, self.update_progress)

    def next_track(self):
        if self.is_playing:
            self.stop()
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
            next_track_path = os.path.join(os.path.dirname(self.current_audio_path), self.tracks[self.current_track_index])
            self.current_audio_path = next_track_path
            self.current_track.set(os.path.basename(next_track_path))
            self.audio = AudioSegment.from_file(next_track_path)
            self.play()

    def random_track(self):
        if self.is_playing:
            self.stop()
            random_track_path = os.path.join(os.path.dirname(self.current_audio_path), random.choice(self.tracks))
            self.current_audio_path = random_track_path
            self.current_track.set(os.path.basename(random_track_path))
            self.audio = AudioSegment.from_file(random_track_path)
            self.play()

if __name__ == "__main__":
    root = Tk()
    lecteur_audio = LecteurAudio(root)
    root.mainloop()