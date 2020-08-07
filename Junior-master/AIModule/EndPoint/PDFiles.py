import pdfkit
from shutil import copy2
import os
############################################################################################
##                                                                                        ##
##                                         FIN                                            ##
##                                                                                        ##
############################################################################################
  
class makePDF:


    def __init__(self):
        copy2(os.getcwd()+"/EndPoint/assets/pack/PDFtemplate.html",os.getcwd()+"/EndPoint/data/PDF.html")
        self.__template = open(os.getcwd()+"/EndPoint/data/PDF.html","a",encoding="utf-8")
        self.__template.write("\n")
    
    
    def __AddTextPage(self,cnt):
        fi = open(os.getcwd()+"/EndPoint/data/CleanText"+str(cnt)+".txt",encoding="utf-8")
        self.__template.write('\t\t\t<div>\n')
        for i in fi:
            self.__template.write('\t\t\t\t<p style = " font-size:15px ; font-family:Arial, Helvetica, sans-serif;" >'+i.replace("\n","")+ '</p>\n')
        fi.close()
        self.__template.write('\t\t\t</div>\n')


    def __AddPicPage(self,cnt):
        self.__template.write('\t\t\t<div>\n')
        string ="CleanPic"+str(cnt)+".jpg"
        self.__template.write('\t\t\t\t<img src='+repr(string)+'></img>\n')
        self.__template.write('\t\t\t</div>\n')


    def __save(self):
        options = {
                'encoding': "UTF-8",
                'page-size' : 'A4',
                'dpi' : 400
            }
        self.__template.write("\t\t</body>\n</html>")
        self.__template.close()
        pdfkit.from_file(os.getcwd()+"/EndPoint/data/PDF.html",os.getcwd()+"/EndPoint/result.pdf",options=options)


    def MakePdf(self, cntPic , cntTxt):
        for i in range(cntTxt):
            self.__AddTextPage(i)
        for i in range(cntPic):
            self.__AddPicPage(i)
        self.__save()
