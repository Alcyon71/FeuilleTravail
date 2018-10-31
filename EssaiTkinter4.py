# -*- coding: utf-8 -*-
import serial
from threading import Thread
from time import sleep
from Tkinter import Button, Label, Tk

ser = serial.Serial(port='/dev/ttyUSB0',
                         baudrate=9600,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS,
                         timeout=1
                        )


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Récupération des pesées')
        self.geometry("300x70")
        self.label = Label(self, text="Stopper.")
        self.label.pack()
        self.label2 = Label(self, text="")
        self.label2.pack()
        self.play_button = Button(self, text="Play", command=self.play)
        self.play_button.pack(padx=2, pady=2)
        #self.stop_button = Button(self, text="Stop", command=self.stop)
        #self.stop_button.pack(side="left", padx=2, pady=2)
        self._thread, self._stop = None, True

    def action(self):  
        while True:
            # if self._stop:
            #     print('on ferme le port')
            #     ser.close()
            #     break
            #while self._pause:
            #    self.label["text"] = "Pause... "
            #    sleep(0.1)
            if not ser.isOpen():
                ser.open()
            ser.reset_output_buffer()
            print('On attend que la balance envoie le poids')
            #Modif de read_until de serialutil.py du package pyserial
            expected = ('\r\n')
            lenterm = len(expected)
            line = bytearray()
            timeout = 1
            while True:
                c = ser.read(1)
                if self._stop:
                    break
                if c:
                    line += c
                    if line[-lenterm:] == expected:
                        break
                #else:
                #    break
            if self._stop:
                print('on ferme le port')
                ser.close()
                break
            response = bytes(line)
            #response = ser.read_until('\r\n')
            response = response.strip().split(' ')
            ser.reset_output_buffer()
            poids = response
            print('m :' + poids[0] + '-unité :' + poids[1])
            self.label2["text"] = 'm :' + poids[0] + '-unité :' + poids[1]


    def play(self):
        if self._thread is None:
            self._stop = False
            self._thread = Thread(target=self.action)
            self._thread.start()
        #self._pause = False
        self.play_button.configure(text="Stop", command=self.stop)
        self.label["text"] = "En attente de poids..."

    #def pause(self):
    #    self._pause = True
    #    self.play_button.configure(text="Play", command=self.play)

    def stop(self):
        if self._thread is not None:
            #ser.close()
            self._thread, self._stop = None, True
        self.play_button.configure(text="Play", command=self.play)
        self.label["text"] = "Stopper"
        self.label2["text"] = ""


App().mainloop()