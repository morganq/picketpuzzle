import pygame

SOUNDFILES = {
    'step0':'assets/Step0.wav',
    'step1':'assets/Step1.wav',
    'step2':'assets/Step2.wav',
    'occupy':'assets/Occupy2.wav',
    'factory':'assets/Factory.wav',
    'blip':'assets/Blip.wav'
}
SOUNDS = {}

def init():
    for s,fn in SOUNDFILES.items():
        SOUNDS[s] = pygame.mixer.Sound(fn)

def play(name):
    SOUNDS[name].play()