# -*- coding: utf-8 -*-
import serial
import pyautogui
from threading import Thread
from time import sleep
from Tkinter import Button, Label, Tk
import ttk



#TODO : Ajouter choix du port com par liste déroulante. Ou dans un fichier de config?
#TODO : Choix de l'unité ( menu deroulant ) et transformation du poids en conséquence


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Récupération des pesées')
        self.geometry("300x120")
        self.label = Label(self, text="Stopper.")
        self.label.pack()
        self.label2 = Label(self, text="")
        self.label2.pack()
        self.convert = Label(self,text="Choix de l'unité de masse :")
        self.convert.pack()
        self.combo = ttk.Combobox(self, values=listunit, state="readonly",
                                  height=4)
        self.combo.set('g')
        self.combo.bind("<<ComboboxSelected>>", self.test)
        self.combo.pack()
        self.play_button = Button(self, text="Play", command=self.play)
        self.play_button.pack(side='bottom',padx=2, pady=2)
        #self.stop_button = Button(self, text="Stop", command=self.stop)
        #self.stop_button.pack(side="left", padx=2, pady=2)
        self._thread, self._stop = None, True

    def test(self, event):
        #print(self.combo.get())
        #print(event)
        self.label2["text"] = 'convert: ' + self.combo.get()

    def action(self):  
        while True:
            if not ser.isOpen():
                ser.open()
            ser.reset_output_buffer()
            print('On attend que la balance envoie le poids')
            #Modif de read_until de serialutil.py du package pyserial
            expected = ('\r\n')
            lenterm = len(expected)
            line = bytearray()
            while True:
                c = ser.read(1)
                if self._stop:
                    break
                if c:
                    line += c
                    if line[-lenterm:] == expected:
                        break
            if self._stop:
                print('on ferme le port')
                ser.close()
                break
            response = bytes(line)
            response = response.strip().split(' ')
            ser.reset_output_buffer()
            poids = response
            print('m :' + poids[0] + '-unité :' + poids[1])
            print('convert: ' + self.combo.get())
            print(convertmasse(unitmasse,poids[0],poids[1],self.combo.get()))
            self.label2["text"] = 'm :' + poids[0] + '-unité :' + poids[1]
            #Utilisation de pyautogui pour copier les valeurs automatiquement
            pyautogui.typewrite(str(convertmasse(unitmasse,poids[0],poids[1],self.combo.get()))+'\n')


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


def convertmasse(dictunit, valeur, unit_in, unit_out):
    return float(valeur)*dictunit[unit_in]/dictunit[unit_out]


if __name__ == '__main__':

    ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1
                        )

    #Définition du dict pour convertir les unitées et de la list
    unitmasse = {'kg': 1000, 'hg': 100, 'dag': 10, 'g': 1, 'dg': 0.1,
                 'cg': 0.01, 'mg': 0.001, 'dmg': 0.0001, 'µg': 0.000001}
    listunit = [key for key, value in sorted(unitmasse.iteritems(), key=lambda (k, v): (v, k), reverse=True)]


    App().mainloop()