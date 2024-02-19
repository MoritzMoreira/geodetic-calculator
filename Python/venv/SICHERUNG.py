def umrechnen_rad(self):
    rad = gui.auswerten(self.eingabe_rad)
    gon = winkel.rad2gon(rad)
    deg = winkel.rad2deg(rad)
    self.eingabefelder_schreiben(rad, gon, deg)


def umrechnen_gon(self):
    gon = gui.auswerten(self.eingabe_gon)
    rad = winkel.gon2rad(gon)
    deg = winkel.gon2deg(gon)
    self.eingabefelder_schreiben(rad, gon, deg)


def umrechnen_deg(self):
    deg = gui.auswerten(self.eingabe_deg)
    gon = winkel.deg2gon(deg)
    rad = winkel.deg2rad(deg)
    self.eingabefelder_schreiben(rad, gon, deg)


def eingabefelder_schreiben(self, p_rad, p_gon, p_deg):
    gui.eingabefeld_schreiben(self.eingabe_rad, p_rad)
    gui.eingabefeld_schreiben(self.eingabe_gon, p_gon)
    gui.eingabefeld_schreiben(self.eingabe_deg, p_deg)


# HINWEIS: Elemente in Zeile oder Spalte 0 benötigen kein "row" oder "column" Attribut
# Zeile 0

# Label mit fenster als Masterelement. Ausdehnung über drei Spalten
Label(self, text="PGA | Winkelumrechnungen").grid(row=0, column=0, columnspan=3)

# Zeilen 1 - 3

# Spalte 0: Eingabefelder

self.eingabe_rad.grid(row=1, column=0)
self.eingabe_gon.grid(row=2, column=0)
self.eingabe_deg.grid(row=3, column=0)

# Spalte 1: Beschriftungen

# Anker ist an der westlichen Seite, linksbündig und Breite 10
Label(self, text="[rad]", anchor=W, justify=LEFT, width=10).grid(row=1, column=1)
Label(self, text="[gon]", anchor=W, justify=LEFT, width=10).grid(row=2, column=1)
Label(self, text="[°]", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)

# Spalte 2: Knöpfe

# HINWEIS: Bitte nicht "command=umrechnenrad()", also mit Klammern, verwenden, da sonst "umrechnenrad"
# unmittelbar beim Start des Programms aufgerufen wird und nicht erst beim Klick auf den Knopf!
Button(self, text="Umrechnen", command=self.umrechnen_rad).grid(row=1, column=2)
Button(self, text="Umrechnen", command=self.umrechnen_gon).grid(row=2, column=2)
Button(self, text="Umrechnen", command=self.umrechnen_deg).grid(row=3, column=2)








fenster=Tk()
        Label(self,text="1.Hauptaufgabe", anchor=W,justify=LEFT,width=25).grid(row=0,column=0, columnspan=4)

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


def eingabefelder_schreiben(self, p_y1, p_x1, p_y2, p_x2):
    gui.eingabefeld_schreiben(self.eingabe_y1, p_y1)
    gui.eingabefeld_schreiben(self.eingabe_x1, p_x1)
    gui.eingabefeld_schreiben(self.eingabe_y2, p_y2)
    gui.eingabefeld_schreiben(self.eingabe_x2, p_x2)


def ausgabefeld_schreiben(self, p_t12, p_s12):
    gui.eingabefeld_schreiben(self.ausgabe_t12, p_t12)
    gui.eingabefeld_schreiben(self.ausgabe_s12, p_s12)


fenster=Tk()
    Label(fenster,text="2.Hauptaufgabe", anchor=W,justify=LEFT,width=25).grid(row=0,column=0, columnspan=4)

    Label(fenster,text="y1:",anchor=W,justify=LEFT,width=10).grid(row=1,column=0)
    Label(fenster,text="x1:",anchor=W,justify=LEFT,width=10).grid(row=2,column=0)
    Label(fenster,text="y2:",anchor=W,justify=LEFT,width=10).grid(row=3,column=0)
    Label(fenster,text="x2:",anchor=W,justify=LEFT,width=10).grid(row=4,column=0)

    eingabe_y1=Entry(fenster)
    eingabe_x1=Entry(fenster)
    eingabe_y2=Entry(fenster)
    eingabe_x2=Entry(fenster)

    eingabe_y1.grid(row=1, column=1)
    eingabe_x1.grid(row=2, column=1)
    eingabe_y2.grid(row=3, column=1)
    eingabe_x2.grid(row=4, column=1)

    Button(fenster,text="Umrechnen", command=umrechnen_gui).grid(row=0,column=2)

    ausgabe_s12=Entry(fenster)
    ausgabe_t12=Entry(fenster)

    ausgabe_s12.grid(row=2, column=2)
    ausgabe_t12.grid(row=4, column=2)

    Label(fenster,text="Strecke, s12:", anchor=W,justify=LEFT,width=10).grid(row=1,column=2)
    Label(fenster,text="Richtung, t12:", anchor=W,justify=LEFT,width=10).grid(row=3,column=2)

    test2()
    Button(fenster,text="Beenden",command=fenster.destroy).grid(row=5,column=2, columnspan=3)

