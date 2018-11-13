# -*- coding: utf-8 -*-
import serial
import sys
import glob
import pyautogui
from threading import Thread
from time import sleep
from Tkinter import Button, Label, Tk
import ttk
import tkMessageBox

#TODO : Vérifier que la balance est bien une mettler? voir dans metler_toledo_device?


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Récupération des pesées')
        self.geometry("300x160")
        self.label = Label(self, text="Stopper.")
        self.label.pack()
        self.label2 = Label(self, text="")
        self.label2.pack()
        self.convert = Label(self,text="Choix de l'unité de masse :")
        self.convert.pack()
        self.combo = ttk.Combobox(self, values=listunit, state="readonly", height=4)
        self.combo.set('g')
        self.combo.bind("<<ComboboxSelected>>")
        self.combo.pack()
        self.labelSerie = Label(self, text="Choix du port série :")
        self.labelSerie.pack()
        self.comboSerie = ttk.Combobox(self, values=listportserie, state="readonly", height=4)
        self.comboSerie.bind("<<ComboboxSelected>>")
        self.comboSerie.pack()
        self.play_button = Button(self, text="Play", command=self.play)
        self.play_button.pack(side='bottom',padx=2, pady=2)
        #self.stop_button = Button(self, text="Stop", command=self.stop)
        #self.stop_button.pack(side="left", padx=2, pady=2)
        self._thread, self._stop = None, True

    def action(self):
        ser = serial.Serial(port=self.comboSerie.get(),
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=1
                            )
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
            pyautogui.typewrite(str(convertmasse(unitmasse,poids[0],poids[1], self.combo.get()))+'\n')


    def play(self):
        if not self.comboSerie.get():
            tkMessageBox.showinfo("Port série!", "Vous devez choisir le port série de la balance!")
        else:
            if self._thread is None:
                self._stop = False
                self._thread = Thread(target=self.action)
                self._thread.start()
            #self._pause = False
            self.play_button.configure(text="Stop", command=self.stop)
            self.label["text"] = "En attente de poids..."

    def stop(self):
        if self._thread is not None:
            #ser.close()
            self._thread, self._stop = None, True
        self.play_button.configure(text="Play", command=self.play)
        self.label["text"] = "Stopper"
        self.label2["text"] = ""


def convertmasse(dictunit, valeur, unit_in, unit_out):
    return float(valeur)*dictunit[unit_in]/dictunit[unit_out]


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':

    #Vérification du port série
    listportserie = serial_ports()
    if not listportserie:
        tkMessageBox.showerror("Erreur!", "Pas de port com sur ce PC!")
        sys.exit()
    else:
        #Définition du dict pour convertir les unitées et de la list
        unitmasse = {'kg': 1000, 'hg': 100, 'dag': 10, 'g': 1, 'dg': 0.1,
                     'cg': 0.01, 'mg': 0.001, 'dmg': 0.0001, 'µg': 0.000001}
        listunit = [key for key, value in sorted(unitmasse.iteritems(), key=lambda (k, v): (v, k), reverse=True)]


        App().mainloop()