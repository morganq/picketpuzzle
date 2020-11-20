import pygame
import save
from resources import resource_path

MUSIC_ENDEVENT = pygame.USEREVENT+1

SOUNDFILES = {
    'step0':'assets/Step0.wav',
    'step1':'assets/Step1.wav',
    'step2':'assets/Step2.wav',
    'occupy':'assets/Occupy2.wav',
    'factory':'assets/Factory.wav',
    'blip':'assets/Blip.wav',
    'soldier':'assets/Soldier.wav',
    'cannot':'assets/Cannot.wav',
    'cell':'assets/Cell.wav',
    'defeat':'assets/Defeat.wav',
    'tankfire':'assets/TankFire.wav',
    'tankdrive':'assets/TankDrive.wav'
}
SOUNDS = {}

def init():
    for s,fn in SOUNDFILES.items():
        SOUNDS[s] = pygame.mixer.Sound(resource_path(fn))
    pygame.mixer.music.set_endevent(MUSIC_ENDEVENT)

def play(name):
    vol = save.SAVE_OBJ.get_setting("sound_volume") / 12
    if vol > 0:
        SOUNDS[name].play().set_volume(vol)


MUSIC = {
    'overworld':resource_path('assets/menusong.ogg'),
    'game':resource_path('assets/ingamesong.ogg'),
    'victory':resource_path('assets/newvictory.ogg'),
}
MUSIC_TIMES = {
    'overworld':0,
    'game':0,
    'victory':0
}
MUSIC_VOLUME_CO = {
    'overworld':1.5,
    'game':2.25,
    'victory':1.25
}
LAST_TRACK = None
CURRENT_TRACK = None

def play_music(name, loops=0, force = False):
    global CURRENT_TRACK, MUSIC_TIMES, LAST_TRACK
    if name == CURRENT_TRACK and not force:
        return
    CURRENT_TRACK = name

    if name == "victory":
        MUSIC_TIMES['victory'] = 0

    time_played = pygame.mixer.music.get_pos()
    if LAST_TRACK:
        MUSIC_TIMES[LAST_TRACK] = pygame.mixer.music.get_pos()

    pygame.mixer.music.load(MUSIC[name])
    pygame.mixer.music.play(loops=0)
    try:
        pygame.mixer.music.set_pos(max(0,MUSIC_TIMES[name] / 1000.0))
    except Exception as e:
        print(e)
    update_volume()
    LAST_TRACK = name

def update_volume():
    pygame.mixer.music.set_volume(0.1 * save.SAVE_OBJ.get_setting("music_volume") / 10 * MUSIC_VOLUME_CO[CURRENT_TRACK])

def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def end_of_music():
    if CURRENT_TRACK != "victory":
        MUSIC_TIMES[CURRENT_TRACK] = 0
        play_music(CURRENT_TRACK, force=True)