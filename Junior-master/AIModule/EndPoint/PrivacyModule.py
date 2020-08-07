from sklearn import datasets
from sklearn.model_selection import train_test_split
import diffprivlib.models as models
import joblib
import os
import random 
class Privacymodule:
    
    
    def __init__(self):
        dataset = []
        dataset2 = []
        for i in range(0,1000):
            dataset.append([random.randint(0,1000)])
            dataset2.append(random.randint(0,1000))
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(dataset, dataset2, test_size=0.2)
    

    def __save(self, module):
        joblib.dump(module, os.getcwd()+"/EndPoint/assets/pack/Privacy.pb")
        

    def start(self):
        module = models.GaussianNB()
        module.fit(self.__X_train,  self.__y_train)
        self.__save(module)
