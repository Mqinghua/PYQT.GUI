#!/usr/bin/python
#coding:utf-8

import sys
import os
from PyQt4.QtGui import QWidget, QPalette, QPixmap, QLabel, QApplication, QBrush, QHBoxLayout, QVBoxLayout, \
    QDesktopWidget, QPushButton, QLineEdit, QIcon, QFont,QFileDialog,QDialog,QFormLayout,QDesktopWidget,QTextEdit
#from PyQt4.QtCore import Qt,QDir,SIGNAL,QThread,pyqtSignal
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
#from example_ui import *

class Application(QWidget):
    leftSide = 1
    rightSide = 0
    btncontrol = None
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #self.setupUi(self)
        self.setWindowTitle(u'大图检测')
        #self.setFixedSize(1280,720)
        screen = QDesktopWidget().screenGeometry()
        #self.resize(screen.width(), screen.height())
        self.setFixedSize(screen.width()-100, screen.height()-100)
        self.center()
        ##########################背景层,使用绝对坐标########################
        palette = QPalette()
        self.setBackgroundandSize(self,'./background.png',self.backgroundRole(),screen.height(),screen.width())

        ##########################标题部分,用的一张图片######################
        title = QLabel()
        self.setBackgroundandSize(title,'./titlebg.png',QPalette.Window,100,706)
        hboxTilte = QHBoxLayout()
        hboxTilte.addWidget(title)

        ##############################下方左侧#############################
        #########并列部分
        btnSelFile = QPushButton(u"选择文件")
        self.setBackgroundandSize(btnSelFile, './yellowbar.png', QPalette.Button, 23, 76)
        btnSelFile.setFlat(True)   #边缘消失
        editSelFile = QLineEdit(u"file:///")
        self.setBackgroundandSize(editSelFile, './greybar.png', QPalette.Base, 23, 115)
        hboxSelFile = QHBoxLayout()
        hboxSelFile.addWidget(btnSelFile)
        hboxSelFile.addWidget(editSelFile)
        self.connect(btnSelFile,SIGNAL("clicked()"),lambda:self.button_openfile_click(Application.btncontrol,editSelFile,previewImg))
        hboxPicSize = QHBoxLayout()
        self.addRow(hboxPicSize, u"大图尺寸", u"宽:xxx 高:xxx",Application.leftSide)
        hboxOnlineNodes = QHBoxLayout()
        self.addRow(hboxOnlineNodes, u"联机集群节点数", u"xxx",Application.leftSide,smaller=True)
        hboxUsedNodes = QHBoxLayout()
        self.addRow(hboxUsedNodes, u"使用集群节点数", u"xxx",Application.leftSide,smaller=True)
        ########原图预览
        previewTxt = QLabel(u"原图预览")
        previewTxt.setFixedHeight(25)
        previewTxt.setFont(QFont("Times New Roman",12))
        palette.setColor(QPalette.WindowText,Qt.yellow)
        previewTxt.setPalette(palette)
        previewTxt.setAlignment(Qt.AlignCenter)
        previewImg = QLabel()
        previewImg.setFixedHeight(0.3*screen.height())
        previewImg.setFixedWidth(0.2 * screen.width())
        previewImg.setAutoFillBackground(True)
        previewImg.setAlignment(Qt.AlignCenter)
        image = QPixmap("./rawpic.png").scaled(previewImg.width(), previewImg.height())
        previewImg.setPixmap(image)
        #self.setBackgroundandSize(previewImg,'./rawpic.png',QPalette.Window,128,196)
        ########终端显示
        statusTxt = QLabel(u"集群终端状态")
        statusTxt.setFixedHeight(25)
        statusTxt.setFont(QFont("Times New Roman", 12))
        palette.setColor(QPalette.WindowText, Qt.yellow)
        statusTxt.setPalette(palette)
        statusTxt.setAlignment(Qt.AlignCenter)
        #statusImg = QLabel()
        #statusImg.setFixedHeight(0.3 * screen.height())
        #statusImg.setFixedWidth(0.2 * screen.width())
        #statusImg.setAutoFillBackground(True)
        #statusImg.setAlignment(Qt.AlignCenter)
        #palette.setColor(statusImg.backgroundRole(), Qt.black)
        #statusImg.setPalette(palette)
        #statusImg.setText("hello!")
        self.statusEdit=QTextEdit("python gui.py")
        statusEdit = self.statusEdit
        statusEdit.setFixedHeight(0.3 * screen.height())
        statusEdit.setFixedWidth(0.2 * screen.width())
        statusEdit.setAutoFillBackground(True)
        statusEdit.setAlignment(Qt.AlignLeft)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.Text, Qt.yellow)
        statusEdit.setPalette(palette)
        #self.setBackgroundandSize(statusImg, './rawpic.png', QPalette.Window, 128, 196)
        ########以垂直的结构显示
        vboxleft = QVBoxLayout()
        vboxleft.addLayout(hboxSelFile)
        vboxleft.addLayout(hboxPicSize)
        vboxleft.addLayout(hboxOnlineNodes)
        vboxleft.addLayout(hboxUsedNodes)
        vboxleft.addWidget(previewTxt)
        vboxleft.addWidget(previewImg)
        vboxleft.addWidget(statusTxt)
        #vboxleft.addWidget(statusImg)
        vboxleft.addWidget(statusEdit)
        ###########################下方中间部分##########################
        ########控制按钮
        Application.btncontrol = QPushButton(u"将大图发送至集群")
        Application.btncontrol.setFont(QFont("Times New Roman", 12))
        Application.btncontrol.setEnabled(False)
        Application.btncontrol.setFixedHeight(25)
        Application.btncontrol.setFixedWidth(200)
        self.connect(Application.btncontrol, SIGNAL("clicked()"),self.button_control_click)
        ########显示处理后的图片
        mid = QLabel()
        mid.setFixedHeight(440)
        mid.setFixedWidth(550)
        # palette.setColor(QPalette.Window, Qt.red)
        # mid.setAutoFillBackground(True)
        # mid.setPalette(palette)
        ########中间部分垂直布局
        vboxmid = QVBoxLayout()
        vboxmid.addWidget(Application.btncontrol)
        vboxmid.addWidget(mid)

        ##########################下方右侧部分############################
        ########三个返回值
        hboxTime = QHBoxLayout()
        self.addRow(hboxTime, u"运行时间", u"xxx", Application.rightSide)
        hboxPlanes = QHBoxLayout()
        self.addRow(hboxPlanes, u"飞机目标数", u"xxx", Application.rightSide)
        hboxShips = QHBoxLayout()
        self.addRow(hboxShips, u"舰船目标数", u"xxx", Application.rightSide)
        btnCoordFile = QPushButton(u"展示结果图")
        #self.setBackgroundandSize(btnCoordFile, './yellowbar2.png', QPalette.Button, 23, 115)
        btnCoordFile.setFlat(True)  # 边缘消失
        self.connect(btnCoordFile, SIGNAL("clicked()"),self.button_show_click)###飞机船照片路径
        ########显示处理后的图片
        #coordFilePath = QLabel(u"file:///")
        #self.setBackgroundandSize(coordFilePath, './greybar.png', QPalette.Window, 23, 115)
        hboxCoordFile = QHBoxLayout()
        #hboxCoordFile.addWidget(coordFilePath)
        hboxCoordFile.addWidget(btnCoordFile)
        ########飞机
        self.planeImg = QLabel()
        planeImg = self.planeImg
        #planeImg.setAlignment(Qt.AlignCenter)
        #self.setBackgroundandSize(planeImg,'./rawpic2a.png',QPalette.Window,128,196)
        planeImg.setFixedHeight(0.3 * screen.height())
        planeImg.setFixedWidth(0.2 * screen.width())
        planeImg.setAutoFillBackground(True)
        planeImg.setAlignment(Qt.AlignCenter)
        planeimage = QPixmap("./rawpic2a.png").scaled(planeImg.width(), planeImg.height())
        planeImg.setPixmap(planeimage)
        ########船
        self.shipImg = QLabel()
        shipImg =self.shipImg
        #shipImg.setAlignment(Qt.AlignCenter)
        #self.setBackgroundandSize(shipImg, './rawpic2b.png', QPalette.Window, 128, 196)
        shipImg.setFixedHeight(0.3 * screen.height())
        shipImg.setFixedWidth(0.2 * screen.width())
        shipImg.setAutoFillBackground(True)
        shipImg.setAlignment(Qt.AlignCenter)
        self.shipimage = QPixmap("./rawpic2b.png").scaled(shipImg.width(), shipImg.height())
        shipImg.setPixmap(self.shipimage)
        ########下方右侧布局
        vboxright = QVBoxLayout()
        vboxright.addLayout(hboxTime)
        vboxright.addLayout(hboxPlanes)
        vboxright.addLayout(hboxShips)
        vboxright.addLayout(hboxCoordFile)
        vboxright.addWidget(planeImg)
        vboxright.addWidget(shipImg)

        ##########################整体布局############################
        ########下方左中右
        hboxbody = QHBoxLayout()
        hboxbody.addLayout(vboxleft)
        hboxbody.addStretch(1)
        hboxbody.addLayout(vboxmid)
        hboxbody.addStretch(1)
        hboxbody.addLayout(vboxright)
        ########上下两部分
        vbox = QVBoxLayout()
        vbox.addLayout(hboxTilte)
        vbox.addStretch(0)
        vbox.addLayout(hboxbody)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def setBackgroundandSize(self, qwidget, imgpath, role, fixedHeight=None, fixedWidth=None):
        if isinstance(qwidget, QWidget) and isinstance(imgpath,str):
            palette = QPalette()
            palette.setBrush(role, QBrush(QPixmap(imgpath)))
            qwidget.setAutoFillBackground(True)
            qwidget.setPalette(palette)
            if fixedHeight is not None and fixedWidth is not None:
                qwidget.setFixedHeight(fixedHeight)
                qwidget.setFixedWidth(fixedWidth)

    def addRow(self,box,text,text_,pos,smaller=False):# 用smaller的原因是有时候文本过长,所以缩小字号
        lab = QLabel(text)
        if smaller:
            lab.setFont(QFont("Times New Roman",8))
        lab.setAlignment(Qt.AlignCenter)
        if pos:
            self.setBackgroundandSize(lab, './yellowbar.png', QPalette.Window, 23, 76)
        else:
            self.setBackgroundandSize(lab, './yellowbar2.png', QPalette.Window, 23, 76)
        lab_ = QLabel(text_)
        lab_.setAlignment(Qt.AlignCenter)
        self.setBackgroundandSize(lab_, './greybar.png', QPalette.Window, 23, 115)
        if pos: #pos==1表示左侧那四行,pos==0表示右侧那四行
            box.addWidget(lab)
            box.addWidget(lab_)
        else:
            box.addWidget(lab_)
            box.addWidget(lab)
        #self.labels.append(lab)
        #self.labels.append(lab_)

    def button_openfile_click(self,btncontrol,editSelFile,previewImg):
        absulute_path = QFileDialog.getOpenFileName(self,'Open File','.','png files(*.png)')
        if absulute_path:
            cur_path = QDir('.')
            relative_path=cur_path.relativeFilePath(absulute_path)
            editSelFile.setText(relative_path)
            image = QPixmap(relative_path).scaled(previewImg.width(),previewImg.height())
            previewImg.setPixmap(image)
            os.system("python aaa.py")
            self.statusEdit.append("python aaa.py")
            #self.hboxPicSize.setText(u"???")
            #self.hboxOnlineNodes.setText(u"???")
            #self.hboxUsedNodes.setText(u"???")
            btncontrol.setEnabled(True)

    def button_control_click(self):
        #点几次？？
        Application.btncontrol.setEnabled(False)
        self.statusEdit.append("./???.sh")

        self.controlThread = Runthread(True)
        self.controlThread.finishSignal_sh.connect(self.terminal)
        self.controlThread.start()
    def terminal(self,str):
        self.statusEdit.append(str)#进程窗口展示进度条???
        if str == "end" :
            Application.btncontrol.setEnabled(True)

    def button_show_click(self):
        self.planeThread = Runthread(False,"plane")
        self.planeThread.finishSignal_sh.connect(self.showplanepicture)
        self.planeThread.start()
        self.shipThread = Runthread(False, "ship")
        self.shipThread.finishSignal_sh.connect(self.showshippicture)
        self.shipThread.start()

    #def button_show_click(self):
    #    kinds =["plane","ship"]
    #    for kind in kinds:
    #        self.kindThread = Runthread(False,kind)
    #        if kind =="plane":
    #            self.kindThread.finishSignal_show.connect(self.showplanepicture)
    #        else:
    #            self.kindThread.finishSignal_show.connect(self.showshippicture)
    #        self.kindThread.start()
    def showshippicture(self,str):
        print str
        if "png" in str:
            print  "right"
            shipimage = QPixmap("./ship/" + str).scaled(self.shipImg.width(), self.shipImg.height())
            self.shipImg.setPixmap(shipimage)
        else:
            self.statusEdit.append(str)  # 进程窗口展示进度条???

    def showplanepicture(self,str):
        print str
        if "png" in str:
            print  "right"
            planeimage = QPixmap("./plane/"+str).scaled(self.planeImg.width(), self.planeImg.height())
            self.planeImg.setPixmap(planeimage)
        else:
            self.statusEdit.append(str)  # 进程窗口展示进度条???

class Runthread(QThread):
    finishSignal_sh = pyqtSignal(str)
    #finishSignal_show = pyqtSignal(str)
    def __init__(self,flag,kind="",parent=None):
        super(Runthread, self).__init__(parent)
        self.flag = flag
        self.kind = kind
    def run(self):
        if self.flag:##脚本线程
            self.finishSignal_sh.emit("./aaa.sh")
            os.system("bash ./aaa.sh")
            self.finishSignal_sh.emit("end")
        else:
            labels=[]##展示图片线程
            for f in os.listdir("./"+self.kind+"/"):
                if "png" in f:
                    print f
                    labels.append(f)
                    #self.finishSignal_show.emit(f)
                    self.finishSignal_sh.emit(f)
                    time.sleep(1)
            if len(labels) < 1:
                self.finishSignal_sh.emit("no result of "+self.kind)
                self.finishSignal_sh.emit(".rawpic2.png")

# 信号焕发，我是通过我封装类的回调来发起的
# self._signal.emit(msg);

app = QApplication(sys.argv)
foo = Application()
foo.show()
sys.exit(app.exec_())
