# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:09:46 2020
@author: Ivan Nemov
"""


from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import cv2
import numpy as np
import csv
import time



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.form_widget = FormWidget(self)
        _widget = QtWidgets.QWidget()
        _layout = QtWidgets.QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.showMaximized()
        self.setWindowTitle("Camera undistortion calibration")
        self.setWindowIcon(QtGui.QIcon(QtCore.QDir.currentPath()+'/res/img/win/app_logo.png'))
        
    
        
class FormWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.original_image_array = []
        self.undistorted_image_array = []
        self.current_original_image_to_show = 0
        self.current_undistorted_image_to_show = 0

    def __controls(self):
        
        self.menu_bar=QtWidgets.QMenuBar()
        self.menu_bar.setFixedHeight(20)
        file_menu=self.menu_bar.addMenu("File")
        exit_action=QtWidgets.QAction('Exit',self)
        exit_action.triggered.connect(QtWidgets.QApplication.quit)
        file_menu.addAction(exit_action)

        self.FrameBox = QtWidgets.QGroupBox(self)
        self.FrameBox.setObjectName("FrameBox")
        self.FrameBox.setTitle("Calibration frame")
        self.x_dim = self.FrameBox.frameGeometry().width()-45
        self.y_dim = self.FrameBox.frameGeometry().height()-65
        
        self.FrameView=QtWidgets.QLabel(self.FrameBox)
        self.FrameView.setObjectName("FrameView")
        self.FrameViewPixmap = QtGui.QPixmap(QtCore.QDir.currentPath()+'/res/img/camera_undistortion_image.jpg')
        self.FrameView.setPixmap(self.FrameViewPixmap.scaled(self.x_dim, self.y_dim, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
        self.Original_Dir_Label = QtWidgets.QLabel(self.FrameBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Original_Dir_Label.setFont(font)
        self.Original_Dir_Label.setObjectName("Original_Dir_Label")
        self.Original_Dir_Label.setText("Image directory: ")
        
        self.Original_Dir = QtWidgets.QLineEdit(self.FrameBox)
        self.Original_Dir.setFixedHeight(25)
        self.Original_Dir.setText(str(QtCore.QDir.currentPath()+'/resolution_cases'))
        
        self.Original_Dir_CommandButton = QtWidgets.QPushButton(self.FrameBox)
        self.Original_Dir_CommandButton.setObjectName("Original_Dir_CommandButton")
        self.Original_Dir_CommandButton.setFixedWidth(80)
        self.Original_Dir_CommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Original_Dir_CommandButton.setText("Open")
        self.Original_Dir_CommandButton.clicked.connect(self.open_image_directory)
        
        self.ViewSelBox = QtWidgets.QGroupBox(self.FrameBox)
        self.ViewSelBox.setObjectName("ViewSelBox")
        self.ViewSelBox.setFixedWidth(220)
        
        self.OriginalViewRadioButton = QtWidgets.QRadioButton(self.ViewSelBox)
        self.OriginalViewRadioButton.setObjectName("OriginalViewRadioButton")
        self.OriginalViewRadioButton.setText("Original view")
        self.OriginalViewRadioButton.setChecked(True)
        self.OriginalViewRadioButton.setDisabled(False)
        self.OriginalViewRadioButton.clicked.connect(self.swap_view)
        
        self.UndistortedViewRadioButton = QtWidgets.QRadioButton(self.ViewSelBox)
        self.UndistortedViewRadioButton.setObjectName("UndistortedViewRadioButton")
        self.UndistortedViewRadioButton.setText("Undistorted view")
        self.UndistortedViewRadioButton.setChecked(False)
        self.UndistortedViewRadioButton.setDisabled(False)
        self.UndistortedViewRadioButton.clicked.connect(self.swap_view)
        
        self.Chessboard_width_Label = QtWidgets.QLabel(self.FrameBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Chessboard_width_Label.setFont(font)
        self.Chessboard_width_Label.setObjectName("Chessboard_width_Label")
        self.Chessboard_width_Label.setText("Chessboard width: ")
        
        self.Chessboard_width = QtWidgets.QLineEdit(self.FrameBox)
        self.Chessboard_width.setFixedHeight(25)
        self.Chessboard_width.setFixedWidth(25)
        self.Chessboard_width.setText(str(12))
        
        self.Chessboard_height_Label = QtWidgets.QLabel(self.FrameBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Chessboard_height_Label.setFont(font)
        self.Chessboard_height_Label.setObjectName("Chessboard_height_Label")
        self.Chessboard_height_Label.setText("Chessboard height: ")
        
        self.Chessboard_height = QtWidgets.QLineEdit(self.FrameBox)
        self.Chessboard_height.setFixedHeight(25)
        self.Chessboard_height.setFixedWidth(25)
        self.Chessboard_height.setText(str(9))
        
        self.PreviousButton = QtWidgets.QPushButton(self.FrameBox)
        self.PreviousButton.setObjectName("PreviousButton")
        self.PreviousButton.setFixedWidth(75)
        self.PreviousButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PreviousButton.setText("Previous")
        self.PreviousButton.clicked.connect(self.show_previous_image)
        
        self.NextButton = QtWidgets.QPushButton(self.FrameBox)
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setFixedWidth(75)
        self.NextButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextButton.setText("Next")
        self.NextButton.clicked.connect(self.show_next_image)
        
        self.SaveButton = QtWidgets.QPushButton(self.FrameBox)
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.setFixedWidth(75)
        self.SaveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SaveButton.setText("Save")
        self.SaveButton.clicked.connect(self.save_calibration_matrix)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setFixedHeight(10)
        self.progressBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        
    def __layout(self):
        self.vmainbox=QtWidgets.QVBoxLayout()
        self.hmenubox = QtWidgets.QHBoxLayout()
        self.hmenubox.addWidget(self.menu_bar)
        self.vmainbox.addLayout(self.hmenubox)
        self.vmainbox.addWidget(self.FrameBox)
        self.vmainbox.addWidget(self.progressBar)
        self.setLayout(self.vmainbox)
        
        self.viewselbox=QtWidgets.QHBoxLayout()
        self.viewselbox.addWidget(self.OriginalViewRadioButton)
        self.viewselbox.addWidget(self.UndistortedViewRadioButton)
        self.ViewSelBox.setLayout(self.viewselbox)
        
        self.hgroupbox = QtWidgets.QHBoxLayout()
        self.hgroupbox.addWidget(self.Original_Dir_Label)
        self.hgroupbox.addWidget(self.Original_Dir)
        self.hgroupbox.addWidget(self.Original_Dir_CommandButton)
        self.hgroupbox.addWidget(self.ViewSelBox)
        self.hgroupbox.addWidget(self.Chessboard_width_Label)
        self.hgroupbox.addWidget(self.Chessboard_width)
        self.hgroupbox.addWidget(self.Chessboard_height_Label)
        self.hgroupbox.addWidget(self.Chessboard_height)
        self.hgroupbox.addWidget(self.PreviousButton)
        self.hgroupbox.addWidget(self.NextButton)
        self.hgroupbox.addWidget(self.SaveButton)
        self.hgroupbox.setAlignment(QtCore.Qt.AlignCenter)

        self.vgroupbox = QtWidgets.QVBoxLayout()
        self.vgroupbox.addStretch(1)
        self.vgroupbox.addWidget(self.FrameView)
        self.vgroupbox.addStretch(1)
        self.vgroupbox.addLayout(self.hgroupbox)
        self.vgroupbox.setAlignment(self.FrameView, QtCore.Qt.AlignCenter)
        self.FrameBox.setLayout(self.vgroupbox)

    def open_image_directory(self):
        folder_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.Original_Dir.setText(folder_name)
        self.original_image_array = []
        original_image_filename_array = []
        file_names_array = []
        file_names_array = os.listdir(folder_name)
        if file_names_array != []:
            for file_item in file_names_array:
                if file_item[-3:] == "jpg":
                    self.original_image_array.append(folder_name + "/" + file_item)
                    original_image_filename_array.append(file_item)
        if len(self.original_image_array) == 0:
            QtWidgets.QMessageBox.warning(self,"No images in the folder", "Select folder with images.")
            return None
        try:
            os.mkdir(folder_name + "/undistorted")
        except:
            try:
                if os.path.isdir(folder_name + "/undistorted") == False:
                    QtWidgets.QMessageBox.warning(self,"Cannot create new directory within selected folder", "Check folder access rights.")
                    return None
                else:
                    reply = QtWidgets.QMessageBox.question(self, "Directory for undistorted images already exists", "Replace all images in the directory?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
                    if reply == QtWidgets.QMessageBox.Cancel:
                        return None
            except:
                QtWidgets.QMessageBox.warning(self,"Cannot create new directory within selected folder", "Unknown error")
                return None
        file_names_array = []
        file_names_array = os.listdir(folder_name + "/undistorted")
        if file_names_array != []:
            for file_item in file_names_array:
                if file_item[-3:] == "jpg":
                    os.remove(folder_name + "/undistorted/" + file_item)
        #find coeefficients
        for file_item in original_image_filename_array:
            chessboard_widht = int(self.Chessboard_width.text()) - 1
            chessboard_height = int(self.Chessboard_height.text()) - 1
            original_file_name = folder_name + "/" + file_item
            image = cv2.imread(original_file_name, cv2.IMREAD_COLOR)
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((chessboard_widht*chessboard_height,3), np.float32)
            objp[:,:2] = np.mgrid[0:chessboard_height,0:chessboard_widht].T.reshape(-1,2)
            # Arrays to store object points and image points from all the images.
            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(grayImage, (chessboard_height,chessboard_widht),None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(grayImage,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)
            self.progress_bar_update(50*original_image_filename_array.index(file_item)/len(original_image_filename_array))
        #calibrate camera
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, grayImage.shape[::-1],None,None)
        self.undistorted_image_array = []
        #undistort images
        for file_item in original_image_filename_array:
            original_file_name = folder_name + "/" + file_item
            image = cv2.imread(original_file_name, cv2.IMREAD_COLOR)
            h,  w = image.shape[:2]
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))
            # undistort
            mapx,mapy = cv2.initUndistortRectifyMap(self.mtx,self.dist,None,newcameramtx,(w,h),5)
            dst = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)
            # crop the image
            #x,y,w,h = roi
            #dst = dst[y:y+h, x:x+w]
            undistorted_filename = folder_name + "/undistorted/" + file_item
            cv2.imwrite(undistorted_filename,dst)
            self.undistorted_image_array.append(undistorted_filename)
            self.progress_bar_update(50+50*original_image_filename_array.index(file_item)/len(original_image_filename_array))
        self.progress_bar_update(100)
        time.sleep(0.25)
        self.progress_bar_update(0)
        self.current_original_image_to_show = 0
        self.current_undistorted_image_to_show = 0
        self.prepare_image(self.original_image_array[self.current_original_image_to_show], original=True)
        
    def show_previous_image(self):  
        if (len(self.original_image_array) == 0 and self.OriginalViewRadioButton.isChecked() == True) or (len(self.undistorted_image_array) == 0 and self.UndistortedViewRadioButton.isChecked() == True):
            return None
        else:
            if self.OriginalViewRadioButton.isChecked() == True:
                if self.current_original_image_to_show == 0:
                    self.current_original_image_to_show = len(self.original_image_array) - 1
                else:
                    self.current_original_image_to_show = self.current_original_image_to_show - 1
                self.prepare_image(self.original_image_array[self.current_original_image_to_show], original=True)
            elif self.UndistortedViewRadioButton.isChecked() == True:
                if self.current_undistorted_image_to_show == 0:
                    self.current_undistorted_image_to_show = len(self.undistorted_image_array) - 1
                else:
                    self.current_undistorted_image_to_show = self.current_undistorted_image_to_show - 1
                self.prepare_image(self.undistorted_image_array[self.current_undistorted_image_to_show], original=False)
    
    def show_next_image(self): 
        if (len(self.original_image_array) == 0 and self.OriginalViewRadioButton.isChecked() == True) or (len(self.undistorted_image_array) == 0 and self.UndistortedViewRadioButton.isChecked() == True):
            return None
        else:
            if self.OriginalViewRadioButton.isChecked() == True:
                if self.current_original_image_to_show == len(self.original_image_array)-1:
                    self.current_original_image_to_show = 0
                else:
                    self.current_original_image_to_show = self.current_original_image_to_show + 1
                self.prepare_image(self.original_image_array[self.current_original_image_to_show], original=True)
            elif self.UndistortedViewRadioButton.isChecked() == True:
                if self.current_undistorted_image_to_show == len(self.undistorted_image_array)-1:
                    self.current_undistorted_image_to_show = 0
                else:
                    self.current_undistorted_image_to_show = self.current_undistorted_image_to_show + 1
                self.prepare_image(self.undistorted_image_array[self.current_undistorted_image_to_show], original=False)
            
    def prepare_image(self, file_path, original=True):
        try:
            image = cv2.imread(file_path,cv2.IMREAD_COLOR)
            rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            return None
        if original:
            chessboard_widht = int(self.Chessboard_width.text()) - 1
            chessboard_height = int(self.Chessboard_height.text()) - 1
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((chessboard_widht*chessboard_height,3), np.float32)
            objp[:,:2] = np.mgrid[0:chessboard_height,0:chessboard_widht].T.reshape(-1,2)
            # Arrays to store object points and image points from all the images.
            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(grayImage, (chessboard_height, chessboard_widht),None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(grayImage,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)
                # Draw and display the corners
                rgbImage = cv2.drawChessboardCorners(rgbImage, (chessboard_height, chessboard_widht), corners2,ret)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        self.FrameViewPixmap = QtGui.QPixmap(convertToQtFormat)
        self.draw_image()

    def swap_view(self):
        self.current_original_image_to_show = 0
        self.current_undistorted_image_to_show = 0
        if (len(self.original_image_array) == 0 and self.OriginalViewRadioButton.isChecked() == True) or (len(self.undistorted_image_array) == 0 and self.UndistortedViewRadioButton.isChecked() == True):
            return None
        else:
            if self.OriginalViewRadioButton.isChecked() == True:
                self.prepare_image(self.original_image_array[self.current_original_image_to_show], original=True)
            elif self.UndistortedViewRadioButton.isChecked() == True:
                self.prepare_image(self.undistorted_image_array[self.current_undistorted_image_to_show], original=False)
    
    def draw_image(self):
        try:
            self.FrameView.setPixmap(self.FrameViewPixmap.scaled(self.x_dim, self.y_dim, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        except:
            return None
    
    def save_calibration_matrix(self):
        # print("Undistortion mtx ")
        # print(self.mtx)
        # print("\n")
        # print("Undistortion dist ")
        # print(self.dist)
        filename = self.Original_Dir.text() + "/undistortion_matrix.csv"
        try:
            if os.path.isfile(filename):
                os.remove(filename)
        except:
            filename = self.Original_Dir.text() + "/undistortion_matrix.csv"
        with open(filename, 'w', newline='') as csvfile:
            undistortion_matrix_csv = csv.writer(csvfile, dialect='excel')
            undistortion_mtx = ['undistortion_mtx']
            undistortion_mtx.append(self.mtx)
            undistortion_matrix_csv.writerow(undistortion_mtx)
            undistortion_dist = ['undistortion_dist']
            undistortion_dist.append(self.dist)
            undistortion_matrix_csv.writerow(undistortion_dist)
            
    def resizeEvent(self, event):
        self.x_dim = self.FrameBox.frameGeometry().width()-100
        self.y_dim = self.FrameBox.frameGeometry().height()-100
        if self.x_dim*0.74585 < self.y_dim:
            self.y_dim = self.x_dim*0.74585
        elif self.y_dim/0.74585 < self.x_dim:
            self.x_dim = self.y_dim/0.74585
        self.draw_image()

    def progress_bar_update(self, percentage):
        self.progressBar.setValue(percentage)

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
    
if __name__ == '__main__':
    sys.exit(main())