
from PIL import Image, ImageTk
import numpy as np
import cv2

def skyRegion1(picname):
    iLow = np.array([100,43,46])
    iHigh = np.array([124,255,255])
    img = cv2.imread(picname)
    imgOri = cv2.imread(picname)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h,s,v = cv2.split(img)
    v = cv2.equalizeHist(v)
    hsv = cv2.merge((h,s,v))

    imgThresholded = cv2.inRange(hsv,iLow,iHigh)

    imgThresholded = cv2.medianBlur(imgThresholded,9);

    kernel = np.ones((5,5),np.uint8)
    imgThresholded = cv2.morphologyEx(imgThresholded,cv2.MORPH_OPEN,kernel,iterations=10)
    imgThresholded = cv2.medianBlur(imgThresholded,9)
    pic_name = picname.split('/')[-1].split('.')[0]
    tmp = "tmp/" + pic_name + "-mask.jpg"
    print (tmp)
    cv2.imwrite("./image/tmp.jpg",imgThresholded)
    return tmp

def seamClone(skyname,picname,maskname):
    src = cv2.imread(skyname)
    dst = cv2.imread(picname)

    src_mask = cv2.imread(maskname,0)
    src_mask0 = cv2.imread(maskname,0)
    contours = cv2.findContours(src_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]

    x,y,w,h = cv2.boundingRect(cnt)
    print (x,y,w,h)
    if w==0 or h==0:
        return dst
    dst_x = len(dst[0])
    dst_y = len(dst[1])
    src_x = len(src[0])
    src_y = len(src[1])
    scale_x = w*1.0/src_x
    src = cv2.resize(src,(dshape,dshape),interpolation=cv2.INTER_CUBIC)

    cv2.imwrite("src_sky.jpg",src)
    center = ((x+w)/2,(y+h)/2)
    print (center)

    output = cv2.seamlessClone(src,dst,src_mask0,center,cv2.NORMAL_CLONE)

    return output

def myFilter(orimap,newmap,picname):
    ori = cv2.imread(orimap)
    new = cv2.imread(newmap)
    my = cv2.imread(picname)

    pic_name = picname.split('/')[-1].split('.')[0]
    style_name = newmap.split('/')[-1].split('.')[0]

    tmp = "tmp/" + pic_name + "-" + style_name + ".jpg"

    for i in range(len(my)):
        for j in range(len(my[0])):
            pos = cv2.findNonZero(my[i][j],ori)
            my[i][j] = new[pos[0],pos[1]]

    cv2.imwrite(tmp,my)

    return tmp
