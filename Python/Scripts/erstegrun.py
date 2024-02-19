from tkinter import *
from math import *
from Scripts import winkel, gui


def umrechnen_gui():
    y1= gui.auswerten(eingabe_y1)
    x1 = gui.auswerten(eingabe_x1)
    s12= gui.auswerten(eingabe_s12)
    t12= gui.auswerten(eingabe_t12)

    y2,x2=umrechnen_koordinaten(y1,x1,s12,t12)

    gui.eingabefeld_schreiben(ausgabe_y2, y2)
    gui.eingabefeld_schreiben(ausgabe_x2, x2)

def umrechnen_koordinaten(y1,x1,s12,t12):
    sin_t12=sin(winkel.gon2rad(t12))
    cos_t12=cos(winkel.gon2rad(t12))

    y2=y1+s12*sin_t12
    x2=x1+s12*cos_t12

    return y2,x2

def test1():
    y1=16.1
    x1=23.06
    s12=17.11
    t12=214.199

    gui.eingabefeld_schreiben(eingabe_y1, y1)
    gui.eingabefeld_schreiben(eingabe_x1, x1)
    gui.eingabefeld_schreiben(eingabe_s12, s12)
    gui.eingabefeld_schreiben(eingabe_t12, t12)


fenster=Tk()
Label(fenster,text="1.Hauptaufgabe", anchor=W,justify=LEFT,width=25).grid(row=0,column=0, columnspan=4)

Label(fenster,text="y1:", anchor=W,justify=LEFT,width=10).grid(row=1,column=0)
Label(fenster,text="x1:",anchor=W,justify=LEFT,width=10).grid(row=2,column=0)
Label(fenster,text="s12",anchor=W,justify=LEFT,width=10).grid(row=3,column=0)
Label(fenster,text="t12",anchor=W,justify=LEFT,width=10).grid(row=4,column=0)

eingabe_y1=Entry(fenster)
eingabe_x1=Entry(fenster)
eingabe_s12=Entry(fenster)
eingabe_t12=Entry(fenster)

eingabe_y1.grid(row=1, column=1)
eingabe_x1.grid(row=2, column=1)
eingabe_s12.grid(row=3, column=1)
eingabe_t12.grid(row=4, column=1)

Button(fenster,text="Umrechnen", command=umrechnen_gui).grid(row=0,column=2)

ausgabe_x2=Entry(fenster)
ausgabe_y2=Entry(fenster)

ausgabe_x2.grid(row=2, column=2)
ausgabe_y2.grid(row=4, column=2)

Label(fenster,text="Hoch, x2:", anchor=W,justify=LEFT,width=10).grid(row=1,column=2)
Label(fenster,text="Rechts, y2:", anchor=W,justify=LEFT,width=10).grid(row=3,column=2)

test1()
Button(fenster,text="Beenden",command=fenster.destroy).grid(row=5,column=2, columnspan=3)

fenster.mainloop()

