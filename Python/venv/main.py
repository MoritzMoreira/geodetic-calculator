from tkinter import *
import grundlagen.gui
import grundlagen.winkel

def eingabefelder(p_rad, p_gon, p_grad):
    eingabe_gon.delete(0, END)
    eingabe_grad.delete(0, END)
    eingabe_rad.delete(0, END)

    eingabe_gon.insert(0, str(p_gon))
    eingabe_grad.insert(0, str(p_grad))
    eingabe_rad.insert(0, str(p_rad))


class Anwendung(Frame):
    def __init__(self, master):
        #Konstruktur der Elternklasse (frame) aufrufen. Diese bentigt als Parameter das uebergeordnete Widget,
        #also in diesem Fall Master, also das Top Level Widget (die Tk inter applikation an sich)
        super().__init__(master)
        self.meister=master
        self.eingabe_gon = Entry(self)
        self.eingabe_rad = Entry(self)
        self.eingabe_grad = Entry(self)

        self.initialisiere_gui()

    def initialisiere_gui(self):
        self.grid()
        beschriftung=Label(fenster,text="Umrechnung").grid(row=0,columnspan=3)

        Label(self,text="gon:", anchor=W,justify=LEFT,width=10).grid(row=1,column=1)
        Label(self,text="rad",anchor=W,justify=LEFT,width=10).grid(row=2,column=1)
        Label(self,text="grad",anchor=W,justify=LEFT,width=10).grid(row=3,column=1)

        self.eingabe_gon.grid(row=1, column=0)
        self.eingabe_rad.grid(row=2, column=0)
        self.eingabe_grad.grid(row=3, column=0)

        Button(self,text="Umrechnen", command=self.umrechnen_gon).grid(row=1,column=2)
        Button(self,text="Umrechnen", command=self.umrechnen_rad).grid(row=2,column=2)
        Button(self,text="Umrechnen", command=self.umrechnen_grad).grid(row=3,column=2)

        knopf=Button(self,text="Beenden",command=self.meister.destroy)
        knopf.grid(row=4,column=0,columnspan=3)

    def umrechnen_gon(self):
        p_gon = gui.auswerten(self.eingabe_gon)
        p_rad = winkel.gon2rad(rad)
        p_grad = (p_gon * 360.0) / 400.0
        self.eingabefelder(p_rad, p_gon, p_grad)

    def umrechnen_rad(self):
        p_rad = gui.auswerten(self.eingabe_rad)
        p_gon = (p_rad * 400.0) / (2 * math.pi)
        p_grad = (p_rad * 360.0) / (2 * math.pi)
        self.eingabefelder(p_rad, p_gon, p_grad)

    def umrechnen_grad(self):
        p_grad = gui.auswerten(self.eingabe_grad)
        p_gon = (p_grad * 400.0 / 360.0)
        p_rad = (p_grad * 2 * math.pi) / 360.0
        self.eingabefelder(p_rad, p_gon, p_grad)

if __name__ == "__main__":
    fenster=Tk()
    #master
    anwendung=Anwendung(fenster)
    fenster.mainloop()