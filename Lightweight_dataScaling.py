from time import strftime,localtime
from os.path import join,dirname,abspath
from sys import executable
from os import mkdir
from glob import glob
from PyQt5.QtWidgets import QApplication,QLabel,QMainWindow
from PyQt5.QtGui import QPixmap,QPainter,QColor,QPen,QImage,QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.abs_dir_path = dirname(abspath(__file__)).replace("\\",'/')
        # self.abs_dir_path = '/'.join(join(executable).replace("\\", '/').split('/')[:-1])
        self.dir_path = None
        self.setStyleSheet('background-color:white;')
        self.image_label = QLabel(self)
        self.img = QImage(f"{self.abs_dir_path}/logo.png")
        pixmap = QPixmap(self.img)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()
        self.setAcceptDrops(True)
        self.points = []
        self.alpoints = []
        self.file_list = ["logo"]
        self.file_name = "logo"
        self.time_text = None
        self.setFixedSize(self.img.width(),self.img.height())
        self.pic_index = 0

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Escape:
            if self.points:
                self.points = []
            else:
                if self.alpoints:
                    self.alpoints.pop()
        if event.key() == Qt.Key_Backspace:
            if self.points:
                self.points.pop()
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Enter-1:
            self.alpoints.append(self.points)
            self.points = []
            if self.file_name != "logo":
                self.img.save(f"{self.abs_dir_path}/train/images/{self.time_text}.jpg")
                with open(f"{self.abs_dir_path}/train/labels/{self.time_text}.txt","w") as f:
                    for index,point_list in enumerate(self.alpoints):
                        if index != 0:
                            f.write('\n')
                        f.write("0")
                        for point in point_list:
                            f.write(f" {point.x()/self.img.width()} {point.y()/self.img.height()}")
                        f.write(f" {point_list[0].x()/self.img.width()} {point_list[0].y()/self.img.height()}")
        if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            if self.pic_index + 1 < len(self.file_list):
                self.time_text = strftime("%Y%m%d%H%M%S", localtime())
                self.pic_index += 1
                self.showImg(self.file_list[self.pic_index])
                self.points = []
                self.alpoints = []
                self.file_name = self.file_list[self.pic_index].split('\\')[-1].split('.')[0]
        if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            if self.pic_index - 1 >= 0:
                self.time_text = strftime("%Y%m%d%H%M%S", localtime())
                self.pic_index -= 1
                self.showImg(self.file_list[self.pic_index])
                self.points = []
                self.alpoints = []
                self.file_name = self.file_list[self.pic_index].split('\\')[-1].split('.')[0]

    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_urls = event.mimeData().urls()
        file_path = file_urls[0].toLocalFile()
        self.dir_path = '/'.join(file_path.split('/')[:-1])
        suffix = file_path.split('/')[-1].split('.')[-1]
        self.time_text = strftime("%Y%m%d%H%M%S", localtime())
        if suffix in ["jpg","png"] and len(file_urls) == 1:
            self.points = []
            self.alpoints = []
            self.showImg(file_path)
            self.file_name = file_path.split('/')[-1].split('.')[0]
            self.file_list = [self.file_name]
        else:
            self.points = []
            self.alpoints = []
            self.dir_path = file_path
            if len(file_urls) == 1:
                self.file_list = list(glob(self.dir_path + "/*.jpg")) + list(glob(self.dir_path + "/*.png"))
            else:
                self.file_list = [file_name.toLocalFile().replace('/','\\') for file_name in file_urls]
            if len(self.file_list) > 0:
                file_path = self.file_list[0]
                self.showImg(file_path)
                self.file_name = file_path.split('\\')[-1].split('.')[0]
                print(self.file_name)

    def mousePressEvent(self,event):
        self.points.append(event.pos())

    def paintEvent(self,event):
        painter = QPainter()
        show_img = self.img.copy()
        painter.begin(show_img)
        pen = QPen(QColor(255,0,0))
        pen.setWidth(5)
        painter.setPen(pen)
        for index,point in enumerate(self.points):
            painter.drawPoint(point)
            if index < len(self.points) - 1:
                painter.drawLine(self.points[index], self.points[index + 1])
            else:
                painter.drawLine(self.points[index], self.points[0])
        pen = QPen(QColor(255,255,0))
        pen.setWidth(5)
        painter.setPen(pen)
        for point_list in self.alpoints:
            for index,point in enumerate(point_list):
                painter.drawPoint(point)
                if index < len(point_list) - 1:
                    painter.drawLine(point_list[index],point_list[index+1])
                else:
                    painter.drawLine(point_list[index], point_list[0])
        painter.setFont(QFont('Arial', 15))
        painter.setPen(QColor(0, 255, 0))
        painter.drawText(10, 20, f"{self.pic_index+1}/{len(self.file_list)}")
        painter.end()
        pixmap = QPixmap(show_img)
        self.image_label.setPixmap(pixmap)

    def showImg(self,img_path):
        self.img = QImage(img_path)
        self.setFixedSize(self.img.width(),self.img.height())
        pixmap = QPixmap(self.img)

        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()

if __name__ == "__main__":
    abs_dir_path = dirname(abspath(__file__)).replace("\\", '/')
    # abs_dir_path = '/'.join(join(executable).replace("\\", '/').split('/')[:-1])
    mkdir_list = [f"{abs_dir_path}/train/",f"{abs_dir_path}/train/images/",f"{abs_dir_path}/train/labels/"]
    for mkdir_name in mkdir_list:
        try:
            mkdir(mkdir_name)
        except:
            print(f"folder:{mkdir_name} Created!")
    with open(f"{abs_dir_path}/pallet.yaml",'w') as f:
        for classify in ["train","test","val"]:
            f.write(f"{classify}: {abs_dir_path}/train/images\n")
        f.write("nc: 1\n")
        f.write("names: ['pallet']")
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("dataScaling")
    window.show()
    app.exec_()