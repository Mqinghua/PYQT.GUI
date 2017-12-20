#!/usr/bin/python
#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *

__author__ = "Atinderpal Singh"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "atinderpalap@gmail.com"

class ImageViewer:
    ''' Basic image viewer class to show an image with zoom and pan functionaities.
        Requirement: Qt's Qlabel widget name where the image will be drawn/displayed.
    '''
    def __init__(self,qlabel):

        self.zoomX = 0              # zoom factor w.r.t size of qlabel_image
        self.position = [0, 0]      # position of top left corner of qimage_label w.r.t. qimage_scaled
        self.panFlag = False        # to enable or disable pan
        self.pressed = None
        self.anchor = None  ### 鼠标按下时刻 左上角

        self.mid = qlabel
        self.qimage = QImage("./background.png")
        self.qpixmap = QPixmap(self.mid.size())
        self.image = self.qimage.scaled(self.mid.width() * (1.5 ** self.zoomX),
                                        self.mid.height() * (1.5 ** self.zoomX), Qt.KeepAspectRatio)
        self.update()
        self.__connectEvents()

    def __connectEvents(self):
        # Mouse events
        self.mid.mousePressEvent = self.mousePressAction
        self.mid.mouseMoveEvent = self.mouseMoveAction
        self.mid.mouseReleaseEvent = self.mouseReleaseAction

    def update(self):
        ''' This function actually draws the scaled image to the qlabel_image.
            It will be repeatedly called when zooming or panning.
            So, I tried to include only the necessary operations required just for these tasks.
        '''
        if not self.qimage_scaled.isNull():
            # check if position is within limits to prevent unbounded panning.
            px, py = self.position
            px = px if (px <= self.qimage_scaled.width() - self.mid.width()) else (self.qimage_scaled.width() - self.mid.width())
            py = py if (py <= self.qimage_scaled.height() - self.mid.height()) else (self.qimage_scaled.height() - self.mid.height())
            px = px if (px >= 0) else 0
            py = py if (py >= 0) else 0
            self.position = (px, py)

            if self.zoomX == 1:
                self.qpixmap.fill(QtCore.Qt.white)

            # the act of painting the qpixamp
            painter = QPainter()
            painter.begin(self.qpixmap)
            painter.drawImage(QtCore.QPoint(0, 0), self.qimage_scaled,
                    QtCore.QRect(self.position[0], self.position[1], self.mid.width(), self.mid.height()) )
            painter.end()

            self.mid.setPixmap(self.qpixmap)
        else:
            pass

    def mousePressAction(self, QMouseEvent):
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        if x > 0 and x < self.mid.width() and y > 0 and y < self.mid.height():
            self.panFlag = True
        ##判断是不是在面板处 是的话 panFlag = True
        if self.panFlag:
            self.pressed = QMouseEvent.pos()    # starting point of drag vector
            self.anchor = self.position         # save the pan position when panning starts

    def mouseMoveAction(self, QMouseEvent):
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        if self.pressed:
            dx, dy = x - self.pressed.x(), y - self.pressed.y()         # calculate the drag vector
            self.position = self.anchor[0] - dx, self.anchor[1] - dy    # update pan position using drag vector
            self.update()                                               # show the image with udated pan position

    def mouseReleaseAction(self, QMouseEvent):
        self.pressed = None                                             # clear the starting point of drag vector
        self.anchor = None
    def zoomPlus(self):
        self.zoomX += 1
        px, py = self.position
        px += self.mid.width()/2
        py += self.mid.height()/2
        self.position = (px, py)
        self.qimage_scaled = self.qimage.scaled(self.mid.width() * self.zoomX, self.mid.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
        self.update()
###qimage_scaled  image  qlabel_image ,id
    def zoomMinus(self):
        if self.zoomX > 1:
            self.zoomX -= 1
            px, py = self.position
            px -= self.mid.width()/2
            py -= self.mid.height()/2
            self.position = (px, py)
            self.qimage_scaled = self.qimage.scaled(self.mid.width() * self.zoomX, self.mid.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
            self.update()


    def enablePan(self, value):
        self.panFlag = value