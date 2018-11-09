
#!/usr/bin/env python3
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import numpy as np
import ImageOperations
import matplotlib.pyplot as plt
from tkinter import colorchooser
import colorsys
from tkinter import filedialog
import sys
import webbrowser
import cv2

class Application():

    def __init__(self, main):

        # main
        self.root = main
        self.root.title("Image Editor")
        self.root.configure()

        # canvas frame
        self.frame_canvas =Frame(self.root,)
        self.canvas = Canvas(self.frame_canvas, width=500, height=200, bg='#ffffff', highlightthickness=0)
        self.loaded = False
        self.scaleZoom = 1.0

        # setup text
        self.canvas_text = self.canvas.create_text(40, 90, anchor="nw", fill='white',)
        self.canvas.itemconfig(self.canvas_text, text="                                     Please load an image...")

        self.i = 0
        self.state = ''
        self.color = 'black'

        # setup side frame
        # the frame on right
        self.frame_side = Frame(self.root, bg='#869bb8', borderwidth=10,relief=RIDGE)
        self.frame_bottom = Frame(self.frame_side, bg='#ffffff', borderwidth=10,relief=FLAT)
        self.frame_right = Frame(self.root, borderwidth=10, relief=FLAT,)
        # toolbar1 frame
        self.frame_top = Frame(self.root,borderwidth=1,relief=RIDGE)
        #toolbar2 frame
        self.frame_left = Frame(self.root,bg = '#869bb8',borderwidth=10, relief=RIDGE)
        self.frame_subleft = Frame(self.frame_left, bg='#ffffff', borderwidth=1,relief=FLAT)
        self.frame_subleft1 = Frame(self.frame_left, bg='#ffffff', borderwidth=1,relief=FLAT)
        # setup info label in frame_side
        self.label1 = Label(self.frame_side, text='Image info:', bg='#ffffff', fg='#2d65d9', anchor=W)
        self.label2 = Label(self.frame_side, text='no image', bg='#ffffff', fg='#2d65d9', borderwidth=10, anchor=W,
                            justify=LEFT)
        self.label3 = Label(self.frame_side, text='Applied effects:', bg='#ffffff', fg='#2d65d9', anchor=W)

        #setup sidetop frame
        self.button1 =  Button(self.frame_top,text='load',fg='white',relief=FLAT,command=self.load_image)
        load = ImageTk.PhotoImage(file="./icon/load.png")
        self.button1.config(image=load)
        self.button1.image=load

        self.button2= Button(self.frame_top,text='save',fg='white',relief=FLAT,command=self.save_image)
        save = ImageTk.PhotoImage(file="./icon/save.png")
        self.button2.config(image=save,state=DISABLED)
        self.button2.image=save

        self.button3 = Button(self.frame_top, text='Undo', fg='white',relief=FLAT,command=self.undo_history)
        undo = ImageTk.PhotoImage(file="./icon/undo.png")
        self.button3.config(image=undo,state=DISABLED)
        self.button3.image = undo

        self.separator1 = ttk.Separator(self.frame_top,orient='vertical')

        self.button4 = Button(self.frame_top, text='Inverse', fg='white',relief=FLAT,command=self.exit)
        quit = ImageTk.PhotoImage(file="./icon/quit.png")
        self.button4.config(image=quit)
        self.button4.image=quit

        self.button5 = Button(self.frame_top, text='GrayScale', fg='white',relief=FLAT,command=self.info)
        info = ImageTk.PhotoImage(file="./icon/aboutus.png")
        self.button5.config(image=info,)
        self.button5.image=info

        self.button6 = Button(self.frame_top, text='light', fg='white',relief=FLAT,command=self.mannual)
        mannual = ImageTk.PhotoImage(file="./icon/mannual.png")
        self.button6.config(image=mannual)
        self.button6.image=mannual

        self.separator2 = ttk.Separator(self.frame_top, orient='vertical')

        self.button7 = Button(self.frame_top, text='crop', fg='white',relief=FLAT,command=self.CropAndZoom)
        crop1 = ImageTk.PhotoImage(file="./icon/crop.png")
        self.button7.config(image=crop1,state=DISABLED)
        self.button7.image=crop1

        self.button8 = Button(self.frame_top, text='light', fg='white',relief=FLAT,command=self.twitter)
        twitter = ImageTk.PhotoImage(file="./icon/twitter.png")
        self.button8.config(image=twitter,state=DISABLED)
        self.button8.image=twitter

        #setup sideleft frame
        #subleft
        self.button9 = Button(self.frame_subleft1, text='yourname', bg='#ffffff',fg='white',relief=FLAT,command=self.skyRegion1)
        yourname = ImageTk.PhotoImage(file="./icon/yourname.png")
        self.button9.config(image=yourname)
        self.button9.image=yourname

        self.button11 = Button(self.frame_subleft, text='scale', bg='#ffffff',fg='white',relief=FLAT,command=self.CropAndZoom)
        scale = ImageTk.PhotoImage(file="./icon/scale.png")
        self.button11.config(image=scale)
        self.button11.image=scale

        self.button13 = Button(self.frame_subleft, text='pen', bg='#ffffff',fg='white',relief=FLAT, command=self.pan)
        pen = ImageTk.PhotoImage(file="./icon/pen.png")
        self.button13.config(image=pen)
        self.button13.image=pen

        self.button16 = Button(self.frame_subleft, text='grayscale', bg='#ffffff',fg='white',relief=FLAT,command=self.grayscale)
        GrayScale1 = ImageTk.PhotoImage(file="./icon/GrayScale.png")
        self.button16.config(image=GrayScale1)
        self.button16.image=GrayScale1

        self.button17 = Button(self.frame_subleft, text='brightness', bg='#ffffff',fg='white',relief=FLAT,command=self.brightness)
        brightness = ImageTk.PhotoImage(file="./icon/light.png")
        self.button17.config(image=brightness)
        self.button17.image=brightness

        self.button19 = Button(self.frame_subleft, text='emboss_weak', bg='#ffffff',fg='white',relief=FLAT,command=self.emboss_weak)
        weak_emboss1 = ImageTk.PhotoImage(file="./icon/emboss1.png")
        self.button19.config(image=weak_emboss1)
        self.button19.image=weak_emboss1

        self.button21 = Button(self.frame_subleft, text='sharpen_c', bg='#ffffff',fg='white',relief=FLAT,command=self.sharpen_c)
        sharp = ImageTk.PhotoImage(file="./icon/sharp.png")
        self.button21.config(image=sharp)
        self.button21.image=sharp

        self.button22 = Button(self.frame_subleft, text='straight',bg='#ffffff',fg='white',relief=FLAT,command=self.draw_line)
        straight = ImageTk.PhotoImage(file="./icon/straight.png")
        self.button22.config(image=straight)
        self.button22.image=straight

        self.button23 = Button(self.frame_subleft, text='arc',bg='#ffffff',fg='white',relief=FLAT,command=self.draw_arc)
        arc = ImageTk.PhotoImage(file="./icon/arc.png")
        self.button23.config(image=arc)
        self.button23.image=arc

        self.button26 = Button(self.frame_subleft, text='arc',bg='#ffffff',fg='white',relief=FLAT,command=self.facebook)
        facebook = ImageTk.PhotoImage(file="./icon/facebook.png")
        self.button26.config(image=facebook)
        self.button26.image=facebook

        self.button27 = Button(self.frame_subleft, text='arc',bg='#ffffff',fg='white',relief=FLAT,command=self.ins)
        ins = ImageTk.PhotoImage(file="./icon/ins.png")
        self.button27.config(image=ins)
        self.button27.image=ins

        #subleft1
        self.button10 = Button(self.frame_subleft1, text='color', bg='#ffffff',fg='white',relief=FLAT,command=self.chooseColor)
        color = ImageTk.PhotoImage(file="./icon/color.png")
        self.button10.config(image=color)
        self.button10.image=color


        self.button12 = Button(self.frame_subleft1, text='crop', bg='#ffffff',fg='white',relief=FLAT,command=self.CropAndZoom)
        crop = ImageTk.PhotoImage(file="./icon/crop.png")
        self.button12.config(image=crop)
        self.button12.image=crop

        self.button14 = Button(self.frame_subleft1, text='rotate_90', bg='#ffffff',fg='white',relief=FLAT,command=self.rotate_90)
        rotate_90 = ImageTk.PhotoImage(file="./icon/rotate.png")
        self.button14.config(image=rotate_90)
        self.button14.image=rotate_90

        self.button15 = Button(self.frame_subleft1, text='inverse', bg='#ffffff',fg='white',relief=FLAT,command=self.inverse)
        inverse1 = ImageTk.PhotoImage(file="./icon/inverse.png")
        self.button15.config(image=inverse1)
        self.button15.image=inverse1

        self.button18 = Button(self.frame_subleft1, text='emboss_strong', bg='#ffffff',fg='white',relief=FLAT,command=self.emboss_strong)
        strong_emboss1 = ImageTk.PhotoImage(file="./icon/emboss.png")
        self.button18.config(image=strong_emboss1)
        self.button18.image=strong_emboss1

        self.button20 = Button(self.frame_subleft1, text='motion_blur', bg='#ffffff',fg='white',relief=FLAT,command=self.motion_blur)
        motion_blur = ImageTk.PhotoImage(file="./icon/motionblur.png")
        self.button20.config(image=motion_blur)
        self.button20.image=motion_blur

        self.button24 = Button(self.frame_subleft1, text='circle', bg='#ffffff',fg='white',relief=FLAT,command=self.draw_oval)
        circle = ImageTk.PhotoImage(file="./icon/circle.png")
        self.button24.config(image=circle)
        self.button24.image=circle

        self.button25 = Button(self.frame_subleft1, text='rectangle', bg='#ffffff',fg='white',relief=FLAT,command=self.draw_rectangle)
        rectangle = ImageTk.PhotoImage(file="./icon/retangle.png")
        self.button25.config(image=rectangle)
        self.button25.image=rectangle

        self.button28 = Button(self.frame_subleft1, text='wechat', bg='#ffffff',fg='white',relief=FLAT,command=self.wechat)
        wechat = ImageTk.PhotoImage(file="./icon/wechat.png")
        self.button28.config(image=wechat)
        self.button28.image=wechat

        self.button29 = Button(self.frame_subleft1, text='weibo', bg='#ffffff',fg='white',relief=FLAT,command=self.weibo)
        weibo = ImageTk.PhotoImage(file="./icon/weibo.png")
        self.button29.config(image=weibo)
        self.button29.image=weibo

        self.button30 = Button(self.frame_subleft, text='humanRecognition', bg='#ffffff',fg='white',relief=FLAT,command=self.humanRecognition)
        humanRecognition = ImageTk.PhotoImage(file="./icon/humanRecognition.png")
        self.button30.config(image=humanRecognition)
        self.button30.image=humanRecognition

        # setup listbox
        self.listbox = Listbox(self.frame_bottom, relief=FLAT, bg='#869bb8', fg='#ffffff', borderwidth=10, \
                               selectborderwidth=0, selectbackground='#ffffff', selectforeground='#1296db',
                               highlightthickness=0)

        # setup scroll
        self.scrollbar = Scrollbar(self.frame_bottom, bg='#1296db', relief=FLAT)

        self.h = Scale(self.frame_right, from_=255, to=0,orient=HORIZONTAL,command=self.update)
        self.h.pack(side=BOTTOM,padx=2,pady=2)
        hue = Label(self.frame_right,text='Hue')
        hue.pack(side=BOTTOM, padx=2)

        self.l = Scale(self.frame_right, from_=255, to=0,orient=HORIZONTAL,command=self.update)
        self.l.pack(side=BOTTOM, padx=2, pady=2)
        light = Label(self.frame_right, text='Lightness')
        light.pack(side=BOTTOM, padx=2)

        self.s = Scale(self.frame_right, from_=255, to=0, orient=HORIZONTAL,command=self.update)
        self.s.pack(side=BOTTOM, padx=2, pady=2)
        sat = Label(self.frame_right, text='Saturation')
        sat.pack(side=BOTTOM, padx=2)

        self.c = Canvas(self.frame_right, width=100, height=100, bg='Black')
        self.c.pack(side=BOTTOM, padx=2, pady=2)
        self.rgb = Label(self.frame_right, text='RGB(0, 0, 0)')
        self.rgb.pack(side=BOTTOM, padx=2, pady=2)

        '''
        number = "Red: 0    Green:0     Blue:0"
        red = 0
        green = 0
        blue = 0
        box = 0
        box1 = 0
        box2 = 0

        #setup the color chooser
        self.blue = Scale(self.frame_right, label ='Blue',variable=blue,bg='#ffffff', fg='white',\
                          length='6c' ,width='.30c',from_=0,to=255,orient=HORIZONTAL,\
                          )
        self.red = Scale(self.frame_right, label ='Red',variable=red,bg='#ffffff', fg='white',\
                          length='6c',width='.30c',from_=0,to=255,orient=HORIZONTAL,\
                          )
        self.green = Scale(self.frame_right, label ='green',variable=green,bg='#ffffff', fg='white',\
                          length='6c',width='.30c',from_=0,to=255,orient=HORIZONTAL,\
                          )

        self.number = Label(self.frame_right,textvariable=number,fg='white',bg='#869bb8')
        '''
        # menu
        self.setup_menu()

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('PNG', '.png'), ('JPG', '.jpg .jpeg'), ('PPM', '.ppm')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.png'
        options['parent'] = root
        options['title'] = 'Choose file:'

    def zoomIn(self):
        # a condicao abaixo e para realizar um zoom gradual, dependendo do nivel de zoom atual
        if self.scaleZoom > 1.5:
            self.scaleZoom += 0.05
        elif self.scaleZoom > 1.3:
            self.scaleZoom += 0.08
        else:
            self.scaleZoom += 0.1

        self.imgArrayAux = self.imgArray.resize(
            (int(self.imgOrig.width() * self.scaleZoom), int(self.imgOrig.height() * self.scaleZoom)),
            Image.ANTIALIAS)  # redimensiona a imagem

        # o codigo abaixo e responsavel por exibir a nova imagem redimensionada
        self.img = ImageTk.PhotoImage(self.imgArrayAux)
        self.mainImg.configure(image=self.img)
        self.frame.configure(width=int(self.imgOrig.width() * self.scaleZoom),
                             height=int(self.imgOrig.height() * self.scaleZoom))
        self.canvas.configure(scrollregion=(
        0, 0, int(self.imgOrig.width() * self.scaleZoom), int(self.imgOrig.height() * self.scaleZoom)))

    def facebook(self):
        sys.path.append("libs")
        url='http://www.facebook.com/'
        webbrowser.open(url)
        print
        webbrowser.get

    def ins(self):
        sys.path.append("libs")
        url='https://www.instagram.com/'
        webbrowser.open(url)
        print
        webbrowser.get

    def wechat(self):
        sys.path.append("libs")
        url='https://web.wechat.com/'
        webbrowser.open(url)
        print
        webbrowser.get

    def twitter(self):
        sys.path.append("libs")
        url='https://twitter.com/'
        webbrowser.open(url)
        print
        webbrowser.get

    def weibo(self):
        sys.path.append("libs")
        url='https://www.weibo.com/'
        webbrowser.open(url)
        print
        webbrowser.get

    def Press(self,event):
        self.i += 1
        self.x = event.x
        self.y = event.y

    def Draw(self,event):
        if self.state == 'pan':
            self.canvas.create_line(self.x, self.y, event.x, event.y, fill=self.color)
            self.x = event.x
            self.y = event.y

        if self.state == 'line':
            if not self.canvas.find_withtag('line' + str(self.i)):
                self.canvas.create_line(self.x, self.y, event.x, event.y, fill=self.color, tags='line' + str(self.i))
            else:
                self.canvas.delete('line' + str(self.i))
                self.canvas.create_line(self.x, self.y, event.x, event.y, fill=self.color, tags='line' + str(self.i))

        if self.state == 'oval':
            if not self.canvas.find_withtag('oval' + str(self.i)):
                self.canvas.create_oval(self.x, self.y, event.x, event.y, outline=self.color, tags='oval' + str(self.i))
            else:
                self.canvas.delete('oval' + str(self.i))
                self.canvas.create_oval(self.x, self.y, event.x, event.y, outline=self.color, tags='oval' + str(self.i))

        if self.state == 'arc':
            if not self.canvas.find_withtag('arc' + str(self.i)):
                self.canvas.create_arc(self.x, self.y, event.x, event.y, tags='line' + str(self.i))
            else:
                self.canvas.delete('arc' + str(self.i))
                self.canvas.create_arc(self.x, self.y, event.x, event.y, start=0, tags='line' + str(self.i))

        if self.state == 'rectangle':
            if not self.canvas.find_withtag('rectangle' + str(self.i)):
                self.canvas.create_rectangle(self.x, self.y, event.x, event.y, outline=self.color,
                                             tags='rectangle' + str(self.i))
            else:
                self.canvas.delete('rectangle' + str(self.i))
                self.canvas.create_rectangle(self.x, self.y, event.x, event.y, outline=self.color,
                                             tags='rectangle' + str(self.i))

    def setStates(self, state):
            self.state = state

    def pan(self):
        self.add_history(self.pillow_image)
        self.setStates("pan")
    def draw_line(self):
        self.add_history(self.pillow_image)
        self.setStates("line")
    def draw_oval(self):
        self.add_history(self.pillow_image)
        self.setStates("oval")
    def draw_arc(self):
        self.add_history(self.pillow_image)
        self.setStates("arc")
    def draw_rectangle(self):
        self.add_history(self.pillow_image)
        self.setStates("rectangle")
    def chooseColor(self):
        r = colorchooser.askcolor()
        self.color = r[1]

    def skyRegion1(self):
        iLow = np.array([100, 43, 46])
        iHigh = np.array([124, 255, 255])
        img = cv2.imread(self.pillow_image)
        imgOri = cv2.imread(self.pillow_image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(img)
        v = cv2.equalizeHist(v)
        hsv = cv2.merge((h, s, v))

        imgThresholded = cv2.inRange(hsv, iLow, iHigh)

        imgThresholded = cv2.medianBlur(imgThresholded, 9);

        kernel = np.ones((5, 5), np.uint8)
        imgThresholded = cv2.morphologyEx(imgThresholded, cv2.MORPH_OPEN, kernel, iterations=10)
        imgThresholded = cv2.medianBlur(imgThresholded, 9)
        pic_name = self.pillow_image.split('/')[-1].split('.')[0]
        tmp = "tmp/" + pic_name + "-mask.jpg"
        print(tmp)
        cv2.imwrite("./image/tmp.jpg", imgThresholded)
        return tmp

    def seamClone(skyname, picname, maskname):
        src = cv2.imread(skyname)
        dst = cv2.imread(picname)

        src_mask = cv2.imread(maskname, 0)
        src_mask0 = cv2.imread(maskname, 0)
        contours = cv2.findContours(src_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]

        x, y, w, h = cv2.boundingRect(cnt)
        print(x, y, w, h)
        if w == 0 or h == 0:
            return dst
        dst_x = len(dst[0])
        dst_y = len(dst[1])
        src_x = len(src[0])
        src_y = len(src[1])
        scale_x = w * 1.0 / src_x
        src = cv2.resize(src, (dshape, dshape), interpolation=cv2.INTER_CUBIC)

        cv2.imwrite("src_sky.jpg", src)
        center = ((x + w) / 2, (y + h) / 2)
        print(center)

        output = cv2.seamlessClone(src, dst, src_mask0, center, cv2.NORMAL_CLONE)

        return output

    def myFilter(orimap, newmap, picname):
        ori = cv2.imread(orimap)
        new = cv2.imread(newmap)
        my = cv2.imread(picname)

        pic_name = picname.split('/')[-1].split('.')[0]
        style_name = newmap.split('/')[-1].split('.')[0]

        tmp = "tmp/" + pic_name + "-" + style_name + ".jpg"

        for i in range(len(my)):
            for j in range(len(my[0])):
                pos = cv2.findNonZero(my[i][j], ori)
                my[i][j] = new[pos[0], pos[1]]

        cv2.imwrite(tmp, my)

        return tmp

    def update(self,*args):
        'color'
        r, g, b = colorsys.hls_to_rgb(self.h.get() / 255.0, self.l.get() / 255.0, self.s.get() / 255.0)
        r, g, b = r * 255, g * 255, b * 255
        self.rgb.configure(text='RGB:(%d, %d, %d)' % (r, g, b))
        self.c.configure(bg='#%02d%02d%02d' % (r, g, b))

    def setup_menu(self):
        self.menubar = Menu(self.root, bg='gray7', fg='white', relief=FLAT)

        #File Menu
        self.submenu1 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="File", menu=self.submenu1)
        self.submenu1.add_command(label="Load image", command=self.load_image)
        self.submenu1.add_command(label="Save image", command=self.save_image)
        self.submenu1.add_separator()
        self.submenu1.add_command(label="Exit", command=self.exit)

        #Edit Menu
        self.submenu2 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Edit", menu=self.submenu2)
        self.submenu2.add_command(label="Undo", command=self.undo_history)
        self.submenu2.add_separator()
        self.submenu2.add_command(label="Inverse", command=self.inverse)
        self.submenu2.add_command(label="Grayscale", command=self.grayscale)
        self.submenu2.add_command(label="Lighten/Darken", command=self.brightness)

        v=IntVar()
        #View Menu
        self.submenu4 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.submenu4.zoom_menu = Menu(self.submenu4, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="View", menu=self.submenu4)
        self.submenu4.add_checkbutton(label="Always on top",variable=v,command=self.alwaysOnTop(v))
        self.submenu4.zoom_menu.add_command(label="Zoom out")
        self.submenu4.zoom_menu.add_command(label="Zoom in")
        self.submenu4.add_cascade(label="Zoom",menu=self.submenu4.zoom_menu)

        #Filters Menu
        self.submenu3 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Filters", menu=self.submenu3)
        self.submenu3.add_command(label="Weak emboss", command=self.emboss_weak)
        self.submenu3.add_command(label="Strong emboss", command=self.emboss_strong)
        self.submenu3.add_command(label="Motion blur", command=self.motion_blur)
        self.submenu3.add_command(label="Sharpen - excessive edges", command=self.sharpen_ee)
        self.submenu3.add_command(label="Sharpen - crisp", command=self.sharpen_c)
        self.submenu3.add_command(label="Sharpen - subtle edges", command=self.sharpen_se)
        self.submenu3.add_command(label="Edge Detection", command=self.edges_detection)

        #color menu
        self.submenu5 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Color", menu=self.submenu5)
        self.submenu5.add_command(label="Color No.",command=self.color)

        self.submenu6 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Setting", menu=self.submenu6)
        self.submenu6.add_command(label="About us",command=self.info)
        self.submenu6.add_command(label = "User Mannual",command=self.mannual)

        #Edit Menu
        self.root.config(menu=self.menubar)
        self.menubar.entryconfig("Edit", state=DISABLED)
        self.menubar.entryconfig("Filters", state=DISABLED)
        self.submenu1.entryconfig("Save image", state=DISABLED)
        self.submenu2.entryconfig("Undo", state=DISABLED)
        self.submenu4.entryconfig("Zoom", state=DISABLED)

    def color(self):
        colorbox = colorchooser.askcolor()
        print(colorbox)

    #setuo the menu function depend on whether import a photo.
    def menu_enable(self):
        if self.loaded == False:
            self.canvas.delete(self.canvas_text)

        if self.mode == "L" or self.mode == "P" or self.mode == "RGB" or self.mode == "RGBA":
            self.menubar.entryconfig("Edit", state=NORMAL)
            self.submenu1.entryconfig("Save image", state=NORMAL)
            self.menubar.entryconfig("Filters", state=NORMAL)
            self.submenu4.entryconfig("Zoom", state=NORMAL)
        else:
            self.menubar.entryconfig("Edit", state=DISABLED)
            self.menubar.entryconfig("Filters", state=DISABLED)
            self.submenu4.entryconfig("Zoom",state=DISABLED)
        if self.mode == "L" or self.mode == "P":
            self.submenu2.entryconfig("Grayscale", state=DISABLED)
        else:
            self.submenu2.entryconfig("Grayscale", state=NORMAL)




    #setup the button depend on whether import a photo
    def button_enable(self):
        if self.loaded == False:
            self.canvas.delete(self.canvas_text)
        if self.mode == "L" or self.mode == "P" or self.mode == "RGB" or self.mode == "RGBA":
            self.button2.config(state=NORMAL)
            self.button3.config(state=NORMAL)
            self.button4.config(state=NORMAL)
            self.button5.config(state=NORMAL)
            self.button6.config(state=NORMAL)
            self.button7.config(state=NORMAL)
            self.button8.config(state=NORMAL)
        else:
            self.button2.config(state=DISABLED)
            self.button3.config(state=DISABLED)
            self.button4.config(state=DISABLED)
            self.button5.config(state=DISABLED)
            self.button6.config(state=DISABLED)
            self.button7.config(state=DISABLED)
            self.button8.config(state=DISABLED)
    #save image and info
    def save_main_image(self, directory):
        try:
            self.pillow_image.save(directory)
        except:
            showerror("Saving image", "Can't save this image as\n{}".format(directory))
        self.canvas.update()

    #pack the UI
    def run_application(self):
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT,padx=2)
        self.button3.pack(side=LEFT,padx=2)
        #self.separator1.update()
        self.separator1.pack(side=LEFT,anchor="n",fill=Y, pady = 7, padx=7)
        self.button4.pack(side=LEFT,padx=2)
        self.button5.pack(side=LEFT,padx=2)
        self.button6.pack(side=LEFT,padx=2)
        self.separator2.pack(side=LEFT,anchor="n",fill=Y, pady = 7, padx=7)
        self.button7.pack(side=LEFT,padx=2)
        self.button8.pack(side=LEFT,padx=2)
        self.canvas.update()
        self.canvas.pack(side=LEFT,pady=10,padx=10)
        self.canvas.bind('<Button-1>', self.Press)
        self.canvas.bind('<B1-Motion>', self.Draw)
        self.label1.pack(fill=X)
        self.label2.pack(fill=X)
        self.label3.pack(fill=X)
        self.listbox.pack(expand=1, fill=Y, side=LEFT)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.listbox.yview)

        self.frame_top.update()
        self.frame_top.pack(expand=1,side=TOP,fill=X)

        self.frame_left.update()
        self.frame_subleft.update()
        self.frame_subleft1.update()
        self.frame_left.pack(expand=1, side=LEFT,fill=BOTH,padx=20,pady=20)
        self.frame_subleft.pack(expand=1, side=LEFT,fill=BOTH)
        self.frame_subleft1.pack(expand=1, side=LEFT,fill=BOTH)


        self.button11.pack()
        self.button30.pack()
        self.button16.pack()
        self.button17.pack()
        self.button19.pack()
        self.button21.pack()
        self.button13.pack()
        self.button22.pack()
        self.button23.pack()
        self.button26.pack()
        self.button27.pack()

        self.button12.pack()
        self.button14.pack()
        self.button15.pack()
        self.button18.pack()
        self.button20.pack()
        self.button9.pack()
        self.button10.pack()
        self.button24.pack()
        self.button25.pack()
        self.button28.pack()
        self.button29.pack()

        self.frame_canvas.update()
        self.frame_canvas.pack(expand=1,side=LEFT,fill=BOTH,)

        self.frame_bottom.update()
        self.frame_bottom.pack(expand=1, side=BOTTOM,fill=BOTH)

        self.frame_side.update()
        self.frame_side.pack(expand=1, side=LEFT,pady=20,padx=20,fill=BOTH)

        self.frame_right.update()
        self.frame_right.pack(side=RIGHT,anchor=NW,fill=Y,pady=60)

        '''
        self.number.pack(side=BOTTOM,padx=2,pady=2)
        self.blue.pack(side=BOTTOM,padx=2,pady=2)
        self.green.pack(side=BOTTOM,padx=2,pady=2)
        self.red.pack(side=BOTTOM,padx=2,pady=2)
        '''

    # the function that keep the windows on top
    def alwaysOnTop(self,variable):
        if variable.get() is 1:
            Popup = Toplevel(root)
            Popup.attributes("-topmost",1)

    def info(self):
        var = messagebox.showinfo("About Us","This is YuLynn Lee 's final project\n\
        Software engineering\n\
        YuLynn Lee\n\
        1409853G-I011-0074")
    #Returns an opened file in read mode

    def mannual(self):
        var1 = messagebox.showinfo("User Mannual","1.as you can se, all the buttons can be used.\n2.The button below the menu is the tool key such as import save...\n3.The button on the left is the function of filter, crop ...\n4.The button on the right is a quick look for u to find color")
    def load_image(self, directory=None):
        if directory is None:
            directory = askopenfile(mode='r', **self.file_opt)
            if directory is None:
                return
            else:
                directory = directory.name

        try:
            self.load_main_image(directory)
            self.menu_enable()
            self.button_enable()
            self.loaded = True
        except:
            showerror("Opening image", "Can't open this image...")

        self.canvas.update()
        self.frame_side.update()

    def scrollcolor(self,val):
        global red,green,blue
        global redno,greenno,blueno,number,board
        global box,box1,box2,ten,zero
        #redno[format]=

    def save_image(self, directory=None):
        if directory is None:
            directory = asksaveasfile(mode='w', **self.file_opt)
            if directory is None:
                return
            else:
                directory = directory.name

        self.save_main_image(directory)
        self.image_loaded = False

    def load_main_image(self, directory):
        # add image and info
        self.pillow_image, self.pillow_preview_image, self.np_image, info, self.info_raw = ImageOperations.load_image(
            directory)

        try:
            self.canvas.delete(self.main_image)
        except:
            pass

        width, height = self.pillow_preview_image.size
        self.mode = self.pillow_image.mode
        self.data = ImageTk.PhotoImage(self.pillow_preview_image)
        self.main_image = self.canvas.create_image(0, 0, image=self.data, anchor=NW)
        self.canvas.config(width=width, height=height, bg='white')
        self.label2.config(text=info)
        self.listbox.delete(0, END)

        # history
        self.history = []
    #update the image info to the image editor
    def update_app(self):
        self.data = ImageTk.PhotoImage(self.pillow_preview_image)
        width, height = self.pillow_preview_image.size

        self.canvas.config(width=width, height=height, bg='white')
        self.canvas.itemconfig(self.main_image, image=self.data, anchor=NW)

        self.canvas.update()
        self.frame_side.update()

    def add_list(self, value):
        self.listbox.insert(END, value)
        self.listbox.yview(END)

    def remove_list(self):
        self.listbox.delete(END)

    def update_info(self):
        info, self.info_raw = ImageOperations.update_size_info(self.pillow_image, self.info_raw)
        self.label2.config(text=info)

    def add_history(self, pic):
        self.history.append(pic)
        self.submenu2.entryconfig("Undo", state=NORMAL)

    def undo_history(self):
        try:
            pic = self.history[-1]
            del self.history[-1]
        except:
            return

        try:
            self.history[-1]
        except:
            self.submenu2.entryconfig("Undo", state=DISABLED)

        self.pillow_image, self.pillow_preview_image, self.np_image = ImageOperations.update_image(pic, self.info_raw)
        self.update_info()
        self.remove_list()
        self.update_app()


    def exit(self):
        quit()

    # APPLYING FILTERS
    def rotate_90(self):
        self.apply_effect(ImageOperations.rotate_90,"rotate_90")

    def erosion(self):
        self.apply_effect(ImageOperations.erosion, "erosion")
    #the inverse
    def inverse(self):
        self.apply_effect(ImageOperations.inverse, "inverse")
    #grayscake & it only used in the colorful image
    def grayscale(self):
        if self.mode == 'RGB' or self.mode == 'RGBA':
            self.apply_effect(ImageOperations.grayscale, "grayscale")

    # MINI WINDOW BRIGHTNESS GUI ------
    def brightness(self):
        # setup preview
        self.br_window = Toplevel(bg='gray7')
        self.br_window.title("Brightness")
        self.br_window.resizable(width=False, height=False)

        self.br_frame = Frame(self.br_window, bg='gray7', borderwidth=10)

        self.slider = Scale(self.br_window, from_=-100, to=400, bg='gray7', fg='white', \
                            troughcolor='gray7', orient=HORIZONTAL, \
                            command=self.schedule_preview, highlightthickness=0)
        self.apply_button = Button(self.br_frame, text="Apply", bg='gray7', fg='white', \
                                   command=self.apply_brightness, highlightthickness=0)

        # adjust preview
        self.br_preview, self.br_np_image = ImageOperations.get_miniature(self.pillow_image)
        self.br_np_original = self.br_np_image
        width, height = self.br_preview.size
        self.br_canvas = Canvas(self.br_window, width=width, height=height, bg='white', highlightthickness=0)
        self.br_data = ImageTk.PhotoImage(self.br_preview)
        self.br_preview_image = self.br_canvas.create_image(0, 0, image=self.br_data, anchor=NW)

        self._job = None
        self.br_canvas.pack(fill=BOTH)
        self.slider.pack(fill=BOTH)
        self.apply_button.pack(side=LEFT)
        self.br_frame.update()
        self.br_frame.pack(expand=1, fill=BOTH)
    """
    def zoom_image(self):
        self.zm_window = Toplevel(bg='gray7')
        self.zm_window.title("Zoom")
        self.zm_window.resizable(width=False, height=False)

        self.zm_frame = Frame(self.zm_window, bg='gray7', borderwidth=10)
        self.slider1 = Scale(self.zm_window, from_=0, to=200, bg='gray7', fg='white', \
                            troughcolor='gray7', orient=HORIZONTAL, \
                            command=self.schedule_preview, highlightthickness=0)
        self.apply_button = Button(self.zm_frame, text="Apply", bg='gray7', fg='white', \
                                   command=self.apply_zoom(), highlightthickness=0)

        #adjust preview
        self.zm_preview, self.zm_np_image = ImageOperations.get_miniature(self.pillow_image)
        self.zm_np_original = self.zm_np_image
        width, height = self.zm_preview.size
        self.zm_canvas = Canvas(self.zm_window,width=width,height=height,bg='white',highlightthickness=0)
        self.zm_data = ImageTk.PhotoImage(self.zm_preview)
        self.zm_preview_image = self.zm_canvas.create_image(0,0,image = self.zm_data,anchor=NW)

        self._job = None
        self.zm_canvas.pack(fill=BOTH)
        self.slider1.pack(fill=BOTH)
        self.apply_button.pack(side=LEFT)
        self.zm_frame.update()
        self.zm_frame.pack(expand=1,fill=BOTH)
    """

    def CropAndZoom(self):
        img = self.pillow_image  # 打开图像
        plt.figure("CropAndZoom")
        plt.subplot(1, 1, 1), plt.title('Image')
        plt.imshow(img), plt.axis('off')
        plt.show()


    def schedule_preview(self, event):
        if self._job:
            self.root.after_cancel(self._job)
        self._job = self.root.after(300, self.apply_preview)
    #brightness
    def apply_preview(self):
        self._job = None
        value = self.slider.get()
        self.br_preview, _, self.br_np_image = ImageOperations.brightness(self.br_np_original, self.mode, value)
        self.br_data = ImageTk.PhotoImage(self.br_preview)
        self.br_canvas.itemconfig(self.br_preview_image, image=self.br_data)
        self.br_canvas.update()
    #zoom
    """
    def apply_preview1(self):
        self._job = None
        value = self.slider1.get()
        self.zm_preview, _, self.zm_np_image = ImageOperations.zoom(self.zm_np_original, self.mode, value)
        self.zm_data = ImageTk.PhotoImage(self.zm_preview)
        self.zm_canvas.itemconfig(self.zm_preview_image, image=self.zm_data)
        self.zm_canvas.update()
    """
    def apply_brightness(self):
        self.add_history(self.pillow_image)
        value = self.slider.get()
        self.br_window.destroy()
        self.pillow_image, self.pillow_preview_image, self.np_image = ImageOperations.brightness(self.np_image,
                                                                                                 self.mode, value)
        self.add_list("brightness")
        self.update_app()

    """
    def apply_zoom(self):
        self.add_history(self.pillow_image)
        value = self.slider1.get()
        self.zm_window.destroy()
        self.pillow_image, self.pillow_preview_image, self.np_image = ImageOperations.zoom(self.np_image,self.mode, value)
        self.add_list("Zoom")
        self.update_app()
    """

    def edges_detection(self):
        self.apply_effect(ImageOperations.edges_detection, "edges detection")

    def emboss_weak(self):
        self.apply_effect(ImageOperations.emboss_weak, "weak emboss")

    def emboss_strong(self):
        self.apply_effect(ImageOperations.emboss_strong, "strong emboss")

    def motion_blur(self):
        self.apply_effect(ImageOperations.motion_blur, "motion blur")

    def sharpen_ee(self):
        self.apply_effect(ImageOperations.sharpen_ee, "sharpen - edges excessively")

    def sharpen_c(self):
        self.apply_effect(ImageOperations.sharpen_c, "sharpen - crisp")

    def sharpen_se(self):
        self.apply_effect(ImageOperations.sharpen_se, "sharpen - subtle edges")

    #apply the image effect
    def apply_effect(self, function, name):
        self.add_history(self.pillow_image)
        self.pillow_image, self.pillow_preview_image, self.np_image = function(self.np_image, self.mode)
        self.add_list(name)
        self.update_info()
        self.update_app()
    '''
    class History(object):
        def __init__(self):
            self.l = ['']
            self.i = 0
        def next(self):
            if self.i ==len(self.i):
                return None
            self.i +=1
            return self.l[self.i]
        def prev(self):
            if self.i ==0:
                return None
            self.i -= 1
            return self.l[self.i]
        def add(self,s):
            del self.l[self.i+1]
            self.l.append(s)
            self.i +=1
        def current(self):
            return self.l[self.i]
    '''
    def humanRecognition(self):
        color = (0, 255, 0)
        cv_image = self.np_image[:, :, ::-1].copy()
        grey = cv2.cvtColor(cv_image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        classfier = cv2.CascadeClassifier("G:\opencv\sources\data\haarcascades\haarcascade_frontalface_alt2.xml")
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # >0 can detect the face
            for faceRect in faceRects:  # mark the face
                x, y, w, h = faceRect
                cv2.rectangle(cv_image, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 3)  # control the thickness of the frame
        cv2.imwrite('./icon/image/2.jpg', cv_image)
        self.update_info()
        self.update_app()
    '''
    def send_mail(self,var):
        # smtp server of qq
        host_server = 'smtp.qq.com'
        # sender_qq id
        sender_qq = '441535867'
        # password
        pwd = 'glrcaediszepbgbc'
        # 发件人的邮箱
        sender_qq_mail = '441535867@qq.com'
        # 收件人邮箱
        receiver = '441535867@qq.com'
        # 邮件的正文内容
        mail_content = self.pillow_image
        # 邮件标题
        mail_title = ' The mail from ImageEditor'

        # ssl登录
        smtp = SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()
    '''

root = Tk()
root.resizable(width=False, height=False)
app = Application(root)
app.run_application()

root.mainloop()