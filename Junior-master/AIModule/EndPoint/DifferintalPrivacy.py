import joblib
from EndPoint.PrivacyModule import Privacymodule
import os

class DifferintialPrivacy:

    
    def __init__(self):
        if not os.path.exists(os.getcwd()+"/EndPoint/assets/pack/Privacy.pb"):
            x = Privacymodule()
            x.start()
        self.__Privacymodel = joblib.load(os.getcwd()+"/EndPoint/assets/pack/Privacy.pb")
        
    def answer(self, number):
       return  self.__Privacymodel.predict(number)