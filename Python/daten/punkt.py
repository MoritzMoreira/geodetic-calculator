class Punkt:
    def __init__(self,p_y=0.0,p_x=0.0, p_nr=""):
        self.__y: float=p_y
        self.__x: float=p_x

        self.oeffentlich: int=42

        self._geschuetzt: int=42
        self.__nr=p_nr

    def setze_y(self,p_y: float):
        self.__y=p_y
    def setze_x(self,p_x: float):
        self.__x=p_x
    def hole_y(self) ->float:
        return self.__y
    def hole_x(self) -> float:
        return self.__x
    def setze_json(self, p_dict):
        for schluessel, wert in p_dict.items():
            print(schluessel + ":" + str(wert))
            setattr(self,schluessel, wert)


    def hole_json(self) -> dict:
        return self.__dict__
    def __str__(self) -> str:
        zeichenkette: str= 'Nr. ' + self.__nr + ':  y = ' + str(self.__y) + ', x = ' + str(self.__x)
        return zeichenkette
    def setze_nr(self,p_nr: str):
        """setter in gon

        :param p_gon: Winkelgroesse in Gon
        :type: float
        """
        self.__nr=p_nr

    def hole_nr(self):
        """getter in gon
        :return: Winkelgroesse in Gon
        :rtype: float
        """
        return self.__nr

    @staticmethod
    def json2punktliste(p_json_daten) -> object:
        punktliste = {}
        for schluessel, wert in p_json_daten.items():
            p = Punkt()
            p.setze_json(wert)
            punktliste[schluessel] = p
        return punktliste




if __name__=="__main__":
    p1: Punkt=Punkt(42.4,24.2, "p1")
    print(p1.oeffentlich)
    print(p1)
    pass