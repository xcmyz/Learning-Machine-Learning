from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint
from PyQt5.QtGui import QColor
import sys
import json
import translator
import aiml
import os


class messageW(QWidget):

    def __init__(self, Msg, sender):
        QWidget.__init__(self)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.setFont(font)
        self.pixmapRight = QtGui.QPixmap("./img/user.jpg")
        self.pixmapLeft = QtGui.QPixmap("./img/helper.jpg")
        self.Msg = Msg
        self.sender = sender

    def fontRect(self):
        iconWH = 30
        triW = 6
        spaceWithTri = 4
        spaceW = 10
        self.spaceH = 20

        textWidth = self.width() - (spaceW + iconWH + spaceWithTri + triW) * 2
        matrics = QtGui.QFontMetricsF(self.font())
        totalWidth = matrics.boundingRect(self.Msg).width()
        n = totalWidth//textWidth+1
        lineH = matrics.lineSpacing()
        textBelowIcon = iconWH - lineH
        textHeight = n * lineH
        if textHeight < iconWH:
            totalHeight = iconWH + self.spaceH
        else:
            totalHeight = textHeight + self.spaceH
        if textWidth > totalWidth:
            textWidth = totalWidth + 10

        if self.sender == 'user':
            self.iconRightRec = QRect(
                self.width() - iconWH - spaceW, self.spaceH, iconWH, iconWH)
            self.textRightRec = QtCore.QRectF(self.width(
            ) - textWidth - (spaceW + iconWH + spaceWithTri + triW)-5, self.spaceH + textBelowIcon, textWidth, textHeight)
            self.frameRight = self.textRightRec.adjusted(
                -5,  - textBelowIcon, 5, 5)
        else:
            self.iconLeftRec = QRect(spaceW, self.spaceH, iconWH, iconWH)
            self.textLeftRec = QtCore.QRectF(
                spaceW + iconWH + spaceWithTri + triW + 5, self.spaceH + textBelowIcon, textWidth, textHeight)
            self.frameLeft = self.textLeftRec.adjusted(
                -5,  - textBelowIcon, 5, 5)
        size = QtCore.QSize(self.width(), totalHeight + 20)
        self.setFixedHeight(totalHeight + 20)
        return size

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing |
                               QtGui.QPainter.SmoothPixmapTransform)
        option = QtGui.QTextOption(Qt.AlignLeft | Qt.AlignVCenter)
        option.setWrapMode(QtGui.QTextOption.WordWrap)
        if self.sender == 'user':
            painter.drawPixmap(self.iconRightRec, self.pixmapRight)
            painter.setBrush(QColor(75, 164, 242))
            painter.drawRoundedRect(self.frameRight, 4.0, 4.0)
            painter.setPen(QColor(75, 164, 142))
            points = [QPoint(self.frameRight.right(), self.frameRight.top() + 6), QPoint(self.frameRight.right(
            ) + 6, self.frameRight.top() + 12), QPoint(self.frameRight.right(), self.frameRight.top() + 18)]
            painter.drawPolygon(QtGui.QPolygon(points), 3)
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(self.font())
            # print("########&&&")
            # print(self.Msg)
            painter.drawText(self.textRightRec, self.Msg, option)
        else:
            painter.drawPixmap(self.iconLeftRec, self.pixmapLeft)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRoundedRect(self.frameLeft, 4.0, 4.0)
            painter.setPen(QColor(0, 0, 0))
            points = [QPoint(self.frameLeft.left(), self.frameLeft.top() + 6), QPoint(self.frameLeft.left(
            )-6, self.frameLeft.top() + 12), QPoint(self.frameLeft.left(), self.frameLeft.top() + 18)]
            painter.drawPolygon(QtGui.QPolygon(points), 3)
            painter.setPen(QColor(51, 51, 51))
            painter.setFont(self.font())
            # print("########$$$")
            # print(self.Msg)
            painter.drawText(self.textLeftRec, self.Msg, option)

        # painter.setBrush(QColor(75, 164, 242))
        # painter.drawRoundedRect(self.iconRightRec, 4, 4)
        painter.end()


class myTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self, parent)
        self.parent = parent

    def keyPressEvent(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self, event)
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.clearSelection()
            cursor.deletePreviousChar()
            if self.toPlainText() != '':
                self.parent.dealMessage()


class mywindow(QtWidgets.QWidget):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setWindowTitle('')
        self.Uinit()
        self.mybot = aiml.Kernel()
        self.mybot.learn("std-startup.xml")
        self.mybot.respond('load aiml b')

    def Uinit(self):
        self.resize(450, 500)
        self.setMinimumSize(QtCore.QSize(200, 200))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.setFont(font)
        # self.layout = QtWidgets.QVBoxLayout()
        self.edit = myTextEdit(self)
        self.edit.setFixedHeight(100)
        self.edit.setGeometry(10, self.height()-110, self.width()-20, 100)
        # self.edit.setMinimumHeight(100)
        # self.edit.setMaximumHeight(100)
        font.setPointSize(10)
        self.edit.setFont(font)
        # self.edit.installEventFilter()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.setGeometry(self.width()-20-70, self.height()-20-24, 70, 24)
        #font.setFamily("Microsoft JhengHei Light")
        # font.setBold(False)
        font.setWeight(50)
        font.setPointSize(10)
        self.btn.setFont(font)
        '''
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)                                             
        sizePolicy.setVerticalStretch(0)                                               
        sizePolicy.setHeightForWidth(self.btn.sizePolicy().hasHeightForWidth()) 
        self.btn.setSizePolicy(sizePolicy)
        '''
        self.btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn.setText("return")
        self.btn.setShortcut("Return")

        self.list = QtWidgets.QListWidget(self)
        self.list.setGeometry(0, 0, self.width(), self.height()-120)
        '''
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        '''

        self.btn.clicked.connect(self.dealMessage)

    # def eventFilter(self, obj, event):
        # if obj == self.edit and event.type() == QtCore.QEvent.KeyPress:

    def resizeEvent(self, event):
        self.list.resize(self.width(), self.height()-120)
        self.edit.setGeometry(10, self.height()-110, self.width()-20, 100)
        self.btn.move(self.width()-90, self.height()-44)
        for i in range(0, self.list.count()):
            item = self.list.item(i)
            message = self.list.itemWidget(item)
            message.setFixedWidth(self.width()-25)
            item.setSizeHint(message.fontRect())
        self.list.scrollToBottom()

    def dealMessage(self):
        Msg = self.edit.toPlainText()
        self.edit.clear()
        message = messageW(Msg, 'user')
        item = QListWidgetItem(self.list)
        message.setFixedWidth(self.width()-25)
        item.setSizeHint(message.fontRect())
        self.list.setItemWidget(item, message)
        self.list.scrollToBottom()
        Msg = translator.translator(Msg, fromLang="ch", toLang="en")
        # print("[ ", mes, " ]")
        get = self.mybot.respond(Msg)
        get = translator.translator(get)            
        # print("bot: ", get)
        returnMsg = get
        message = messageW(returnMsg, 'helper')
        item = QListWidgetItem(self.list)
        message.setFixedWidth(self.width()-25)
        item.setSizeHint(message.fontRect())
        self.list.setItemWidget(item, message)
        self.list.scrollToBottom()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
