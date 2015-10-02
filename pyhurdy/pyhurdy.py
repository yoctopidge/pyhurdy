#! /usr/bin/env python
# TODO: ratios are wrong
# Tuning is high. we're going the wrong way on the dict'
import time, collections, os
import numpy, pygame.mixer, pygame.sndarray
from pygame.locals import *
import pygame
from scikits.samplerate import resample



class PyHurdy():
    def __init__(self, tuning):
        # Sounds
        self._tenor = "pyhurdy/pyhsounds//drones/tenor.wav"
        self._bass = "pyhurdy/pyhsounds//drones/bass.wav"
        self._high_melody = "pyhurdy/pyhsounds//melody/high.wav"
        self._melody = "pyhurdy/pyhsounds//melody/high.wav"
        self.pygame=pygame
        self.tenorstate=False
        self.tuning = tuning
        self.bassstate=False
        self.melodystate=False
        self.noteplaying=self.tuning
        try:
            screen = None
            dispdrivers = ['directfb', 'svgalib', 'fbcon']
            gotdriver = False
            for driver in dispdrivers:
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    self.pygame.display.init()
                except self.pygame.error:
                    continue
                gotdriver = True
                break
                if not gotdriver:
                    raise Exception('Kaboom!')
            size = (self.pygame.display.Info().current_w, self.pygame.display.Info().current_h)
            print "Framebuffer size: %d x %d" % (size[0], size[1])
            screen = self.pygame.display.set_mode(size, self.pygame.FULLSCREEN)
            # Clear the screen to start
            screen.fill((0, 0, 0))
        except:
            print('No framebuffer found. Assume x11')
            os.putenv('SDL_VIDEODRIVER', 'x11')
            self.pygame.init()
            size = (1024, 768)
            print "X server size: %d x %d" % (size[0], size[1])
            screen = self.pygame.display.set_mode(size)
        self.pygame.mixer.init(44100,-16,2,4096)
        # Render the screen
        self.pygame.display.update()
        self.init_sounds(tuning="g0")
        self.set_scale()
        self.play()

    def set_scale(self):
        self.note_dict=collections.OrderedDict()
        self.notes=[] 
        twelfth=1.059463094
#        notes=['c','d','e','f','g','a','b']
        notes=['b', 'a', 'g', 'f', 'e', 'd', 'c']
        prior=1
        for base in range(0,4):
            for note in notes:
                self.note_dict[note+str(base)]={'ratio': prior, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''}
                prior=prior*1.059
                if note is not "b" and note is not "g":
                    self.note_dict[note+"sharp"+str(base)]={'ratio': prior, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''}
                    prior=prior*1.059
        for note in self.note_dict:
            self.notes.append(note)
#        self.toprow = ['F1','F2','F3','F4','F5','F6','F7','F8','F9']
#        self.bottomrow = ['1','2','3','4','5','6','7','8','9','10', '-','=','BACKSPACE']
        self.toprow = ['F9', 'F8', 'F7', 'F6', 'F5', 'F4', 'F3', 'F2', 'F1']
        self.bottomrow = ['BACKSPACE', '=', '-', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']

        self.num_top_keys = len(self.toprow)
        self.num_bottom_keys = len(self.bottomrow)
        self.num_keys=self.num_top_keys+self.num_bottom_keys
        self.top_keys=[]
        self.bottom_keys=[]
        self.keys={}
#        d = collections.deque(self.notes)
#        self.notes=list(d.rotate(len(self.notes)-(self.notes.index(self.tuning)+1)))
        self.notes=self.notes[self.notes.index(self.tuning):self.num_keys+1]
        x=0
        y=0
        for note in self.notes:
            if "sharp" in note:
                self.top_keys.append(note)
                self.note_dict[note]['row']='top' 
                self.note_dict[note]['key']=self.toprow[x] 
                x=x+1
            else:
                self.bottom_keys.append(note)
                self.note_dict[note]['row']='bottom' 
                self.note_dict[note]['key']=self.bottomrow[y] 
                y=y+1
            self.set_note(note, self.melody)

        for x in self.top_keys:
            self.keys[self.note_dict[x]['key']]=x

        for x in self.bottom_keys:
            self.keys[self.note_dict[x]['key']]=x

        print "TOP : " + str(self.top_keys)
        print "BOTTOM : " + str(self.bottom_keys)

    def init_sounds(self, tuning="g0"):
        self.tenor = self.pygame.mixer.Sound(self._tenor)
        self.bass = self.pygame.mixer.Sound(self._bass)
        self._melody = self.pygame.mixer.Sound(self._high_melody)
        self.tenor.set_volume(.15)
        self.bass.set_volume(.15)
        self.drone_sounds= [self.tenor, self._melody, self.bass]
        # load the sound into an array
        self.melody = self.pygame.sndarray.array(self._melody)

    def set_note(self, note, hstring):
        octave = note[-1:]
        self.note_dict[note]['octave']=octave 
        pure_note = note.strip(octave)
        ratio = self.note_dict[note]['ratio']
        globals()[note] = resample(hstring, ratio, "sinc_best").astype(hstring.dtype)
        globals()[note+"_note"] = self.pygame.sndarray.make_sound(globals()[note])
        globals()[note+"_note"].set_volume(.15)
        self.note_dict[note]['snd_arry']=note+"_note" 

    def play(self):
        while True:
            for event in self.pygame.event.get():

                #Changes the moving variables only when the key is being pressed
                if event.type == KEYDOWN:
                    if event.key == K_F10:
                        if self.tenorstate is True:
                            self.tenor.fadeout(1)
                            self.tenorstate = False
                        else:
                            self.tenor.play(loops=-1)
                            self.tenorstate = True
                    if event.key == K_F11:
                        if self.bassstate is True:
                            self.bass.fadeout(1)
                            self.bassstate = False
                        else:
                            self.bass.play(loops=-1)
                            self.bassstate = True
                    if event.key == K_F12:
                        if self.melodystate is True:
                            globals()[self.tuning+"_note"].fadeout(1)
                            globals()[self.tuning+"_note"].set_volume(.1)
                            self.melodystate = False
                        else:
                            globals()[self.tuning+"_note"].play(loops=-1)
                            self.melodystate = True
                    if self.melodystate == True and self.pygame.key.name(event.key).upper() in self.keys.keys():
                        if self.note_dict[self.noteplaying]['ratio'] < self.note_dict[self.keys[self.pygame.key.name(event.key).upper()]]['ratio']:
                            globals()[self.noteplaying+"_note"].fadeout(1)
                            self.noteplaying = self.keys[self.pygame.key.name(event.key).upper()]
                            globals()[self.noteplaying+"_note"].play(loops=-1)
            #                elif noteplaying == TUNING:
            #                        globals()[TUNING+"_note"].fadeout(1)
            #                        noteplaying = NOTES[self.keys.index(pygame.key.name(event.key))]
            #                        globals()[noteplaying.replace('#','sharp')+"_note"].play(loops=-1)
                if event.type == KEYUP:
                    time.sleep(.01)
                    if self.melodystate == True and self.pygame.key.name(event.key).upper() in self.keys.keys():
                        try:
                            globals()[self.keys[self.pygame.key.name(event.key).upper()]+"_note"].fadeout(1)
                            globals()[self.tuning+"_note"].play(loops=-1)
                            self.noteplaying=self.tuning
                        except:
                            pass


def main():
    hurdy=PyHurdy(tuning="g0")

if __name__ == "__main__":
    main()
