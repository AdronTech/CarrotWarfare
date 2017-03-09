import os
from os.path import isdir, splitext

import pygame
from pygame import mixer
import random

class Sound:
    def __init__(self):

        self.basepath_sound = 'assets/sound'
        self.basepath_music = 'assets/music'
        self.sounds = {}
        self.music = {}

        self.gen_structure(self.sounds, self.basepath_sound, (".wav", ".ogg"))
        self.gen_structure(self.music, self.basepath_music, ".ogg")

        mixer.init()

        self.load_sounds()

        # for entry in SOUND_RESOURCE:
        #     for version in entry:
        #         version["sound"] = Sound(join('assets/sprites', version["name"] + ".wav"))

    def gen_structure(self, output: dict, dir: str, ends, base=None):

        if not base:
            base = dir

        for file in os.listdir(dir):
            if file.endswith(ends):
                name = splitext(file)[0]
                l = name.split('_')
                f_name = "_".join(l[:-1])
                count = l[-1]

                shortpath = dir.replace(base, "")
                shortpath = shortpath[1:]
                if shortpath is not "":
                    shortpath = shortpath + "/"

                shortname = ""

                if count.isdigit():
                    shortname = shortpath + f_name

                    if shortname not in output:
                        output[shortname] = []

                else:
                    shortname = shortpath + name

                    if shortname not in output:
                        output[shortname] = []

                output[shortname].append(dir + "/" + file)

            elif isdir(dir + "/" + file):
                self.gen_structure(output, dir + "/" + file, ends, base)

    def load_sounds(self):
        for entry in self.sounds:
            paths = self.sounds[entry]

            self.sounds[entry] = []

            for p in paths:
                # self.sounds[entry].append(p + ": Loaded")
                s = mixer.Sound(p)
                self.sounds[entry].append(s)

    def play(self, name):
        if name in self.sounds:
            random.choice(self.sounds[name]).play()

if __name__ == "__main__":
    import time

    pygame.mixer.init()

    s = Sound()
    print(s.sounds)

    for i in range(100):
        s.play("hit")

        # time.sleep(1)
