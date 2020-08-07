from imutils.object_detection import non_max_suppression
import numpy as np
import time
import pytesseract
import cv2
from PIL import ImageFont, ImageDraw, ImageEnhance
import PIL
from wand.image import Image
from wand.color import Color
from EndPoint import PDFiles
import pickle
import os
from EndPoint.DifferintalPrivacy import DifferintialPrivacy as DiffPrv

#################################################################################################
##                                                                                             ##
##                                      FIN                                                    ##
##                                                                                             ##
#################################################################################################

class remove:
    
    def __init__(self):
        
        self.__lang_pack = np.load(os.getcwd()+"/EndPoint/assets/pack/lang_pack.npy",allow_pickle='TRUE').item()
        self.__layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"
            ]
        # load the pre-trained EAST text detector
        self.__net = cv2.cv2.dnn.readNet(os.getcwd()+"/EndPoint/assets/pack/EAST.pb")


    # match every string in the picture with the deletaion list or set if it exist so cover the block with a 
    # black rectangle

    def __reformat(self, file):

        fi = open(file,"r+",encoding='UTF-8')
        ToWrite = ""
        for line in fi.readlines():
            ls = line.strip()
            if len(ls)==0:
                continue
            tp = ""
            if line.find('.') :
                for i in range(0, len(line)):
                    if line[i] == ' ' and i > 0 and line[i-1] == '.':
                        continue
                    tp += line[i]
                ToWrite += tp

        fi.close()
        fi = open(file,"w+",encoding = "UTF-8")
        fi.writelines(ToWrite)
        fi.close()



    def __RemoveFromImages(self,countPic , lang):
        
        diffrintial = DiffPrv()
        for i in range(countPic):
            # load the input image and grab the image dimensions
            image = cv2.cv2.imread(os.getcwd()+"/EndPoint/data/HighRes"+str(i)+".jpg")
            (H, W) = image.shape[:2]
            # construct a blob from the image and then perform a forward pass of
            # the model to obtain the two output layer sets
            blob = cv2.cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                        (123.68, 116.78, 103.94), swapRB=True, crop=False)
            self.__net.setInput(blob)
            (scores, geometry) = self.__net.forward(self.__layerNames)
            # grab the number of rows and columns from the scores volume, then
            # initialize our set of bounding box rectangles and corresponding
            # confidence scores
            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []
            for y in range(0, numRows):
                # extract the scores (probabilities), followed by the geometrical
                # data used to derive potential bounding box coordinates that
                # surround text
                scoresData = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]
                # loop over the number of columns
                for x in range(0, numCols):
                    # if our score does not have sufficient probability, ignore it
                    if scoresData[x] < 0.001:
                        continue
                    # compute the offset factor as our resulting feature maps will
                    # be 4x smaller than the input image
                    (offsetX, offsetY) = (x * 4.0, y * 4.0)
                    # extract the rotation angle for the prediction and then
                    # compute the sin and cosine
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)
                    # use the geometry volume to derive the width and height of
                    # the bounding box
                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]
                    # compute both the starting and ending (x, y)-coordinates for
                    # the text prediction bounding box
                    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                    startX = int(endX - w)
                    startY = int(endY - h)
                    # add the bounding box coordinates and probability score to
                    # our respective lists
                    rects.append((startX, startY, endX, endY))
                    confidences.append(scoresData[x])
            # apply non-maxima suppression to suppress weak, overlapping bounding boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)
            fordel =[]
            forrep =[]
            tobeAnswer =[]
            DelLst = pickle.load(open(os.getcwd()+"/EndPoint/data/dellstpic"+str(i)+".p","rb"))
            # loop over the bounding boxes
            for (startX, startY, endX, endY) in boxes:
                # scale the bounding box coordinates based on the respective ratios
                # cv2.cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
                p = image
                # crop the image 
                p  = p[startY-1:endY+1,startX-1:endX+1]
                cv2.cv2.imwrite(os.getcwd()+"/EndPoint/data/anything.jpg",p)
                del p
                with Image(filename=os.getcwd()+"/EndPoint/data/anything.jpg" ,resolution= 300) as HiImg:
                            #change the background color to white
                            HiImg.background_color = Color('white')
                            #remove the alpha channel -> RGBA to RGB
                            HiImg.alpha_channel = 'remove'
                            #save the image
                            HiImg.save(filename=os.getcwd()+"/EndPoint/data/HighRes.jpg")
                            temp = cv2.cv2.imread(os.getcwd()+"/EndPoint/data/HighRes.jpg")
                            string = pytesseract.image_to_string(temp,lang)
                            del temp
                            from EndPoint.NLPModule import NLPModule
                            Correct = NLPModule(language = "null")
                            string = Correct.findMinDistance(i,string)

                            if string in DelLst :
                                fordel.append((startX,startY,endX,endY))
                                continue
                            if string.isnumeric():
                                forrep.append((startX,startY,endX,endY))
                                tobeAnswer.append(string)
            for (startx,starty,endx,endy) in fordel:
                image[starty-1:endy+1,startx-1:endx+1]=1
            #show the output image
            #cv2.cv2.imshow("Text Detection", image)
            #cv2.cv2.waitKey(0)
            cv2.cv2.imwrite(os.getcwd()+"/EndPoint/data/CleanPic"+str(i)+".jpg",image)
            del image
            image = PIL.Image.open(os.getcwd()+"/EndPoint/data/CleanPic"+str(i)+".jpg")
            draw = ImageDraw.Draw(image)
            for (startx,starty,endx,endy) in forrep:
                temp = [float(tobeAnswer.pop(0))]
                temp = np.array(temp).reshape(1,-1) 
                draw.rectangle(((startx,starty),(endx,endy)),fill="white")
                draw.text((startX+1,startY),"".join(str(diffrintial.answer(temp)[0])))
            image = image.save(os.getcwd()+"/EndPoint/data/CleanPic"+str(i)+".jpg")

    def __RemoveFromFiles(self,countText):
        
        diffrintial = DiffPrv()
        
        for i in range(countText):
            DelLst = pickle.load(open(os.getcwd()+"/EndPoint/data/dellsttxt"+str(i)+".p","rb"))
            self.__reformat(str(os.getcwd()+"/EndPoint/data/Text"+str(i)+".txt"))
            Rfi = open(os.getcwd()+"/EndPoint/data/Text"+str(i)+".txt","r+",encoding='UTF-8')
            Wfi = open(os.getcwd()+"/EndPoint/data/CleanText"+str(i)+".txt","w+",encoding='UTF-8')
            for line in Rfi :
                Wline = ""
                for word in line.split() :
                    if word in DelLst:
                        continue
                    if word.isnumeric():
                        temp = [float(word)]
                        temp = np.array(temp).reshape(1,-1)
                        word = "".join(str(diffrintial.answer(temp)[0])) 
                    Wline = Wline + word + " " 
                Wfi.write(Wline+'\n')
            Rfi.close()
            Wfi.close()

    
    # setting the passing language to a prefex
    def __set_lang(self,lang):
        if lang in self.__lang_pack.keys():
            return self.__lang_pack[lang]
        else :
            print ("cannot find language the language will set to the default english")
            lang = "eng"
        return lang


    def RemoveFromData(self,countPicture,countText , lang):
        lang = self.__set_lang(lang)
        if countPicture > 0:
            self.__RemoveFromImages(countPicture,lang)
        if countText > 0:
            self.__RemoveFromFiles(countText)
        makepdf = PDFiles.makePDF()
        del self.__net
        makepdf.MakePdf(countPicture,countText)