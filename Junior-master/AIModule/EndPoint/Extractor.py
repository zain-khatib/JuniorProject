import wand.image as wimage
from wand.color import Color
import os
import pytesseract
import shutil
import cv2
from PIL import Image, ImageSequence
import fitz
import numpy as np

########################################################################################################
########################################################################################################
##                                                                                                    ##
##                                             FIN                                                    ##
##                                                                                                    ##
########################################################################################################
########################################################################################################


class Extractor:

    ## when we call the ocr module we need to make a file named data 
    # in the future we can modify this and use tempfolder for the privacy 
    # but for now this works fine
    def __init__(self):
        self.__lang_pack = np.load(os.getcwd()+"/EndPoint/assets/pack/lang_pack.npy",allow_pickle='TRUE').item()
        try:  
            os.mkdir(os.getcwd()+"/EndPoint/data")  
        except Exception as e:
            e.args  
            print("error accourd while making the directory !") 

    # this function to delete the folder whith all what's in it so we can free up some memory !
    def delete(self,FileName):
        try:
            shutil.rmtree(FileName)
        except Exception as e:
            e.args
            print("dir is not found !")

    def __getText(self,filename):
        (fi, fo, fe) = os.popen('catdoc -w "%s"'%filename)
        fi.close()
        retval = fo.read()
        error = fe.read()
        fo.close()
        fe.close()
        if not error :
            return retval
        return ""

    def __HandleDocuments(self,DocURL , lang):
        fi = open(os.getcwd()+"/EndPoint/data/Text0.txt","w+",encoding="UTF-8")
        fi.writelines(self.__getText(DocURL))
        fi.close()
        return (0,1)
    
    
    def __MakeHighResolutionImage(self, img , cnt , res = 300):
        #open the image first
        try:
            with wimage.Image(filename=img ,resolution= res) as img_pdf:
                    #change the background color to white
                    img_pdf.background_color = Color('white')
                    #remove the alpha channel -> RGBA to RGB
                    img_pdf.alpha_channel = 'remove'
                    #resize the image
                    img_pdf.resize(960,1376)
                    #save the image
                    img_pdf.save(filename=os.getcwd()+"/EndPoint/data/HighRes"+str(cnt)+".jpg")
        except Exception as e:
            e.args
            print("error in making the image high res")


    def __PDFFILES(self,PDFFile , lang):
        # note that this method will return a tuple the first value is the number of images in the pdf 
        # the second value of the tuple is the number of documents that been written
        # if we pass a link to the file we need to open the file first using 
        # PDFFile = fitz.open("location")
        # iterating over the pdf pages
        # counting the number of pages
        cntPic = 0
        cntText = 0
        for page in PDFFile:
            #getting the text and checking if there is a text in the file 
            # so i can write the text to file and continue we no need for the image and passing it to the tesseract 
            PDFText = page.getText()
            if PDFText != "":
                File = open(os.getcwd()+"/EndPoint/data/Text"+str(cntText)+".txt","w+",encoding="UTF-8")
                File.write(PDFText)
                File.close()
                self.__CleanFile(os.getcwd()+"/EndPoint/data/Text"+str(cntText)+".txt")
                cntText = cntText + 1
                continue
            #if we get here then the page is not a text it contains a picture so we get the picture handle it then pass it to the tesseract 
            pix = page.getPixmap()
            #saving the image as png !
            pix.writePNG(os.getcwd()+"/EndPoint/data/OriginalPic"+str(cntPic)+".jpg")
            #here we need to call for a function that make the image high resolution
            self.__MakeHighResolutionImage(os.getcwd()+"/EndPoint/data/OriginalPic"+str(cntPic)+".jpg" , cntPic)
            cntPic = cntPic + 1
        # iterating over the picture that been relesed and passing them to the OCR MODULE
        # and writing them to files !
        for i in range(cntPic):
            img = cv2.cv2.imread(os.getcwd()+"/EndPoint/data/HighRes"+str(i)+".jpg")
            text = self.__ExtractText(img,lang)
            fi = open(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt","w+",encoding="UTF-8")
            fi.writelines(text)
            fi.close()
            self.__CleanFile(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt")
            del img
        return (cntPic , cntText) 


    def __ExtractText(self, File , lang):
        try:
            p = pytesseract.image_to_string(File, lang=lang)
            return p
        except Exception as e:
            e.args
            print("error in the OCR module")
    

    def __HandleImage(self,img, lang):
        cnt = 0
        img=cv2.cv2.imread(img)
        cv2.cv2.imwrite(os.getcwd()+"/EndPoint/data/OriginalPic0.jpg",img)
        del img
        self.__MakeHighResolutionImage(os.getcwd()+"/EndPoint/data/OriginalPic0.jpg",cnt)
        cnt = cnt+1
        for i in range(cnt):
            img = cv2.cv2.imread(os.getcwd()+"/EndPoint/data/HighRes"+str(i)+".jpg")
            text = self.__ExtractText(img,lang)
            fi = open(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt","w+",encoding='UTF-8')
            fi.write(text)
            fi.close()
            self.__CleanFile(os.getcwd()+"/EndPoint/data/im"+str(i)+".txt")
            del img
        return (cnt,0)

    # this function can be replacied with kmp !
    def __find_all_indexes(self,string, pattern):
        ret = []
        length = len(string)
        index = 0
        while index < length:
            i = string.find(pattern, index)
            if i == -1:
                return ret
            ret.append(i)
            index = i + 1
        return ret


    def __CleanFile(self,file):
        fi = open(file,"r+",encoding='UTF-8')
        ToWrite = ""
        for line in fi.readlines():
            ls = line.strip()
            if len(ls)==0:
                continue
            if line.find('.') :
                temp = self.__find_all_indexes(line,'.')
                tp = ""
                prv = 0
                for i in temp :
                    tp += line[prv:i] + " "
                    prv = i
                line = tp
                ToWrite += line
        fi.close()
        fi = open(file,"w+",encoding = "UTF-8")
        fi.writelines(ToWrite)
        fi.close()

    # setting the passing language to a prefex
    def __set_lang(self,lang):
        if lang in self.__lang_pack.keys():
            return self.__lang_pack[lang]
        else :
            print ("cannot find language the language will set to the default english")
            lang = "eng"
        return lang

        
    # here is the controler function that only the user can use !
    # i will call it help XD for now until something come up in my mind 
    # u need to pass a file for now not a url actually i will make to function 
    # one for passing the file as a parameter and the second passing a url
    # help is a function that allow the user to pass the file directly
    
    def ProcessFile(self,docURL,lang):
        docURL = docURL[:len(docURL)-4]
        lang = self.__set_lang(lang)
        # this means the doc is a pdf file
        if docURL.endswith(".pdf") is True:
            pdf = fitz.open(docURL)
            countPic,countText = self.__PDFFILES(pdf,lang)
        elif docURL.endswith(".doc") is True or docURL.endswith(".docx") is True :
            countPic,countText = self.__HandleDocuments(docURL,lang)
        else:
            countPic,countText = self.__HandleImage(docURL,lang)
        return countPic,countText

    def ProcessFileMobile(self, object, lang, flag):
        countPic = 0
        countText = 0
        if flag == 0: #pic
            import base64
            image = base64.b64decode(object)
            fi = open(os.getcwd()+"/EndPoint/data/temporaryImage.jpg","w+",encoding="UTF-8")
            fi.writelines(image)
            countPic, countText = self.ProcessFile(os.getcwd()+"/EndPoint/data/temporaryImage.jpg", lang)
        elif flag == 1: #doc
            import base64
            doc = base64.b64decode(object)
            fi = open(os.getcwd()+"/EndPoint/data/temporaryDoc.docx","w+",encoding="UTF-8")
            fi.writelines(doc)
            countPic, countText = self.ProcessFile(os.getcwd()+"/EndPoint/data/temporaryDoc.doc", lang)
        elif flag == 2: #pdf
            import base64
            pdf = base64.b64decode(object)
            fi = open(os.getcwd()+"/EndPoint/data/temporaryPDF.pdf","w+",encoding="UTF-8")
            fi.writelines(pdf)
            countPic, countText = self.ProcessFile(os.getcwd()+"/EndPoint/data/temporaryPDF.pdf", lang)
        return countPic, countText