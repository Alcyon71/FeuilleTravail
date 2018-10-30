# -*- coding: utf-8 -*-
import serial
from Tkinter import *

def read_weight(socket):
    # bal = serial.Serial(port='/dev/ttyUSB0',
    #                     baudrate=9600,
    #                     parity=serial.PARITY_NONE,
    #                     stopbits=serial.STOPBITS_ONE,
    #                     bytesize=serial.EIGHTBITS
    #                     )
    socket.reset_output_buffer()
    print('On attend que la balance envoie le poids')
    response = socket.read_until('\r\n')
    socket.reset_output_buffer()
    #bal.close()
    return response


class Interface(Frame):
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0

        # Création de nos widgets
        self.message = Label(self, text="Pas de pesée reçu.")
        self.message.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack(side="left")

        self.bouton_activer = Button(self, text="Activer", command=self.activer)
        self.bouton_activer.pack(side="right")

        self.bouton_desactiver = Button(self, text="Désactiver", command=self.desactiver)
        self.bouton_desactiver.pack(side="center")

    def desactiver(self):

    def activer(self):
        ser = serial.Serial(port='/dev/ttyUSB0',
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS
                            )
        if not ser.isOpen():
            ser.open()

        while True:
            print(read_weight(ser))

    #     self.bouton_cliquer = Button(self, text="Cliquez ici", fg="red",
    #                                  command=self.cliquer)
    #     self.bouton_cliquer.pack(side="right")
    #
    # def cliquer(self):
    #     """Il y a eu un clic sur le bouton.
    #
    #     On change la valeur du label message."""
    #
    #     self.nb_clic += 1
    #     self.message["text"] = "Vous avez cliqué {} fois.".format(self.nb_clic)


fenetre = Tk()
fenetre.title('Récupération des pesées')
fenetre.geometry("300x50")
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()
