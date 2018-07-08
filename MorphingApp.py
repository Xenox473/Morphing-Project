from PySide.QtGui import *
from MorphingGUI import *
import sys
import os
import numpy as np
from scipy import spatial
from Morphing import *

class Consumer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Consumer, self).__init__(parent)
        self.setupUi(self)
        self.initialState()
        self.LoadStartBtn.clicked.connect(self.loadStartingImage)
        self.LoadEndBtn.clicked.connect(self.loadEndingImage)
        self.checkBox.stateChanged.connect(self.triangles)
        self.SlidertxtBox.setReadOnly(True)
        self.horizontalSlider.setRange(0,20)
        self.horizontalSlider.setTickInterval(0.05)
        self.horizontalSlider.valueChanged.connect(self.update)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.SlidertxtBox.setText('0.0')
        self.BlendBtn.clicked.connect(self.morph)
        self.isStartClicked = False
        self.isEndClicked = False
        self.wait = False
        self.newEndPoints = np.array([])
        self.newStartPoints = np.array([])

        # self.mousePressEvent.connect(self.clicker)
        # self.SlidertxtBox.setAlignment(Qt.AlignHCenter)

    def persist(self,event):

        if(self.isStartClicked and self.isEndClicked and not self.wait):
            self.startScene.removeItem(self.startDraw)
            self.startScene.addEllipse(self.tempStartPosition.x(),self.tempStartPosition.y(),10,10,QPen(QtCore.Qt.blue),QBrush(QtCore.Qt.blue))
            self.endScene.removeItem(self.endDraw)
            self.endScene.addEllipse(self.tempEndPosition.x(),self.tempEndPosition.y(),10,10,QPen(QtCore.Qt.blue),QBrush(QtCore.Qt.blue))
            self.isEndClicked = False
            self.isStartClicked = False
            self.wait = True
            if self.newStartPoints.any():
                self.newStartPoints = np.vstack((self.newStartPoints,np.array([[self.tempStartPosition.x(), self.tempStartPosition.y()]])))
            else:
                self.newStartPoints = np.array([[self.tempStartPosition.x(), self.tempStartPosition.y()]])
            if self.newEndPoints.any():
                self.newEndPoints = np.vstack((self.newEndPoints,np.array([[self.tempEndPosition.x(), self.tempEndPosition.y()]])))
            else:
                self.newEndPoints = np.array([[self.tempEndPosition.x(), self.tempEndPosition.y()]])
            with open(self.startfilePath+'.txt',"a") as file:
                file.write('\n'+str(int(round(self.tempStartPosition.x(), 0)))+' '+str(int(round(self.tempStartPosition.y(),0)))+'\n')
            with open(self.endfilePath+'.txt',"a") as file:
                file.write('\n'+str(int(round(self.tempEndPosition.x(), 0)))+' '+str(int(round(self.tempEndPosition.y(),0)))+'\n')
            self.triangles()
            if self.tempStartPosition != self.nextPos:
                if not self.isStartClicked:
                    self.isStartClicked = True
                    position = self.nextPos
                    self.startDraw = self.startScene.addEllipse(position.x(),position.y(),10,10,QPen(QtCore.Qt.green),QBrush(QtCore.Qt.green))
                    self.tempStartPosition = position
            # if not self.isStartClicked:
            #     self.isStartClicked = True
            #     position = event.lastScenePos()
            #     self.startDraw = self.startScene.addEllipse(position.x(),position.y(),10,10,QPen(QtCore.Qt.green),QBrush(QtCore.Qt.green))
            #     self.tempStartPosition = position
        elif self.wait:
            self.wait = False

    def removeStartPoint(self, event):
        if(self.isStartClicked and event.key() == QtCore.Qt.Key_Backspace):
            self.startScene.removeItem(self.startDraw)
            self.isStartClicked = False

    def removeEndPoint(self, event):
        if(self.isEndClicked and event.key() == QtCore.Qt.Key_Backspace):
            self.endScene.removeItem(self.endDraw)
            self.isEndClicked = False
            self.wait = False

    def pointStartDraw(self, event):
        self.nextPos = event.lastScenePos()
        if not self.isStartClicked:
            self.isStartClicked = True
            position = event.lastScenePos()
            self.startDraw = self.startScene.addEllipse(position.x(),position.y(),10,10,QPen(QtCore.Qt.green),QBrush(QtCore.Qt.green))
            self.tempStartPosition = position
            #self.startDraw = QGraphicsEllipseItem(position.x(),position.y(),5,5,QPen(QtCore.Qt.green),QBrush(QtCore.Qt.green))
        # elif (self.isStartClicked and self.isEndClicked):
        #     self.startScene.removeItem(self.startDraw)
        #     self.startScene.addEllipse(self.tempStartPosition.x(),self.tempStartPosition.y(),5,5,QPen(QtCore.Qt.blue),QBrush(QtCore.Qt.blue))
        #     self.endScene.removeItem(self.endDraw)
        #     self.endScene.addEllipse(self.tempEndPosition.x(),self.tempEndPosition.y(),5,5,QPen(QtCore.Qt.blue),QBrush(QtCore.Qt.blue))
        #     self.isEndClicked = False
        #     self.isStartClicked = False

    def pointEndDraw(self, event):
        if not self.isEndClicked and self.isStartClicked:
            self.isEndClicked = True
            position = event.lastScenePos()
            self.endDraw = self.endScene.addEllipse(position.x(),position.y(),10,10,QPen(QtCore.Qt.green),QBrush(QtCore.Qt.green))
            self.tempEndPosition = position
        self.wait = True


    def initialState(self):
        self.horizontalSlider.setDisabled(True)
        self.SlidertxtBox.setDisabled(True)
        self.BlendBtn.setDisabled(True)
        self.checkBox.setDisabled(True)

    def update(self):
        self.SlidertxtBox.setText(str(self.horizontalSlider.value()/20))

    def morph(self):
        sourceImage = imageio.imread(self.startfilePath)
        endImage = imageio.imread(self.endfilePath)
        if self.newStartPoints.any() and not self.startPoints.any():
            self.templistStart = self.newStartPoints
            self.templistEnd = self.newEndPoints
        elif self.newStartPoints.any():
            self.templistStart = np.vstack((self.startPoints,self.newStartPoints))
            self.templistEnd = np.vstack((self.endPoints,self.newEndPoints))
        else:
            self.templistStart = self.startPoints
            self.templistEnd = self.endPoints
        startPoints = self.templistStart
        endPoints = self.templistEnd
        if len(sourceImage.shape) == 3:
            Image1 = ColorBlender(np.array(sourceImage), np.array(startPoints), np.array(endImage), np.array(endPoints)).getBlendedImage(self.horizontalSlider.value()/20)
            finalImage = QtGui.QImage(Image1, Image1.shape[1],Image1.shape[0], Image1.shape[1]*3,QtGui.QImage.Format_RGB888)

        else:
            Image2 = Blender(np.array(sourceImage), np.array(startPoints), np.array(endImage), np.array(endPoints)).getBlendedImage(self.horizontalSlider.value()/20)
            finalImage = QtGui.QImage(Image2, Image2.shape[1],Image2.shape[0], Image2.shape[1],QtGui.QImage.Format_Indexed8)

        # image = QtGui.QImage(test_image, test_image.shape[1],test_image.shape[0], test_image.shape[1],QtGui.QImage.Format_Indexed8)
        tempScene = QGraphicsScene()
        tempScene1 = QPixmap.fromImage(finalImage)
        tempScene.addPixmap(tempScene1)
        self.BlendResult.setScene(tempScene)
        self.BlendResult.fitInView(tempScene.itemsBoundingRect())

    def loadStartingImage(self):
        filePath = self.loadFileDialog()
        self.startfilePath = filePath
        # scene = QGraphicsScene()
        # pixmap = QPixmap(filePath)
        # pixmap = pixmap.scaled(235,190, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # scene.addPixmap(pixmap)
        # self.StartingImage.setScene(scene)
        # self.StartingImage.fitInView(scene.itemsBoundingRect())
        if filePath:
            if os.path.isfile(filePath+".txt"):
                 if os.stat(filePath+".txt") != 0:
                    self.startPoints = np.loadtxt(filePath+".txt")
            else:
                self.startPoints = np.array([])
                # file = open(filePath+".txt", 'w')
                # file.close()
            self.loadStartPoints(filePath)
        # frame = QWidget()
        # self.StartingImage = QtGui.Qlabel(frame)
        # image = QImage(filePath)
        # image = image.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # self.S

    def loadEndingImage(self):
        filePath = self.loadFileDialog()
        self.endfilePath = filePath
        # scene = QGraphicsScene()
        # pixmap = QPixmap(filePath)
        # pixmap = pixmap.scaled(235,190, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # scene.addPixmap(pixmap)
        # self.EndingImage.setScene(scene)
        # self.EndingImage.fitInView(scene.itemsBoundingRect())
        if filePath:
            if os.path.isfile(filePath+".txt"):
                if os.stat(filePath+".txt") != 0:
                    self.endPoints = np.loadtxt(filePath+".txt")
            else:
                self.endPoints = np.array([])
                # file = open(filePath+".txt", 'w')
                # file.close()
            self.loadEndPoints(filePath)

    def loadStartPoints(self, filePath):
        self.startingImage = QImage(filePath)
        Image = self.startingImage
        # Image = Image.scaled(400,300, aspectRatioMode = QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # tempScene = MyGraphicsScene()
        tempScene = QGraphicsScene()
        tempScene1 = QPixmap.fromImage(Image)
        # tempScene2 = QPixmap.fromImage(Image)
        image1 = QPainter(tempScene1)
        # image2 = QPainter(tempScene1)
        image1.setBrush(QtCore.Qt.red)
        image1.setPen(QtCore.Qt.red)
        # image2.setBrush(QtCore.Qt.red)
        # image2.setPen(QtCore.Qt.red)
        if (len(self.startPoints.shape) == 1 and self.startPoints.any()):
            self.startPoints = np.array([[self.startPoints[0], self.startPoints[1]]])

        # if self.startPoints.any():
        for point in self.startPoints:
            image1.drawEllipse(point[0], point[1], 10,10)
            # image2.drawEllipse(point[0]/2 - 2, point[1]/2 - 2, 2*2, 2*2)
        image1.setBrush(QtCore.Qt.blue)
        image1.setPen(QtCore.Qt.blue)
        if self.newStartPoints.any():
            for point in self.newStartPoints:
                image1.drawEllipse(point[0], point[1], 10,10)

        image1.end()
        # image2.end()
        tempScene.addPixmap(tempScene1)
        self.startScene = tempScene
        self.StartingImage.setScene(tempScene)
        self.StartingImage.fitInView(tempScene.itemsBoundingRect(),QtCore.Qt.KeepAspectRatio)
        self.monitor()


    def loadEndPoints(self,filePath):
        self.endingImage = QImage(filePath)
        Image = self.endingImage
        # Image = Image.scaled(400,300, aspectRatioMode = QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # tempScene = MyGraphicsScene()
        tempScene = QGraphicsScene()
        tempScene1 = QPixmap.fromImage(Image)
        # tempScene2 = QPixmap.fromImage(Image)
        image1 = QPainter(tempScene1)
        # image2 = QPainter(tempScene1)
        image1.setBrush(QtCore.Qt.red)
        image1.setPen(QtCore.Qt.red)
        # image2.setBrush(QtCore.Qt.red)
        # image2.setPen(QtCore.Qt.red)

        if (len(self.endPoints.shape) == 1 and self.endPoints.any()):
            self.endPoints = np.array([[self.endPoints[0], self.endPoints[1]]])

        for point in self.endPoints:
            image1.drawEllipse(point[0], point[1], 10,10)
            # image2.drawEllipse(point[0]/2 - 2, point[1]/2 - 2, 2*2, 2*2)
        image1.setBrush(QtCore.Qt.blue)
        image1.setPen(QtCore.Qt.blue)
        if self.newEndPoints.any():
            for point in self.newEndPoints:
                image1.drawEllipse(point[0], point[1], 10,10)

        image1.end()
        # image2.end()

        tempScene.addPixmap(tempScene1)
        self.endScene = tempScene
        self.EndingImage.setScene(tempScene)
        self.EndingImage.fitInView(tempScene.itemsBoundingRect(),QtCore.Qt.KeepAspectRatio)
        self.monitor()


    def loadFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Image file ...')

        if not filePath:
            return
        else:
            return filePath

    def monitor(self):
        if (self.StartingImage.scene() != None and self.EndingImage.scene() != None):
            self.loadedstate()

    def loadedstate(self):
        self.horizontalSlider.setDisabled(False)
        self.SlidertxtBox.setDisabled(False)
        self.BlendBtn.setDisabled(False)
        self.checkBox.setDisabled(False)
        self.startScene.mousePressEvent = self.pointStartDraw
        self.startScene.keyPressEvent = self.removeStartPoint
        self.endScene.mousePressEvent = self.pointEndDraw
        self.endScene.keyPressEvent = self.removeEndPoint
        self.mousePressEvent = self.persist
        self.isStartClicked = False
        self.isEndClicked = False
        self.wait = False


    def triangles(self):
        if self.checkBox.isChecked() and (self.startPoints.any() or self.newStartPoints.any()):
            # startingImage = self.startingImage.scaled(400,300, aspectRatioMode = QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            # endingImage = self.endingImage.scaled(400,300, aspectRatioMode = QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            # tempScene = MyGraphicsScene()
            # tempScene3 = MyGraphicsScene()
            tempScene = QGraphicsScene()
            tempScene3 = QGraphicsScene()
            tempScene1 = QPixmap.fromImage(self.startingImage)
            tempScene2 = QPixmap.fromImage(self.endingImage)
            image1 = QPainter(tempScene1)
            image2 = QPainter(tempScene2)
            if not self.startPoints.any():
                image1.setBrush(QtCore.Qt.blue)
                image1.setPen(QtCore.Qt.blue)
                image2.setBrush(QtCore.Qt.blue)
                image2.setPen(QtCore.Qt.blue)
            elif self.startPoints.any() and self.newStartPoints.any():
                image1.setBrush(QtCore.Qt.yellow)
                image1.setPen(QtCore.Qt.yellow)
                image2.setBrush(QtCore.Qt.yellow)
                image2.setPen(QtCore.Qt.yellow)
            else:
                image1.setBrush(QtCore.Qt.red)
                image1.setPen(QtCore.Qt.red)
                image2.setBrush(QtCore.Qt.red)
                image2.setPen(QtCore.Qt.red)
            if self.newStartPoints.any() and not self.startPoints.any():
                self.templistStart = self.newStartPoints
                self.templistEnd = self.newEndPoints
            elif self.newStartPoints.any():
                self.templistStart = np.vstack((self.startPoints,self.newStartPoints))
                self.templistEnd = np.vstack((self.endPoints,self.newEndPoints))
            else:
                self.templistStart = self.startPoints
                self.templistEnd = self.endPoints

            triangleList = spatial.Delaunay(self.templistStart).simplices
            for index in triangleList:
                x1 = self.templistStart[index[0]][0]
                x2 = self.templistStart[index[1]][0]
                x3 = self.templistStart[index[2]][0]
                y1 = self.templistStart[index[0]][1]
                y2 = self.templistStart[index[1]][1]
                y3 = self.templistStart[index[2]][1]
                image1.drawLine(x1,y1,x2,y2)
                image1.drawLine(x2,y2,x3,y3)
                image1.drawLine(x3,y3,x1,y1)
                x1 = self.templistEnd[index[0]][0]
                x2 = self.templistEnd[index[1]][0]
                x3 = self.templistEnd[index[2]][0]
                y1 = self.templistEnd[index[0]][1]
                y2 = self.templistEnd[index[1]][1]
                y3 = self.templistEnd[index[2]][1]
                image2.drawLine(x1,y1,x2,y2)
                image2.drawLine(x2,y2,x3,y3)
                image2.drawLine(x3,y3,x1,y1)
            for point in self.templistStart:
                image1.drawEllipse(point[0], point[1], 7, 7)
            for point in self.templistEnd:
                image2.drawEllipse(point[0], point[1], 7, 7)
            image1.end()
            image2.end()
            tempScene.addPixmap(tempScene1)
            self.startScene = tempScene
            self.StartingImage.setScene(tempScene)
            self.StartingImage.fitInView(tempScene.itemsBoundingRect(),QtCore.Qt.KeepAspectRatio)
            tempScene3.addPixmap(tempScene2)
            self.endScene = tempScene3
            self.EndingImage.setScene(tempScene3)
            self.EndingImage.fitInView(tempScene.itemsBoundingRect(),QtCore.Qt.KeepAspectRatio)
            self.loadedstate()
        else:
            self.loadStartPoints(self.startfilePath)
            self.loadEndPoints(self.endfilePath)

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()