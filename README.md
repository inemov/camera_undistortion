# camera_undistortion
 Calculation of camera undistortion matrix and coefficients from chessboard image. The resulting coefficients are camera specific and can be used to undistort images from the camera.

For theoretical background and details see:
https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html

## Use guidelines

Run APP.py. I presents 12 x 9 chessboard that can be used for taking calibration photos. Take at least 9 photos on a camera that needs to be undistorted: top-left, top-center, top-right, center-left, center-center, center-right, botton-left, bottom-center, bottom-right. Place the taken \*.jpg original distorted images in a folder.
![image](https://user-images.githubusercontent.com/24581566/150663909-863dbc7b-3bbb-4826-8357-9b77b7b8a1aa.png)

Click Open for Image directory and select a folder that contains original distorted images. The application will try to create 'undistorted' folder inside the selected directory. If such folder already exists, it will ask permission to remove all files from there. No original distorted images will be removed.
![image](https://user-images.githubusercontent.com/24581566/150664009-fcfb5381-3aa5-4d5b-95c0-dcc6bbd28334.png)

The application will analyse the original distorted images, calculate an undistortion matrix and after applying it will also save undistorted images to the 'undistorted' directory.
Both original distorted and undistorted images can be viewed using 'Original view' and 'Undistorted view' radio buttons and Previous/Next buttons.
![image](https://user-images.githubusercontent.com/24581566/150664047-7c56fcc6-acab-4d61-a2c1-ff44154fcdbf.png)
![image](https://user-images.githubusercontent.com/24581566/150664052-60daf6ae-7fb8-4dd4-9a7e-39885f33e6d0.png)

By clicking Save, undistortion_matrix.csv will be created in the originally selected directory. Its content is like:

*undistortion_mtx*
"[[861.72336592   0.         618.13980499]
 [  0.         905.37241179 315.9658367 ]
 [  0.           0.           1.        ]]"
![image](https://user-images.githubusercontent.com/24581566/150664120-e49e177c-d20b-4b76-80b6-9521175609f2.png)

*undistortion_dist*
[[ 0.1061057  -0.03205427 -0.00922332 -0.00281688 -0.06070225]]
![image](https://user-images.githubusercontent.com/24581566/150664132-bd93b70d-3462-4df9-a156-4d9833ac5f74.png)


## Requirements
Run ```pip install -r \__misc\requirements_ide.txt``` within virtual environment to install: 
spyder==5.1.5
numpy==1.22.1
opencv-python==4.5.5.62
