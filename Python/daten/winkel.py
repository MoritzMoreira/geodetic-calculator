import grundlagen.winkel



class Winkel:
    def __init__(self,p_rad=0.0, p_nr=""):
        """primaerer Konstruktor

        :param p_rad: Winkelgroesse in radiant
        :type p_rad : float
        :param p_nr: Nummer
        :type p_nr: str
        """
        self.__rad=p_rad
        self.__nr: str = p_nr
    @classmethod
    def deg(cls,p_deg=0.0, p_nr=""):
        """

        :param p_deg: Winkelgroesse in Grad
        :type p_deg: float
        :param p_nr: Nummer
        :type p_nr: str
        :return: Instanz der Klasse Winkel
        :rtype: Winkel
        """
        return cls(grundlagen.winkel.deg2rad(p_deg),p_nr)
    @classmethod
    def gon(cls,p_gon=0.0, p_nr=""):
        """

        :param p_deg: Winkelgroesse in Grad
        :type: float
        :param p_nr: Nummer
        :type p_nr: str
        :return: Instanz der Klasse Winkel
        :rtype: Winkel
        """
        return cls(grundlagen.winkel.gon2rad(p_gon), p_nr)

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



    def setze_gon(self,p_gon):
        """setter in gon

        :param p_gon: Winkelgroesse in Gon
        :type: float
        """
        self.__rad=grundlagen.winkel.gon2rad(p_gon)

    def hole_gon(self):
        """getter in gon
        :return: Winkelgroesse in Gon
        :rtype: float
        """
        return grundlagen.winkel.rad2gon(self.__rad)

    def setze_deg(self,p_deg):
        """setter in deg

        :param p_deg: Winkelgroesse in Deg
        :type: float
        """
        self.__deg=grundlagen.winkel.deg2rad(p_deg)

    def hole_deg(self):
        """getter in deg
        :return: Winkelgroesse in Deg
        :rtype: float
        """
        return grundlagen.winkel.rad2deg(self.__rad)

    def setze_rad(self,p_rad):
        """setter in rad

        :param p_gon: Winkelgroesse in Rad
        :type: float
        """
        self.__rad=p_rad

    def hole_rad(self):
        """getter in rad
        :return: Winkelgroesse in Rad
        :rtype: float
        """
        return self.__rad

    def __str__(self):
        zeichen: str= "Nr:" + self.__nr + \
                      " rad:" + str(self.__rad) + \
                      " deg" + str(grundlagen.winkel.rad2deg(self.__rad)) + \
                      " gon" + str(grundlagen.winkel.rad2gon(self.__rad))
        return zeichen

if __name__=="__name__":
    w_rad=Winkel(math.pi)
    w_deg=Winkel.deg(180.0)
    w_gon=Winkel.gon(200.0)



