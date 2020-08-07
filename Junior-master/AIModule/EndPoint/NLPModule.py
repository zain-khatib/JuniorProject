import numpy as np
import os
import pickle
import spacy

########################################################################################################
########################################################################################################
##                                                                                                    ##
##                                             FIN                                                    ##
##                                                                                                    ##
########################################################################################################
########################################################################################################



class NLPModule :
        
    def __init__(self , language):
        self.__model = spacy.load("en_core_web_sm")
        if language == 'German':
            self.__model = None
            self.__model = spacy.load("de_core_news_md")
        elif language == "Greek":
            self.__model = None
            self.__model = spacy.load("el_core_news_md")
        elif language == "French":
            self.__model = None
            self.__model = spacy.load("fr_core_news_md")
        elif language == "Spanish":
            self.__model = None
            self.__model = spacy.load("es_core_news_md")
        elif language == "Italian":
            self.__model = None
            self.__model = spacy.load("it_core_news_sm")
        elif language == "Lithuanian":
            self.__model = None
            self.__model = spacy.load("lt_core_news_sm")
        elif language == "Dutch":
            self.__model = None
            self.__model = spacy.load("nl_core_news_sm")
        elif language == "Portuguese":
            self.__model = None
            self.__model = spacy.load("pt_core_news_sm")
        elif language == "Norwegian":
            self.__model = None
            self.__model = spacy.load("nb_core_news_sm")
        self.__private_entities = ['DATE','GPE','NORP','PERSON','TIME']
        self.__biomarkers = ['Hemoglobin','Hematocrit','Leucocytic','Anti-Cardiolipin','Heterozygous','COBAS TaqMan','Haematocrit','Basophils','Prothrombin Time','Eosinophils','Neutrophils','Lymphoctes','Monocytes','Creatinine','Uric','Glucose','Bilirubin','Alanine Aminotransferase','Aspartate Aminotransferase','Albumin','Calcium','Thyroid Stimulating Hormone','Cholesterol','Epstein-barr','TORCH','Anti Cardiolipin','Prothrombin Concentration',
              'Prothrombin Time']

    def __DeleteModule(self):
        del self.__model


    def __ExtractDelWord(self , CntTxt , CntPic):
        for i in range(CntTxt):
            fi = open(os.getcwd()+"/EndPoint/data/Text"+str(i)+".txt",encoding = "UTF-8")
            doc = self.__model(fi.read())
            temp = set()
            for ent in doc.ents:
                if ent.label_ in self.__private_entities and len(ent.text) > 4 and ent.text not in self.__biomarkers: 
                    ls = ent.text.split()
                    for word in ls :
                        temp.add(word)
            file = open(os.getcwd()+"/EndPoint/data/dellsttxt"+str(i)+".p","wb")
            pickle.dump(temp,file)
            file.close()
            fi.close()
        for i in range(CntPic):
            fi = open(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt",encoding="UTF-8")
            doc = self.__model(fi.read())
            temp = set()
            for ent in doc.ents:
                if ent.label_ in self.__private_entities and len(ent.text) > 4 and ent.text not in self.__biomarkers: 
                    ls = ent.text.split()
                    for word in ls :
                        temp.add(word)
            file = open(os.getcwd()+"/EndPoint/data/dellstpic"+str(i)+".p","wb")
            pickle.dump(temp,file)
            file.close()
            fi.close()
            
    # this function for the correction
    def __med(self, x , y):
        res = np.zeros((2000,2000))
        for i in range(0,len(x)):
            res[i, 0] = i
        for j in range(len(y)):
            res[0 , j] = j
        for i in range(1, len(x)):
            for j in range(1, len(y)):
                c1= res[i, j-1] + 1
                c2= res[i-1, j] + 1
                if(x[i-1] == y[j-1]):
                    c3= res[i-1, j-1]
                else:
                    c3= res[i-1, j-1]+ 2
                res[i, j]= min(c1, c2, c3)
        return res[len(x)-1][len(y)-1]

    def __make_words(self , cntPic , CntTxt):
        for i in range(cntPic):
            ret = set()
            fi = open(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt",encoding="UTF-8")
            for x in fi.readlines():
                for word in x.split():
                    if word != "":
                        ret.add(word)
            file = open(os.getcwd()+"/EndPoint/data/wordspic"+str(i)+".p","wb")
            pickle.dump(ret,file)
            file.close()
            fi.close()
        
    def findMinDistance(self,picnum,string):
        li = pickle.load(open(os.getcwd()+"/EndPoint/data/wordspic"+str(picnum)+".p","rb"))
        minimum_dis = 1000000
        if string in li: 
            return string
        ret = ""
        for word in li :
            temp = self.__med(word,string)
            if temp < minimum_dis:
                minimum_dis = temp
                ret = word
        return ret

    def ForDel(self , cntpic, cnttxt):
        if cntpic > 0:
            self.__make_words(cntpic,cnttxt)
        self.__ExtractDelWord(cnttxt,cntpic)
        self.__DeleteModule()
