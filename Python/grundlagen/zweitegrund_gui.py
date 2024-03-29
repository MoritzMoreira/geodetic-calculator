from tkinter import *
from math import *
from Scripts import winkel, gui
from grundlagen import gui, zweitegrund

class Anwendung(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.meister = master

        self.eingabe_y1 = Entry(self)
        self.eingabe_x1 = Entry(self)
        self.eingabe_y2 = Entry(self)
        self.eingabe_x2 = Entry(self)

        self.ausgabe_t12= Entry(self)
        self.ausgabe_s12=Entry(self)

        self.initialisiere_gui()

    def initialisiere_gui(self):
        self.grid()

        Label(self, text="2.Hauptaufgabe", anchor=W, justify=LEFT, width=25).grid(row=0, column=0, columnspan=4)

        self.eingabe_y1.grid(row=1, column=1)
        self.eingabe_x1.grid(row=2, column=1)
        self.eingabe_y2.grid(row=3, column=1)
        self.eingabe_x2.grid(row=4, column=1)

        self.ausgabe_t12.grid(row=1, column=3)
        self.ausgabe_s12.grid(row=2,column=3)

        Label(self, text="y1:", anchor=W, justify=LEFT, width=10).grid(row=1, column=0)
        Label(self, text="x1:", anchor=W, justify=LEFT, width=10).grid(row=2, column=0)
        Label(self, text="y2", anchor=W, justify=LEFT, width=10).grid(row=3, column=0)
        Label(self, text="x2", anchor=W, justify=LEFT, width=10).grid(row=4, column=0)
        Label(self, text="Richtungswinkel t12", anchor=W, justify=LEFT, width=10).grid(row=1, column=2)
        Label(self, text="Strecke s12", anchor=W, justify=LEFT, width=10).grid(row=2, column=2)

        Button(self, text="Umrechnen", command=self.umrechnen_gui).grid(row=0, column=2)
        Button(self, text="Test", command=self.test2).grid(row=0, column=3)
        Button(self, text="Beenden", command=self.meister.destroy).grid(row=4, column=3)


    def umrechnen_gui(self):
        y1= gui.eingabefeld_auswerten(self.eingabe_y1)
        x1 = gui.eingabefeld_auswerten(self.eingabe_x1)
        y2= gui.eingabefeld_auswerten(self.eingabe_y2)
        x2= gui.eingabefeld_auswerten(self.eingabe_x2)

        s12, t12=zweitegrund.umrechnen_koordinaten(y1,x1,y2,x2)

        self.ausgabefeld_schreiben(t12,s12)

    def test2(self):
        y1=528.15
        x1=407.65
        y2=795.17
        x2=525.1

        self.eingabefelder_schreiben(y1,x1,y2,x2)

    def eingabefelder_schreiben(self, p_y1, p_x1, p_y2, p_x2):
        gui.eingabefeld_schreiben(self.eingabe_y1, p_y1)
        gui.eingabefeld_schreiben(self.eingabe_x1, p_x1)
        gui.eingabefeld_schreiben(self.eingabe_y2, p_y2)
        gui.eingabefeld_schreiben(self.eingabe_x2, p_x2)


    def ausgabefeld_schreiben(self, p_t12, p_s12):
        gui.eingabefeld_schreiben(self.ausgabe_t12, p_t12)
        gui.eingabefeld_schreiben(self.ausgabe_s12, p_s12)


if __name__ == "__main__":

    fenster = Tk()

    anwendung = Anwendung(fenster)

    fenster.mainloop()
