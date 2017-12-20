#!/usr/bin/python
#coding:utf-8

import sys
from PyQt4 import QtCore, QtGui
import time
import subprocess
class Application(QtCore.QWidget):
    leftSide = 1
    rightSide = 0
    def __init__(self, parent=None):
        QtCore.QWidget.__init__(self, parent)
        self.setWindowTitle(u'遥感影像深度学习FPGA系统')
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width()-100, screen.height()-100)
        self.center()
        self.relative_path = None
        ##########################背景层,使用绝对坐标########################
        palette = QPalette()
        image = QPixmap("./backgrounddark.png").scaled(screen.width()-100, screen.height()-100)
        palette.setBrush(self.backgroundRole(), QBrush(image))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.setFixedHeight(screen.height()-100)
        self.setFixedWidth(screen.width()-100)
        ##########################标题部分大小######################
        title = QLabel()
        self.setBackgroundandSize(title,'',QPalette.Window,99,706)
        hboxTilte = QHBoxLayout()
        hboxTilte.addWidget(title)
        ###########################下方中间部分##########################
        ########显示大图
        self.mid = QLabel()
        mid = self.mid
        mid.setFixedHeight(0.74 * screen.height())
        mid.setFixedWidth(0.75 * screen.width())
        mid.setAlignment(Qt.AlignCenter)
        self.image_viewer = ImageViewer(self.mid)
        ########选择文件
        self.btnSelFile = QPushButton(u"choose file")
        self.setBackgroundandSize(self.btnSelFile, './bluebar.png', QPalette.Button, 23, 76)
        self.btnSelFile.setFlat(True)  # 边缘消失
        self.editSelFile = QLineEdit(u"")
        self.setBackgroundandSize(self.editSelFile, './greybar.png', QPalette.Base, 23, 600)
        hboxSelFile = QHBoxLayout()
        hboxSelFile.addStretch(1)
        hboxSelFile.addWidget(self.btnSelFile)
        hboxSelFile.addWidget(self.editSelFile)
        hboxSelFile.addStretch(1)
        ########中间部分垂直布局
        vboxmid = QVBoxLayout()
        vboxmid.addWidget(self.mid)
        vboxmid.addLayout(hboxSelFile)

        ##########################下方右侧部分############################
        #########并列部分
        self.btnPlay = QPushButton("PLAY")
        self.btnPlay.setFont(QFont("Times New Roman", 12))
        self.btnPlay.setEnabled(False)
        self.btnPlay.setFlat(True)
        self.setBackgroundandSize(self.btnPlay, './playbluebar.png', QPalette.Button, 25, 180)
        hboxmid = QHBoxLayout()
        hboxmid.addWidget(self.btnPlay)
        self.labelPicSize = QLabel(u"<font color=white>width:xxx height:xxx</font>")
        hboxpicsizeBox =  QHBoxLayout()
        self.addRow(self.labelPicSize, u"image size",hboxpicsizeBox ,Application.leftSide)
        labelContrain = QLabel(u"<font color=white>thresh</font>")
        labelContrain.setFixedWidth(60)
        labelContrain.setAlignment(Qt.AlignLeft)
        self.lineEdit =QLineEdit(u"")
        #self.lineEdit.setFixedWidth(130)
        self.setBackgroundandSize(self.lineEdit, './greybar.png', QPalette.Base, 23, 100)
        self.lineEdit.setAlignment(Qt.AlignRight)
        self.btnDone = QPushButton("DONE")
        self.btnDone.setFlat(True)
        self.setBackgroundandSize(self.btnDone, './playbluebar.png', QPalette.Button, 25, 60)
        self.btnDone.setEnabled(False)
        hboxcontrainBox = QHBoxLayout()
        hboxcontrainBox.addWidget(labelContrain)
        hboxcontrainBox.addStretch(1)
        hboxcontrainBox.addWidget(self.lineEdit)
        hboxcontrainBox.addWidget(self.btnDone)
        self.labelTime = QLabel(u"<font color=white>xxx</font>")
        hboxtimeBox= QHBoxLayout()
        self.addRow(self.labelTime, u"time", hboxtimeBox, Application.leftSide)
        self.labelPlanes = QLabel(u"<font color=white>xxx</font>")
        hboxplaneBox = QHBoxLayout()
        self.addRow(self.labelPlanes, u"plane",hboxplaneBox, Application.leftSide)
        self.labelShips = QLabel(u"<font color=white>xxx</font>")
        hboxshipBox = QHBoxLayout()
        self.addRow(self.labelShips, u"ship", hboxshipBox, Application.leftSide)
        self.labelPow = QLabel(u"<font color=white>xxx</font>")
        hboxpowBox = QHBoxLayout()
        self.addRow(self.labelPow, u"power", hboxpowBox, Application.leftSide)
        self.labelRecall = QLabel(u"<font color=white>xxx</font>")
        hboxrecallBox = QHBoxLayout()
        self.addRow(self.labelRecall, u"recall", hboxrecallBox, Application.leftSide)
        self.labelPrec = QLabel(u"<font color=white>xxx</font>")
        hboxprecBox = QHBoxLayout()
        self.addRow(self.labelPrec, u"mAP", hboxprecBox, Application.leftSide)
        ########终端显示
        statusTxt = QLabel(u"Terminal")
        statusTxt.setFixedHeight(25)
        statusTxt.setFont(QFont("Times New Roman", 12))
        palette.setColor(QPalette.WindowText, Qt.yellow)
        statusTxt.setPalette(palette)
        statusTxt.setAlignment(Qt.AlignCenter)
        self.statusEdit = QTextEdit("python gui.py")
        statusEdit = self.statusEdit
        statusEdit.setFixedHeight(0.4 * screen.height())
        statusEdit.setFixedWidth(0.17 * screen.width())
        statusEdit.setAutoFillBackground(True)
        statusEdit.setAlignment(Qt.AlignLeft)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.Text, Qt.cyan)
        statusEdit.setPalette(palette)
        ########下方右侧布局
        vboxright = QVBoxLayout()
        vboxright.addStretch(1)
        vboxright.addLayout(hboxmid)
        vboxright.addStretch(1)
        vboxright.addLayout(hboxpicsizeBox)
        vboxright.addLayout(hboxcontrainBox)
        vboxright.addLayout(hboxtimeBox)
        vboxright.addLayout(hboxplaneBox)
        vboxright.addLayout(hboxshipBox)
        vboxright.addLayout(hboxpowBox)
        vboxright.addLayout(hboxrecallBox)
        vboxright.addLayout(hboxprecBox)
        vboxright.addStretch(1)
        vboxright.addWidget(statusTxt)
        vboxright.addWidget(statusEdit)
        vboxright.addStretch(1)
        ##########################整体布局############################
        ########下方左中右
        hboxbody = QHBoxLayout()
        #        hboxbody.addLayout(vboxleft)
        hboxbody.addStretch(1)
        hboxbody.addLayout(vboxright)
        hboxbody.addStretch(1)
        hboxbody.addLayout(vboxmid)
        ########上下两部分
        vbox = QVBoxLayout()
        vbox.addLayout(hboxTilte)
        vbox.addStretch(0)
        vbox.addLayout(hboxbody)
        vbox.addStretch(1)
        self.setLayout(vbox)
        ##########################按钮链接初始化##########################
        self.__connect__()
##########################按钮链接函数##########################
    def __connect__(self):
        self.connect(self.btnSelFile, SIGNAL("clicked()"),self.button_openfile_click)
        self.connect(self.btnPlay, SIGNAL("clicked()"), self.button_play_click)
        self.connect(self.btnDone, SIGNAL("clicked()"), self.button_done_click)
##########################布局相关函数##########################
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
    def addRow(self,lab_,text,box,pos,smaller=False):# 用smaller的原因是有时候文本过长,所以缩小字号
        lab = QLabel(text)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        lab.setPalette(palette)
        if smaller:
            lab.setFont(QFont("Times New Roman",8))
        lab.setAlignment(Qt.AlignLeft)
        lab_.setAlignment(Qt.AlignCenter)
        self.setBackgroundandSize(lab_, './greybar2.png', QPalette.Window, 23, 200)
        if pos: #pos==1表示左侧那四行,pos==0表示右侧那四行
            box.addWidget(lab)
            box.addWidget(lab_)
        else:
            box.addWidget(lab_)
            box.addWidget(lab)
##########################打开文件按钮##########################
    def button_openfile_click(self):
        absulute_path = QFileDialog.getOpenFileName(self,'Open File','/root/yolo_con_20171101/orgimage/','tif files(*.tif)')
        if absulute_path:
            cur_path = QDir('.')
            self.relative_path=cur_path.relativeFilePath(absulute_path)
            relative_path=self.relative_path
            self.editSelFile.setText(relative_path)
            ##########重新清空
            self.statusEdit.moveCursor(QTextCursor.End)
            self.statusEdit.append("choose "+relative_path)
            self.labelTime.setText(u"<font color=white>xxx</font>")
            self.labelPlanes.setText(u"<font color=white>xxx</font>")
            self.labelShips.setText(u"<font color=white>xxx</font>")
            self.labelRecall.setText(u"<font color=white>xxx</font>")
            self.labelPrec.setText(u"<font color=white>xxx</font>")
            ##########得到新值
            self.image_viewer.loadImage(relative_path)
            self.image_viewer.enablePan(True)
            getsize.get(str(relative_path))
            self.labelPicSize.setText(u"<font color=white>width:"+getsize.picwidth+u" height:"+getsize.picheight+"</font>")
            self.statusEdit.moveCursor(QTextCursor.End)
            self.btnDone.setEnabled(True)
    def button_done_click(self):
	    self.threshold = self.lineEdit.text()
	    if self.threshold != "":
                self.btnPlay.setEnabled(True)
##########################将大图发送到集群按钮##########################
    def button_play_click(self):
        self.btnSelFile.setEnabled(False)
        self.btnDone.setEnabled(False)
        self.btnPlay.setEnabled(False)
        self.statusEdit.append("send picture to FPGA")
        self.threadPlay = Runthread(self.threshold,self.relative_path)
        self.threadPlay.finishSignal_sh.connect(self.terminal)
        self.threadPlay.start()
    #####脚本运行时候终端的显示
    def terminal(self,strflag):
        self.statusEdit.moveCursor(QTextCursor.End)
        self.statusEdit.append(strflag)
        self.show_sh_result(strflag)
    #####脚本执行后希望界面展示的东西
    def show_sh_result(self,strflag):
        if "plane_num:" in strflag:
	        self.labelPlanes.setText(u"<font color=white>"+strflag[10:-1]+u"</font>")
        if "ship_num:" in strflag:
            self.labelShips.setText(u"<font color=white>"+strflag[9:-1]+u"</font>")
        if "power:" in strflag:
	        self.labelPow.setText(u"<font color=white>"+strflag[6:-1]+u"</font>")
        if "Cost" in strflag:
            self.labelTime.setText(u"<font color=white>"+strflag[5:10]+u"</font>"+u"s")
        if strflag == "end":
            result_path = self.relative_path.replace('orgimage', 'imageResult')
            result_path = result_path.replace('tif','jpg')
            self.image_viewer.loadImage(result_path)
            self.image_viewer.enablePan(True)
            self.btnSelFile.setEnabled(True)

##########################线程类##########################
class Runthread(QThread):
    finishSignal_sh = pyqtSignal(str)
    def __init__(self,threshold,relative_path,parent=None):
        super(Runthread, self).__init__(parent)
        self.threshold = threshold
        self.relative_path = relative_path
    def run(self):
        self.finishSignal_sh.emit("python detectbigimage2.0.py")
        starttime = time.time()
        p = subprocess.Popen(['python','detectbigimage2.0.py',self.threshold,self.relative_path],stdout=subprocess.PIPE)
        while True:
            data = p.stdout.readline()
            if (not data):
                break
            else:
                print data
                self.finishSignal_sh.emit(data)
        endtime = time.time()
        self.finishSignal_sh.emit("Cost "+str(endtime-starttime)+" s")
        self.finishSignal_sh.emit("end")
##########################GUI窗口初始化##########################
app = QApplication(sys.argv)
foo = Application()
foo.show()
sys.exit(app.exec_())
