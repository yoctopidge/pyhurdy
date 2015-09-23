#! /usr/bin/env python
import time, collections, os
import numpy, pygame.mixer, pygame.sndarray
from pygame.locals import *
import pygame
from scikits.samplerate import resample



class PyHurdy():
    def __init__(self, tuning):
        # Sounds
        self._tenor = "./sounds/drones/tenor.wav"
        self._bass = "./sounds/drones/bass.wav"
        self._high_melody = "./sounds/melody/high.wav"
        self._melody = "./sounds/melody/high.wav"
        self.pygame=pygame
        self.tenorstate=False
        self.tuning = tuning
        self.bassstate=False
        self.melodystate=False
        self.noteplaying=self.tuning
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
        # Initialise font support
        self.pygame.font.init()
        self.pygame.mixer.init(44100,-16,2,4096)
        # Render the screen
        self.pygame.display.update()
        self.init_sounds(tuning="g0")
        self.set_scale()
        self.play()

    def set_scale(self):
        # Ok. So, why the big dictionary of ratios? Because while we could just
        # extrapolate the resample ratio, that would mean that we are assuming
        # that the scale is all 12ths and we do not want to make that assumption.
        # So, while this seems messy, for now, we want to do this

        self.note_dict=collections.OrderedDict()

        self.note_dict = {'c0': {'ratio': 1, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'csharp0': {'ratio': 1.059, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'd0': {'ratio': 1.122, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'dsharp0': {'ratio': 1.189, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'e0': {'ratio': 1.26, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'f0': {'ratio': 1.335, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'fsharp0': {'ratio': 1.414, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'g0': {'ratio': 1.335, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'gsharp0': {'ratio': 1.587, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'a1': {'ratio': 1.682, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'asharp1': {'ratio': 1.782, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'b1': {'ratio': 1.888, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'c1': {'ratio': 2, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'csharp1':{'ratio':2.118, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'd1':{'ratio':2.244, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'dsharp1':{'ratio':2.378, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'e1':{'ratio':2.52, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'f1':{'ratio':2.67, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'fsharp1':{'ratio':2.828, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'g1':{'ratio':2.67, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'gsharp1': {'ratio': 3.174, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'a2':{'ratio':3.364, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'asharp2':{'ratio':3.564, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'b2':{'ratio':3.776, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'c2':{'ratio':4, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'csharp2':{'ratio':4.236, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'd2':{'ratio':3.366, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'dsharp2':{'ratio':3.567, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'e2':{'ratio':3.78, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'f2':{'ratio':4.005, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'fsharp2':{'ratio':4.242, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'g2':{'ratio':4.005, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'gsharp2': {'ratio': 4.761, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'a3':{'ratio':5.046, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'asharp3':{'ratio':5.346, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'b3':{'ratio':5.664, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'c3':{'ratio':6, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'csharp3':{'ratio':6.354, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'd3':{'ratio':4.488, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'dsharp3':{'ratio':4.756, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'e3':{'ratio':5.04, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'f3':{'ratio':5.34, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'fsharp3':{'ratio':5.656, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'g3':{'ratio':5.34, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'gsharp3':{'ratio':6.348, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'a4':{'ratio':6.728, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'asharp4':{'ratio':7.128, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'b4':{'ratio':7.552, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'c4':{'ratio':8, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''},
        'csharp4':{'ratio':8.472, 'key':'', 'snd_arry': '', 'resist': 0, 'octave': 0, 'row': ''}}

        self.notes = ['c0','csharp0','d0','dsharp0','e0','f0','fsharp0','g0','gsharp0','a1','asharp1','b1', \
                      'c1', 'csharp1', 'd1', 'dsharp1', 'e1', 'f1', 'fsharp1', 'g1', 'gsharp1', 'a2', 'asharp2', 'b2', \
                      'c2', 'csharp2', 'd2', 'dsharp2', 'e2', 'f2', 'fsharp2', 'g2', 'gsharp2', 'a3', 'asharp3', 'b3', \
                      'c3', 'csharp3', 'd3', 'dsharp3', 'e3', 'f3', 'fsharp3', 'g3', 'gsharp3', 'a4', 'asharp4', 'b4', \
                      'c4', 'csharp4']
        self.toprow = ['F1','F2','F3','F4','F5','F6','F7','F8','F9']
        self.bottomrow = ['1','2','3','4','5','6','7','8','9','10', '-','=','BACKSPACE']
        self.num_top_keys = len(self.toprow)
        self.num_bottom_keys = len(self.bottomrow)
        self.num_keys=self.num_top_keys+self.num_bottom_keys
        self.top_keys=[]
        self.bottom_keys=[]
        self.keys={}
        d = collections.deque(self.notes)
        d.rotate(len(self.notes)-(self.notes.index(self.tuning)+1))
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
            print (str(self.top_keys.index(x)) + " " + x)
            print self.note_dict[x]['key']
            self.keys[self.note_dict[x]['key']]=x

        for x in self.bottom_keys:
            print (str(self.bottom_keys.index(x)) + " " + x)
            print self.note_dict[x]['key']
            self.keys[self.note_dict[x]['key']]=x


        print str(self.note_dict)
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
                        print self.note_dict[self.noteplaying]['ratio']
                        print self.note_dict[self.keys[self.pygame.key.name(event.key).upper()]]['ratio']
        #                if float(self.note_dict[noteplaying]['ratio']) < float(self.note_dict[self.keys[pygame.key.name(event.key).upper()]]['ratio']):
                        globals()[self.noteplaying+"_note"].fadeout(1)
                        self.noteplaying = self.keys[self.pygame.key.name(event.key).upper()]
                        globals()[self.noteplaying+"_note"].play(loops=-1)
                        print self.note_dict[self.noteplaying]['ratio']
                        print self.note_dict[self.keys[self.pygame.key.name(event.key).upper()]]['ratio']
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
